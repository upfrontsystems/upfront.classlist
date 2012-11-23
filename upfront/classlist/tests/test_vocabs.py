from base import UpfrontClassListTestBase

from upfront.classlist.vocabs import availableLanguages

class TestClassList(UpfrontClassListTestBase):
    """ Basic methods to test vocabs """

    def test_availableLanguages(self):
        self.assertEqual(len(availableLanguages(self.portal)), 3)
        language = availableLanguages(self.portal).__iter__()
        self.assertEqual(language.next().title,'Afrikaans')
        self.assertEqual(language.next().title,'English')
        self.assertEqual(language.next().title,'Xhosa')
