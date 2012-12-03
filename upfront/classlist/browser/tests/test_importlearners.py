import xlrd
from upfront.classlist.tests.base import UpfrontClassListTestBase
from upfront.classlist.vocabs import availableLanguages
from upfront.classlist.vocabs import GENDER

from Products.statusmessages.interfaces import IStatusMessage

class TestImportLearnersView(UpfrontClassListTestBase):
    """ Test methods in import-learners view """
    
    def test_languages(self):
        view = self.classlist1.restrictedTraverse('@@import-learners')
        language_vocab = availableLanguages(self.classlist1).__iter__()
        lang_list = []
        notfinished = True;
        while notfinished:            
            try:
                lang = language_vocab.next()
                lang_list.append(lang.title)
            except StopIteration:
                notfinished = False;
        self.assertEqual(view.languages(),lang_list)


class TestUploadClassListSpreadsheetView(UpfrontClassListTestBase):
    """ Test UploadClassListSpreadsheet view """

    def test__call__(self):
        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')



    def test_get_validated_classlist_id(self):

        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')

        test_out = view.get_validated_classlist_id(self.request)
        self.assertEqual(test_out[0],'Please indicate which class to use.')
        self.assertEqual(test_out[1],None)

        self.request.set('classlist_uid','classlist1')
        test_out = view.get_validated_classlist_id(self.request)
        self.assertEqual(test_out[0],None)
        self.assertEqual(test_out[1],'classlist1')
        
        self.request.set('new_classlist_id','classlist1')
        test_out = view.get_validated_classlist_id(self.request)
        self.assertEqual(test_out[0],None)
        self.assertEqual(test_out[1],'classlist1')

    def test_get_validated_learner_data(self):
        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')


    def test_get_classlist(self):
        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')


    def test_add_learners(self):
        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')



    def test_get_learner(self):

        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')

        #learner exists
        test_out = view.get_learner(self.classlist1, 'learner1', 'Name', 'Male',
                                    'English')        
        self.assertEqual(test_out[0],u'Skipping existing learner: Name')
        self.assertEqual(test_out[1],self.learner1)

        #gender code bad
        test_out = view.get_learner(self.classlist1, 'learner4', 'Name', 'Mal',
                                    'English')        
        self.assertEqual(test_out[0],
                         u'Learner: Name gender: Mal not recognized')
        self.assertEqual(test_out[1],None)

        #language code bad
        test_out = view.get_learner(self.classlist1, 'learner4', 'Name', 'Male',
                                    'nglish')        
        self.assertEqual(test_out[0],
                         u'Learner: Name language: nglish not recognized')
        self.assertEqual(test_out[1],None)

        #create learner
        self.assertEqual(len(self.classlist1.getFolderContents()),3)        
        test_out = view.get_learner(self.classlist1, 'learner4', 
                                    'Name', 'Male', 'English')
        self.assertEqual(len(self.classlist1.getFolderContents()),4)
        self.assertEqual(test_out[0],None)
        self.assertEqual(test_out[1],self.classlist1._getOb('learner4'))

    def test_add_portal_errors(self):

        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')
        errors = ['Error1', 'Error2']
        view.add_portal_errors(errors)
        test = IStatusMessage(self.request).show()
        self.assertEqual(test[0].type,'error')
        self.assertEqual(test[0].message,errors[0])
        self.assertEqual(test[1].message,errors[1])

    def test_languages(self):

        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')
        language_vocab = availableLanguages(self.classlist1).__iter__()
        lang_list = []
        intid_list = []
        notfinished = True;
        while notfinished:            
            try:
                lang = language_vocab.next()
                lang_list.append(lang.title)
                intid_list.append(lang.value)
            except StopIteration:
                notfinished = False;
        self.assertEqual(view.languages()[0],lang_list)
        self.assertEqual(view.languages()[1],intid_list)

    def test_genders(self):

        view = self.classlist1.restrictedTraverse('@@upload-classlist-spreadsheet')
        gender_vocab = GENDER.__iter__()
        gender_list = []
        notfinished = True;
        while notfinished:            
            try:
                gender = gender_vocab.next()
                gender_list.append(gender.title)
            except StopIteration:
                notfinished = False;
        self.assertEqual(view.genders(),gender_list)
