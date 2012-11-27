from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
import unittest2 as unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.testing import z2

PROJECTNAME = "upfront.classlist"

class TestCase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.topictree
        import upfront.classlist
        self.loadZCML(package=collective.topictree)
        self.loadZCML(package=upfront.classlist)
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="fixture:Integration")


class UpfrontClassListTestBase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.intids = getUtility(IIntIds)
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.portal.invokeFactory(type_name='Folder', id='topictrees',
                                  title='Topic Trees')
        folder = self.portal._getOb('topictrees')

        self.topictrees = self.portal.topictrees
        self.topictrees.invokeFactory('collective.topictree.topictree',
                                      'language', title='Language')
        topictree = self.topictrees._getOb('language')

        topictree.invokeFactory('collective.topictree.topic',
                                'afrikaans', title='Afrikaans')
        self.topic1 = topictree._getOb('afrikaans')
        topictree.invokeFactory('collective.topictree.topic',
                                'english', title='English')
        self.topic2 = topictree._getOb('english')
        topictree.invokeFactory('collective.topictree.topic',
                                'xhosa', title='Xhosa')
        self.topic3 = topictree._getOb('xhosa')

        self.topictree = topictree

        # create a classlists folder for testing
        self.portal.invokeFactory(type_name='Folder', id='classlists',
                                  title='Classlists')
        self.classlists = self.portal._getOb('classlists') 

        self.classlists.invokeFactory('upfront.classlist.content.classlist',
                                      'list1', title='List1')
        self.classlist1 = self.classlists._getOb('list1')
        self.classlists.invokeFactory('upfront.classlist.content.classlist',
                                      'list2', title='List2')
        self.classlist2 = self.classlists._getOb('list2')

        # add 3 learners to classlist1
        self.classlist1.invokeFactory('upfront.classlist.content.learner',
                                      'learner1', title='Learner1')
        self.learner1 = self.classlist1._getOb('learner1')
        self.classlist1.invokeFactory('upfront.classlist.content.learner',
                                      'learner2', title='Learner2')
        self.learner2 = self.classlist1._getOb('learner2')
        self.classlist1.invokeFactory('upfront.classlist.content.learner',
                                      'learner3', title='Learner3')
        self.learner3 = self.classlist1._getOb('learner3')




