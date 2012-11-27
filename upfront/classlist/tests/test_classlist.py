from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI

from base import UpfrontClassListTestBase
from upfront.classlist.content.classlist import IClassList
from upfront.classlist.vocabs import availableLanguages

class TestClassList(UpfrontClassListTestBase):
    """ Basic methods to test classlists and their default view """
    
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

    def test_getSaveUrl(self):
        view = self.classlist1.restrictedTraverse('@@view')
        self.assertEqual(view.getSaveUrl(), 
                         '%s/@@renameclasslist' % self.classlist1.absolute_url())

    def test_languages(self):
        view = self.classlist1.restrictedTraverse('@@view')
        language_vocab = availableLanguages(self.classlist1).__iter__()
        lang_list = []
        notfinished = True;
        while notfinished:            
            try:
                lang = language_vocab.next()
                # add title and intid to lang_list
                lang_list.append([lang.title, lang.value])
            except StopIteration:
                notfinished = False;
        self.assertEqual(view.languages(),lang_list)

    def test_classlist(self):
        view = self.classlist1.restrictedTraverse('@@view')
        self.assertEqual(view.classlist(),self.classlist1.title)

    def test_learners(self):
        view = self.classlist1.restrictedTraverse('@@view')

        self.assertEqual(len(view.learners()), 2)
        self.assertEqual([obj.id for obj in view.learners()], ['learner1','learner2'])


class TestRenameClassListView(UpfrontClassListTestBase):
    """ Test RenameClassList view
    """

    def test__call__(self):
        view = self.classlist1.restrictedTraverse('@@renameclasslist')
        return True


class TestRemoveLearnersView(UpfrontClassListTestBase):
    """ Test RemoveLearners view
    """

    def test__call__(self):
        view = self.classlist1.restrictedTraverse('@@removelearners')
        return True


class TestAddLearnerView(UpfrontClassListTestBase):
    """ Test AddLearner view
    """

    def test__call__(self):
        view = self.classlist1.restrictedTraverse('@@addlearner')
        return True



