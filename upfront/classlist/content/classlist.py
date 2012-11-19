from five import grok
from zope import schema
from zope.interface import Interface
from plone.directives import dexterity, form

class IClassList(form.Schema):
    """ Description of ClassList content type
    """

class ClassList(dexterity.Container):
    grok.implements(IClassList)

