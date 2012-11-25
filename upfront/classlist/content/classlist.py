from five import grok
from zope import schema
from zope.interface import Interface
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

    def learners(self):
        """ Return all the learners in the current classlist folder
        """
        contentFilter = {
            'portal_type': 'upfront.classlist.content.learner'}
        return self.context.getFolderContents(contentFilter,full_objects=True)





