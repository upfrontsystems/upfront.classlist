from zope.component import createObject
from zope.component import queryUtility

from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.dexterity.interfaces import IDexterityFTI

from base import UpfrontClassListTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

from upfront.classlist.content.learner import ILearner

class TestLearner(UpfrontClassListTestBase):
    """ Basic methods to test learner content types """
    
    def test_learner_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.classlist.content.learner')
        self.assertNotEquals(None, fti)

    def test_learner_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.classlist.content.learner')
        schema = fti.lookupSchema()
        self.assertEquals(ILearner, schema, 'Learner schema incorrect.')

    def test_learner_factory(self):
        fti = queryUtility(
            IDexterityFTI, name='upfront.classlist.content.learner')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(
            ILearner.providedBy(new_object), 
            'learner provides wrong interface.')

