import csv
import xlrd
from os import close, write, system

from five import grok
from zope.app.container.interfaces import INameChooser
from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from z3c.relationfield import RelationValue
from z3c.form.i18n import MessageFactory as _

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName

from upfront.classlist.vocabs import availableLanguages


grok.templatedir('templates')
class ImportLearnersView(grok.View):
    """ Provide view/template to Import Learners from a spreadsheet
    """
    grok.context(Interface)
    grok.name('import-learners')
    grok.template('importlearners')
    grok.require('zope2.View')

    def languages(self):
        """ Return the contents languages dictionary as a list of strings
        """

        language_vocab = availableLanguages(self.context).__iter__()
        lang_list = []
        notfinished = True;
        while notfinished:            
            try:
                lang = language_vocab.next()
                lang_list.append(lang.title)
            except StopIteration:
                notfinished = False;

        return lang_list


class UploadClassListSpreadsheetView(grok.View):
    """ Provide functionality to Import Learners from a spreadsheet
    """
    grok.context(Interface)
    grok.name('upload-classlist-spreadsheet')
    grok.require('zope2.View')

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

    def __call__(self):
        """ Upload the supplied spreadsheet. Get all the learners from
            it and add them to the supplied class list (new or existing).
        """

        errors = []
        request = self.request
        import_view_url = '%s/@@import-learners' % self.context.absolute_url()
        
        # Make sure we have valid class list data (name, grade, etc.)
        error, classlist_id = self.get_validated_classlist_id(request)
        error and errors.append(error)
        
        # Make sure we have valid learner data in the uploaded file.
        error, sheet = self.get_validated_learner_data(request)
        error and errors.append(error)
        
        # If any of the above failed we cannot continue.
        if len(errors) > 0:
            self.add_portal_errors(errors)
            request.RESPONSE.redirect(import_view_url)
            return False
        
        # Get the classlist; new or old.
        error, classlist = self.get_classlist(classlist_id, request)
        if classlist is None:
            errors.append(error)
            self.add_portal_errors(errors)
            request.RESPONSE.redirect(import_view_url)
            return False
       
        # Add the learners from the sheet to the classlist
        # At this stage if there are errors, we report on it, but we
        # don't stop the process.
        learner_errors = self.add_learners(classlist, sheet)
        if learner_errors is not None:
            errors.extend(learner_errors)
            self.add_portal_errors(errors)

        if len(errors) > 0:
            self.add_portal_errors(errors)

        IStatusMessage(self.request).addStatusMessage("DEBUG: GOOD","info")
        request.RESPONSE.redirect(import_view_url)
        
        # Redirect to the new classlist if nothing went wrong.
        request.RESPONSE.redirect('/'.join(classlist.getPhysicalPath()))
        return True

    def get_validated_classlist_id(self, request):
        """ XXX Add description """

        new_classlist_id = request.get('new_classlist_id', None)
        if new_classlist_id is not None and len(new_classlist_id) > 0:
            return None, new_classlist_id
        else:
            classlist_uid = request.get('classlist_uid' , None)
            if classlist_uid is None:
                return _("Please indicate which class to use."), None
            else:
                return None, classlist_uid

    def get_validated_learner_data(self, request):
        """ XXX Add description """

        # Get the spreadsheet from the form.
        xl_file = request.get('csv_file', None)
        contents = xl_file.read()
        xl_file.close()
        if contents is None or len(contents) < 1:
            return _("Please supply a valid file."), None 
        
        # Get the spreadsheet
        book = xlrd.open_workbook(file_contents=contents)

        # If we don't have a worksheet, we cannot continue.
        if book.sheets() < 1:
            return _("Please supply at least one work sheet."), None

        sheet = book.sheet_by_index(0)
        # We must have at least one learner.
        if sheet.nrows < 1:
            return _("Please supply at least one learner."), None
        # We must have at least number and name for the new learner.
        if sheet.ncols < 4:
            return _("Please supply a number, name, gender and language."), None
        return None, sheet

    def get_classlist(self, classlist_id, request):
        """ XXX Add Description """

        error = None
        pc = getToolByName(self, 'portal_catalog')
        query = {'portal_type': 'upfront.classlist.content.classlist',
                 'Title': classlist_id
                }
        brains = pc(**query)
        if brains is not None and len(brains) > 0:
            return None, brains[0].getObject()
        else:
            import pdb; pdb.set_trace()

            # get the context of classlists folder.
            context = self.context
            while context.portal_type != 'Folder':
                context = context.aq_parent

            # this should hopefully never be called
            if context.id != 'classlists':
                return _("import-learners called from incorrect context"), None

            # create new classlist in classlists folder.
            context.invokeFactory('upfront.classlist.content.classlist',
                                  classlist_id,
                                  title=classlist_id)
            classlist = context._getOb(classlist_id)

            return error, classlist

    def add_portal_errors(self, errors):
        for error in errors:
            msg = _(error)
            IStatusMessage(self.request).addStatusMessage(msg,"error")


    def add_learners(self, classlist, sheet):
        """ XXX Add Description """

        errors = []
        learners = []
        row_count = sheet.nrows
        for row_num in range(0, row_count):
            error = None
            learner = None
            code = sheet.cell(row_num, 0).value
            name = sheet.cell(row_num, 1).value
            gender = sheet.cell(row_num, 2).value
            language = sheet.cell(row_num, 3).value
            error, learner = self.get_learner(classlist, code, name, gender,
                                              language)
            if learner is None:                
                errors.append('Could not add learner %s' % name) # XXX add i18n
                errors.append(error)
            else:
                learners.append(learner)
        
#        classlist.setLearners(learners)
        notify(ObjectModifiedEvent(classlist))

        return errors


    def get_learner(self, classlist, code, name, gender_code, language_code):
        """ First try to get the learner off the current class list.
            Then look for the learner in the 'learners' folder.
            If we can't find them there, we create a new one and set its
            properties to those specified in the import data.

            Note: At this stage the code will not overwrite existing learners.
                  It just skips them.
        """

        return "DEBUG: not yet implemented", None


