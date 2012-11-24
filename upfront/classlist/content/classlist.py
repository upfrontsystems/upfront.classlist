from five import grok
from zope import schema
from zope.interface import Interface
from plone.directives import dexterity, form

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

    def learners(self):
        """ Return all the learners in the current classlist folder
        """
        contentFilter = {
            'portal_type': 'upfront.classlist.content.learner'}
        import pdb; pdb.set_trace()
        return self.context.getFolderContents(contentFilter,full_objects=True)




