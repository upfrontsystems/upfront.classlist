import json
from five import grok

from zope.app.container.interfaces import INameChooser
from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from z3c.relationfield import RelationValue
from z3c.form.i18n import MessageFactory as _

from plone.directives import dexterity, form

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName

from upfront.classlist.vocabs import availableLanguages

class IClassList(form.Schema):
    """ Description of ClassList content type
    """


class ClassList(dexterity.Container):
    grok.implements(IClassList)


grok.templatedir('templates')
class View(dexterity.DisplayForm):
    grok.context(IClassList)
    grok.template('viewclasslists')
    grok.require('zope2.View')

    def getSaveUrl(self):
        return '%s/@@renameclasslist' % self.context.absolute_url()

    def languages(self):
        """ Return the contents languages dictionary as a list of strings
        """

        language_vocab = availableLanguages(self.context).__iter__()
        lang_list = []
        notfinished = True;
        while notfinished:            
            try:
                lang = language_vocab.next()
                # add title and intid to lang_list
                lang_list.append([lang.title, lang.value])
            except StopIteration:
                notfinished = False;

        return lang_list

    def classlist(self):
        """ Return the currently selected classlist
        """
        return self.context.title

    def learners(self):
        """ Return all the learners in the current classlist folder
        """
        contentFilter = {
            'portal_type': 'upfront.classlist.content.learner'}
        return self.context.getFolderContents(contentFilter,full_objects=True)


class RenameClassListView(grok.View):
    """ Rename the current classlist
    """
    grok.context(Interface)
    grok.name('renameclasslist') 
    grok.require('zope2.View')

    def __call__(self):
        """ Rename the current classlist """

        new_title = self.request.form['rename.form.newtitle']

        # name/title must exist
        if new_title == '':
            msg = _("Name is required")
            return

        classlist = self.context
        old_title = classlist.Title()

        # name/title must be unique
        if old_title != new_title:
            parent = classlist.aq_inner.aq_parent
            for alist in parent.objectValues():
                if alist != self and alist.Title() == new_title:
                    msg = _("Name is not unique")
                    return

        # Create/Modify
        if old_title != new_title:
            classlists = classlist.aq_parent
            classlist.edit(title=new_title)
            name = INameChooser(classlists).chooseName(None, classlist)
            classlists.manage_renameObject(classlist.id, name)
            msg = _("Classlist %s was modified" % classlist.Title())
            return self.request.RESPONSE.redirect( \
                   "%s" % self.context.absolute_url())

        msg = _("New name identical to old name")
        return

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class RemoveLearnersView(grok.View):
    """ Removes a selected number of learners from a classlist
    """
    grok.context(Interface)
    grok.name('removelearners')
    grok.require('zope2.View')

    def __call__(self):
        """ Remove a selected number of learners from a classlist """

        remove_ids = self.request.get('remove_ids', '')

        if remove_ids == '':
            msg = _("No Learners selected")
            return json.dumps({'result'   : 'error',
                               'contents' : msg})

        if isinstance(remove_ids, basestring):
            # wrap string in a list for deleting mechanism to work
            remove_ids = [remove_ids]

        classlist = self.context
        for remove_id in remove_ids:
            del classlist[remove_id]

        # success
        msg = _("Learner(s) removed from Classlist %s" % classlist.Title())
        return json.dumps({'result'   : 'info',
                           'contents' : msg})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class AddLearnerView(grok.View):
    """ Add a learner to a classlist
    """
    grok.context(Interface)
    grok.name('addlearner')
    grok.require('zope2.View')

    def __call__(self):
        """ Add a learner to a classlist """

        learner_code = self.request.get('learner_code', '')
        learner_name = self.request.get('learner_name', '')
        learner_gender = self.request.get('learner_gender', '')
        learner_lang_id = self.request.get('learner_lang_id', '')
        learner_lang = self.request.get('learner_lang', '')

        # validate that student code is unique
        status = ''
        catalog = getToolByName(self.context, 'portal_catalog')
        result = catalog(id=learner_code)
        if len(result) != 0:
            status = 'error'
            msg = _("Student code not unique")
            return json.dumps({'status' : status,
                               'msg'    : msg})

        classlist = self.context
        classlist.invokeFactory('upfront.classlist.content.learner',
                                      learner_code, title=learner_code)
        new_learner = classlist._getOb(learner_code)

        new_learner.code = learner_code
        new_learner.name = learner_name
        new_learner.gender = learner_gender       
        new_learner.home_language = RelationValue(int(learner_lang_id))
        notify(ObjectModifiedEvent(new_learner))

        learner_id = new_learner.id
        learner_editurl = '%s/edit' % new_learner.absolute_url()

        # success
        status = 'info'
        msg = _("New learner added")
        return json.dumps({'id'              : learner_id,
                           'learner_code'    : learner_code,
                           'learner_name'    : learner_name,
                           'learner_editurl' : learner_editurl,
                           'learner_gender'  : learner_gender,
                           'learner_lang'    : learner_lang,
                           'status' : status,
                           'msg'    : msg})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

