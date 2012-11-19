from five import grok
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.relationfield.schema import RelationChoice
from z3c.form.browser.select import SelectFieldWidget
from plone.directives import dexterity, form

from upfront.classlist import MessageFactory as _
from upfront.classlist.vocabs import GENDER

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

    gender = schema.Choice(
            title=_(u"Gender"),
            vocabulary=GENDER,
            required=True,
        )


class Learner(dexterity.Item):
    grok.implements(ILearner)
