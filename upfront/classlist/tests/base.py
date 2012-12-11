from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from z3c.relationfield import RelationValue

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
import unittest2 as unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.testing import z2

from upfront.classlist.vocabs import availableLanguages

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

        # some details for learner1
        self.learner1.code = '1'
        self.learner1.name = 'John'
        self.learner1.gender = 'Male'

        # some details for learner2
        self.learner2.code = '2'
        self.learner2.name = 'Jennie'
        self.learner2.gender = 'Female'

        # some details for learner3
        self.learner3.code = '3'
        self.learner3.name = 'Nomsa'
        self.learner3.gender = 'Female'

        language_vocab = availableLanguages(self.classlist1).__iter__()
        #associate each language with a learner
        lang = language_vocab.next()
        self.learner1.home_language = RelationValue(lang.value)
        lang = language_vocab.next()
        self.learner2.home_language = RelationValue(lang.value)
        lang = language_vocab.next()
        self.learner3.home_language = RelationValue(lang.value)

        notify(ObjectModifiedEvent(self.learner1))
        notify(ObjectModifiedEvent(self.learner2))
        notify(ObjectModifiedEvent(self.learner3))

