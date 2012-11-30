import xlrd

from five import grok
from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from z3c.relationfield import RelationValue
from z3c.form.i18n import MessageFactory as _

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName

from upfront.classlist.vocabs import availableLanguages
from upfront.classlist.vocabs import GENDER

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
       
        # Redirect to the new classlist if nothing went wrong.
        request.RESPONSE.redirect('/'.join(classlist.getPhysicalPath()))
        return True

    def get_validated_classlist_id(self, request):
        """ Checks the request for a classlist name specified via
            new_classlist_id - from a field in the importlearners template
            classlist_id - if upload-classlist-spreadsheet view called directly
            if none of these exist on the request - throw error
        """

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
        """ Opens supplied xls spreadsheet file and does integrity checks
            to make sure that it contains valid data.
        """

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
        """ returns an existing classlist, if a classlist does not exist
            it is created in the correct context (the classlists folder)
        """

        error = None
        pc = getToolByName(self, 'portal_catalog')
        query = {'portal_type': 'upfront.classlist.content.classlist',
                 'Title': classlist_id
                }
        brains = pc(**query)
        if brains is not None and len(brains) > 0:
            return None, brains[0].getObject()
        else:
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

    def add_learners(self, classlist, sheet):
        """ Extracts learners from specified xls spreadsheet and adds
            them to a classlist. Performs several checks to insure data
            integrity.
        """

        errors = []
        row_count = sheet.nrows
        for row_num in range(0, row_count):
            error = None
            learner = None
            code = sheet.cell(row_num, 0).value

            # if code is a number when imported from excel documents it will be 
            # imported as a float, but we want a string.
            # if code is a contains characters, it should be a string when
            # imported so these checks are not needed.

            if isinstance(code, float):
                # get rid of decimals (the .0 part) and convert to string)
                code = str(int(code))
            if isinstance(code, int): 
                # this may never execute but just in case
                code = str(code)

            name = sheet.cell(row_num, 1).value
            gender = sheet.cell(row_num, 2).value
            language = sheet.cell(row_num, 3).value

            error, learner = self.get_learner(classlist, code, name, gender,
                                              language)
            if learner is None:      
                message = _("Could not add learner:") + ' %s' % name
                errors.append(message)
                errors.append(error)
            else:
                if error is not None:
                    errors.append(error)
        
        notify(ObjectModifiedEvent(classlist))

        return errors

    def get_learner(self, classlist, code, name, gender_code, language_code):
        """ Look if the learner exists in the system.
            If we can't find them there, we create a new one and set its
            properties to those specified in the import data.

            Note: At this stage the code will not overwrite existing learners.
                  It just skips them.
            IMPORTANT - This assumes that a learner can only be in one classlist
                        at a time.
        """

        learner = None
        # Now try to find the learner in the system
        # better make sure we search with 'None' or we get false positives
        if code == '': code = None
        query = {'portal_type': 'upfront.classlist.content.learner',
                 'id': code}
        pc = getToolByName(self, 'portal_catalog')
        brains = pc(**query)

        # For the moment we assume there can be only one... 
        learner = len(brains) > 0 and brains[0].getObject() or None
        # We found her, no need to recreate.
        if learner is not None:
            message = _("Skipping existing learner") + ': %s' % name
            return message, learner
        
        # We could not find the learner, so we will create one, but first
        # get our data ducks in a row.

        if gender_code not in self.genders():
            msgid = _(u"learners_gender_not_recognized",
                default=u"Learner: ${name} gender: ${gender} not recognized",
                mapping={ u"name" : name, u"gender" : gender_code})
            msg = self.context.translate(msgid)
            return msg, None
    
        if language_code not in self.languages()[0]:
            msgid = _(u"learners_language_not_recognized",
                default=u"Learner: ${name} gender: ${language} not recognized",
                mapping={ u"name" : name, u"language" : language_code})
            msg = self.context.translate(msgid)
            return msg, None

        # create learner
        classlist.invokeFactory('upfront.classlist.content.learner',
                                code,
                                title=name)
        new_learner = classlist._getOb(code)
        new_learner.code = code
        new_learner.name = name
        new_learner.gender = gender_code       
        # get position of language in language vocab, using index get its 
        # corresponding from initd list
        index = self.languages()[0].index(language_code)
        lang_intid = self.languages()[1][index]        
        new_learner.home_language = RelationValue(lang_intid)
        notify(ObjectModifiedEvent(new_learner))

        return None, new_learner

    def add_portal_errors(self, errors):
        for error in errors:
            msg = _(error)
            IStatusMessage(self.request).addStatusMessage(msg,"error")

    def languages(self):
        """ Return the contents languages dictionary as two lists of strings
            For each language return its string and intid value.
        """

        language_vocab = availableLanguages(self.context).__iter__()
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

        return lang_list, intid_list

    def genders(self):
        """ Return the contents of gender dictionary as a list of strings
            This may seem redundant as it contains 2 entries but is necessary
            to ensure translated versions are correctly checked against.
        """

        gender_vocab = GENDER.__iter__()
        gender_list = []
        notfinished = True;
        while notfinished:            
            try:
                gender = gender_vocab.next()
                gender_list.append(gender.title)
            except StopIteration:
                notfinished = False;

        return gender_list
