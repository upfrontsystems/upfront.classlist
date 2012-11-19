from zope.component import createObject
from zope.component import queryUtility

from plone.uuid.interfaces import IUUID
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.dexterity.interfaces import IDexterityFTI

from base import UpfrontClassListTestBase
from base import PROJECTNAME
from base import INTEGRATION_TESTING

from upfront.classlist.content.classlist import IClassList

class TestClassList(UpfrontClassListTestBase):
    """ Basic methods to test classlists """
    
    def test_classlist_fti(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.classlist.content.classlist')
        self.assertNotEquals(None, fti)

    def test_classlist_schema(self):
        fti = queryUtility(IDexterityFTI,
                           name='upfront.classlist.content.classlist')
        schema = fti.lookupSchema()
        self.assertEquals(IClassList, schema, 'Class List schema incorrect.')

    def test_classlist_factory(self):
        fti = queryUtility(
            IDexterityFTI, name='upfront.classlist.content.classlist')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(
            IClassList.providedBy(new_object), 
            'class list provides wrong interface.')
