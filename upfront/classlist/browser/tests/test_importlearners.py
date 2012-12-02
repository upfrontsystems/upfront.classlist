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
