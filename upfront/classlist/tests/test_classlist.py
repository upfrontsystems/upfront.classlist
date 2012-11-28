import json
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

        self.assertEqual(len(view.learners()), 3)
        self.assertEqual([obj.id for obj in view.learners()],
                         ['learner1','learner2','learner3'])


class TestRenameClassListView(UpfrontClassListTestBase):
    """ Test RenameClassList view
    """

    def test__call__(self):
        view = self.classlist1.restrictedTraverse('@@renameclasslist')

        self.request.form['rename.form.newtitle'] = ''
        self.assertEqual(self.classlist1.id,'list1')        
        self.assertEqual(view(),"Name is required")
        self.assertEqual(self.classlist1.id,'list1')

        self.request.form['rename.form.newtitle'] = 'List2'
        self.assertEqual(self.classlist1.id,'list1')        
        self.assertEqual(view(),"Name is not unique")
        self.assertEqual(self.classlist1.id,'list1')        

        self.request.form['rename.form.newtitle'] = 'List1'
        self.assertEqual(self.classlist1.id,'list1')        
        self.assertEqual(view(),"New name identical to old name")
        self.assertEqual(self.classlist1.id,'list1')        

        self.request.form['rename.form.newtitle'] = 'anotherlist1'
        self.assertEqual(self.classlist1.id,'list1')        
        self.assertEqual(view(),self.classlist1.absolute_url())
        self.assertEqual(self.classlist1.id,'anotherlist1')

class TestRemoveLearnersView(UpfrontClassListTestBase):
    """ Test RemoveLearners view
    """

    def test__call__(self):
        view = self.classlist1.restrictedTraverse('@@removelearners')
        self.request.set('remove_ids','')
        test = json.dumps({'status'   : 'error',
                           'msg' : "No Learners selected"})
        self.assertEqual(len(self.classlist1.getFolderContents()),3)
        self.assertEqual(view(),test)
        self.assertEqual(len(self.classlist1.getFolderContents()),3)

        self.request.set('remove_ids',['learner1', 'learner3'])
        test2 = json.dumps({'status'   : 'info',
                            'msg' :"Learner(s) removed from Classlist List1"})
        self.assertEqual(view(),test2)
        self.assertEqual(len(self.classlist1.getFolderContents()),1)


class TestAddLearnerView(UpfrontClassListTestBase):
    """ Test AddLearner view
    """

    def test__call__(self):

        view = self.classlist1.restrictedTraverse('@@addlearner')

        # get a valid Language and its intid
        language_vocab = availableLanguages(self.classlist1).__iter__()
        try:
           lang = language_vocab.next()
        except StopIteration:
            pass

        self.request.set('learner_code','001')
        self.request.set('learner_name','James')
        self.request.set('learner_gender','Male')
        self.request.set('learner_lang_id',lang.value)
        self.request.set('learner_lang',lang.title)

        learner_editurl = '%s/001/edit' % self.classlist1.absolute_url()
        test = json.dumps({'learner_id'      : '001',
                           'learner_code'    : '001',
                           'learner_name'    : 'James',
                           'learner_editurl' : learner_editurl,
                           'learner_gender'  : 'Male',
                           'learner_lang'    : lang.title,
                           'status' : 'info',
                           'msg'    : "New learner added"})

        self.assertEqual(len(self.classlist1.getFolderContents()),3)
        self.assertEqual(view(),test)
        self.assertEqual(len(self.classlist1.getFolderContents()),4)

        #try to add the same object again
        self.request.set('learner_code','001')
        self.request.set('learner_name','James')
        self.request.set('learner_gender','Male')
        self.request.set('learner_lang_id',lang.value)
        self.request.set('learner_lang',lang.title)
 
        test2 = json.dumps({'status' : 'error',
                           'msg'    : "Student code not unique"})

        self.assertEqual(view(),test2)
        self.assertEqual(len(self.classlist1.getFolderContents()),4)

