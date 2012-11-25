from five import grok
from zope import schema
from zope.interface import Interface
from z3c.form.i18n import MessageFactory as _
from plone.directives import dexterity, form

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

    def languages(self):
        """ Return the contents languages dictionary as a list of strings
        """

        language_vocab = availableLanguages(self.context).__iter__()
        lang_list = []
        notfinished = True;
        while notfinished:            
            try:
                lang = language_vocab.next().title
                lang_list.append(lang)
            except StopIteration:
                notfinished = False;

        return lang_list

    def classlist(self):
        """ Return the currently selected classlist
        """
#        import pdb; pdb.set_trace()
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

        title = self.request.get('title', '')
        print title

        # Validate
        # name/title must exist
        if self.request.get('title', '') == '':
            msg = _("Name is required")
            return [msg,'error']

        classlist = self.context

        # name/title must be unique
        old_title = classlist.Title()
        new_title = self.request.get('title')
        if old_title != new_title:
            parent = classlist.aq_inner.aq_parent
            for alist in parent.objectValues():
                if alist != self and alist.Title() == new_title:
                    msg = _("Name is not unique")
                    return [msg,'error']

        url = "%s" % self.context.absolute_url()
        return [url,'redirect']

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''




















