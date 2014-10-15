import xlwt
import csv
from cStringIO import StringIO
from DateTime import DateTime

from five import grok
from Products.statusmessages.interfaces import IStatusMessage

from upfront.classlist import MessageFactory as _
from upfront.classlist.content.classlist import IClassList

class ExportClassListView(grok.View):
    """ Export all learners from a classlist into a CSV file, do nothing if the
        class is empty.
    """
    grok.context(IClassList)
    grok.name('export-classlist-csv')
    grok.require('zope2.View')

    def __call__(self):
        """ Export all learners from a classlist into a CSV file, do nothing if 
            the class is empty.
        """

        csv_content = None
        # It is safe to do this at the moment, because the view is bound
        # to IClasslist.
        contentFilter = {'portal_type': 'upfront.classlist.content.learner'}
        contentFilter['sort_on'] = "id"
        contentFilter['sort_order'] = "ascending"
        learners = self.context.getFolderContents(contentFilter,
                                                  full_objects=True)
        learner_csv = StringIO()

        if learners is not None and len(learners) > 0:
            writer = csv.DictWriter(learner_csv,
                                fieldnames=['code', 'name', 'gender',
                                            'language'],
                                restval='',
                                extrasaction='ignore',
                                dialect='excel',
                                quoting=csv.QUOTE_ALL
                               )

            for learner in learners:
                ldict={'code': learner.id,
                       'name': learner.name,
                       'gender': learner.gender,
                       'language': learner.home_language.to_object.title, 
                      }
                writer.writerow(ldict)
            
            csv_content = learner_csv.getvalue()
            learner_csv.close()

            now = DateTime()
            nice_filename = 'classlist-%s' % self.context.title

            self.request.response.setHeader("Content-Disposition",
                                            "attachment; filename=%s.xls" % 
                                             nice_filename)
            self.request.response.setHeader("Content-Type", "text/csv")
            self.request.response.setHeader("Content-Length", len(csv_content))
            self.request.response.setHeader('Last-Modified',
                                            DateTime.rfc822(DateTime()))
            self.request.response.setHeader("Cache-Control", "no-store")
            self.request.response.setHeader("Pragma", "no-cache")

            self.request.response.write(csv_content)
        else:
            msg = _('The classlist has no learners')
            IStatusMessage(self.request).addStatusMessage(msg,"info")

        self.request.response.redirect(
                '/'.join(self.context.getPhysicalPath()))

        return csv_content

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class ExportClassListXlsView(grok.View):
    """ Export all learners from a classlist into an excel file, do nothing if 
        the class is empty.
    """
    grok.context(IClassList)
    grok.name('export-classlist')
    grok.require('zope2.View')

    def __call__(self):
        """ Export all learners from a classlist into an excel file, do nothing
            if the class is empty.
        """

        csv_content = None
        # It is safe to do this at the moment, because the view is bound
        # to IClasslist.
        contentFilter = {'portal_type': 'upfront.classlist.content.learner'}
        contentFilter['sort_on'] = "id"
        contentFilter['sort_order'] = "ascending"
        learners = self.context.getFolderContents(contentFilter,
                                                  full_objects=True)
        learner_csv = StringIO()

        ezxf = xlwt.easyxf
        headings = ['Code', 'Name', 'Gender', 'Language']
        kinds =     'text    text    text      text'.split()
        if learners is not None and len(learners) > 0:

            data = []
            for learner in learners:
                data.append([learner.id, 
                             learner.name, 
                             learner.gender,
                             learner.home_language.to_object.title]
                    )

            heading_xf = ezxf('font: bold on; align: wrap on, '
                              'vert centre, horiz center')
            kind_to_xf_map = {
                'text': ezxf(),
                # other examples
                # 'date': ezxf(num_format_str='yyyy-mm-dd'),
                #'int': ezxf(num_format_str='#,##0'),
                #'money': ezxf('font: italic on; pattern: pattern solid,
                #     fore-colour grey25',
                #    num_format_str='$#,##0.00'),
                #'price': ezxf(num_format_str='#0.000000'),
                }
            data_xfs = [kind_to_xf_map[k] for k in kinds]

            book = xlwt.Workbook()
            sheet = book.add_sheet(self.context.title) # XXX make sure it is utf sanitized
            rowx = 0
            for colx, value in enumerate(headings):
                sheet.write(rowx, colx, value, heading_xf)
            sheet.set_panes_frozen(True) # frozen headings instead of 
                                         # split panes
            sheet.set_horz_split_pos(rowx+1) # in general, freeze after last 
                                             # heading row
            sheet.set_remove_splits(True) # if user does unfreeze, don't leave 
                                          # a split there
            for row in data:
                rowx += 1
                for colx, value in enumerate(row):
                    sheet.write(rowx, colx, value, data_xfs[colx])

            book.save(learner_csv)            
            csv_content = learner_csv.getvalue()
            learner_csv.close()

            now = DateTime()
            nice_filename = 'classlist-%s' % self.context.title

            self.request.response.setHeader("Content-Disposition",
                                            "attachment; filename=%s.xls" % 
                                             nice_filename)
            self.request.response.setHeader("Content-Type", "text/csv")
            self.request.response.setHeader("Content-Length", len(csv_content))
            self.request.response.setHeader('Last-Modified',
                                            DateTime.rfc822(DateTime()))
            self.request.response.setHeader("Cache-Control", "no-store")
            self.request.response.setHeader("Pragma", "no-cache")

            self.request.response.write(csv_content)
        else:
            msg = _('The classlist has no learners')
            IStatusMessage(self.request).addStatusMessage(msg,"info")

        self.request.response.redirect(
                '/'.join(self.context.getPhysicalPath()))

        return csv_content

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
