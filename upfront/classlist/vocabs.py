from five import grok
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

from zope.component.hooks import getSite
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from upfront.classlist import MessageFactory as _

GENDER = SimpleVocabulary(
    [SimpleTerm(value=u'Male', title=_(u'Male')),
     SimpleTerm(value=u'Female', title=_(u'Female'))]
    )

@grok.provider(IContextSourceBinder)
def availableLanguages(context):
    terms = []

    # This method can assume that the language topic tree is in a fixed location 
    # in the site eg /topictrees/language for now.

    portal_state = context.restrictedTraverse('@@plone_portal_state')
    portal = portal_state.portal()

    language_folder = portal.topictrees.language

    topics = language_folder.getFolderContents()
    for brain in topics:
        topic = brain.getObject()
        intids = getUtility(IIntIds)
        topic_intid = intids.getId(topic)
        terms.append(SimpleVocabulary.createTerm(topic_intid, topic_intid,
                                                 topic.Title()))

    return SimpleVocabulary(terms)
