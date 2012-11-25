from five import grok
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.relationfield.schema import RelationChoice
from z3c.form.browser.select import SelectFieldWidget
from plone.directives import dexterity, form
from plone.uuid.interfaces import IUUID

from upfront.classlist import MessageFactory as _
from upfront.classlist.vocabs import GENDER
from upfront.classlist.vocabs import availableLanguages

class ILearner(form.Schema):
    """ Description of Learner content type
    """

    code = schema.TextLine(
            title=_(u"Student Code"),
            required=True,
        )

    name = schema.TextLine(
            title=_(u"Name"),
            required=True,
        )

    form.widget(home_language=SelectFieldWidget)
    home_language = RelationChoice(
            title=_(u"Home Language"),
            source=availableLanguages,
        )

    gender = schema.Choice(
            title=_(u"Gender"),
            vocabulary=GENDER,
            required=True,
        )


class Learner(dexterity.Item):
    grok.implements(ILearner)

    def getIUUID(self):
        return IUUID(self)
