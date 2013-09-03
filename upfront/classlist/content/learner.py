from five import grok
from zope import schema
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.relationfield.schema import RelationChoice
from z3c.form.browser.select import SelectFieldWidget
from z3c.form import validator
from plone.directives import dexterity, form
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName

from upfront.classlist import MessageFactory as _
from upfront.classlist.vocabs import GENDER
from upfront.classlist.vocabs import availableLanguages

class ILearner(form.Schema):
    """ Description of Learner content type
    """

    code = schema.TextLine(
            title=_(u"Code"),
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


class LearnerCodeValidator(validator.SimpleFieldValidator):
    
    def validate(self, value):
        super(LearnerCodeValidator, self).validate(value)

        catalog = getToolByName(self.context, 'portal_catalog')
        result = catalog(portal_type='upfront.classlist.content.learner',
                         id=value)
        count = len(result)
        # we are editing a learner without changing the value
        if count == 1 and result[0].UID == IUUID(self.context):
            return True
        elif count > 0:
            raise Invalid(_(u"This learner code already "
                             "exists in the system. The learner code "
                             "must be unique."))

validator.WidgetValidatorDiscriminators(LearnerCodeValidator, 
                                            field=ILearner['code'])
grok.global_adapter(LearnerCodeValidator)
