from upfront.classlist.tests.base import UpfrontClassListTestBase
from z3c.form.i18n import MessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage

class TestExportClassListView(UpfrontClassListTestBase):

    """ Test ExportClassListView view """

    def test__call__(self):

        view = self.classlist2.restrictedTraverse('@@export-classlist')
        # Classlist with no learners
        # export nothing - test for message
        test_out = view()
        self.assertEqual(test_out,None)
        test = IStatusMessage(self.request).show()
        self.assertEqual(test[0].type,'info')
        self.assertEqual(test[0].message,'The class list has no learners.')

        # classlist that has learners
        # test for contents of csv file in the response
        view = self.classlist1.restrictedTraverse('@@export-classlist')

        test_out = view()
        csv_ref = 'learner1,John,Male,Afrikaans\r\n' +\
                  'learner2,Jennie,Female,English\r\n' +\
                  'learner3,Nomsa,Female,Xhosa\r\n'

        self.assertEqual(test_out,csv_ref)
        ct = self.request.response.getHeader("Content-Type")
        self.assertEqual(ct,"text/csv")
