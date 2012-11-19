from five import grok
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.CMFCore.utils import getToolByName

from upfront.classlist import MessageFactory as _

GENDER = SimpleVocabulary(
    [SimpleTerm(value=u'Male', title=_(u'Male')),
     SimpleTerm(value=u'Female', title=_(u'Female'))]
    )


