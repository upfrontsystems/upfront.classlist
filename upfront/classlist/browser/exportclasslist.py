from csv import DictWriter
from cStringIO import StringIO
from DateTime import DateTime

from five import grok
from z3c.form.i18n import MessageFactory as _

from Products.statusmessages.interfaces import IStatusMessage

from upfront.classlist.content.classlist import IClassList

grok.templatedir('templates')
class ExportClassListView(grok.View):
    """ Export all learners from a classlist into a CSV file, do nothing if the
        class is empty.
    """
    grok.context(IClassList)
    grok.name('export-classlist')
    grok.template('exportclasslist')
    grok.require('zope2.View')

    def __call__(self):
        """ Export all learners from a classlist into a CSV file, do nothing if 
            the class is empty.
        """

        csv_content = None
        # It is safe to do this at the moment, because the view is bound
        # to IClasslist.
        contentFilter = {'portal_type': 'upfront.classlist.content.learner'}
        learners = self.context.getFolderContents(contentFilter,
                                                  full_objects=True)
        learner_csv = StringIO()

        if learners is not None and len(learners) > 0:
            writer = DictWriter(learner_csv,
                                fieldnames=['code', 'name', 'gender',
                                            'language'],
                                restval='',
                                extrasaction='ignore',
                                dialect='excel'
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
            nice_filename = '%s_%s' % ('classlist_', now.strftime('%Y%m%d'))

            self.request.response.setHeader("Content-Disposition",
                                            "attachment; filename=%s.csv" % 
                                             nice_filename)
            self.request.response.setHeader("Content-Type", "text/csv")
            self.request.response.setHeader("Content-Length", len(csv_content))
            self.request.response.setHeader('Last-Modified',
                                            DateTime.rfc822(DateTime()))
            self.request.response.setHeader("Cache-Control", "no-store")
            self.request.response.setHeader("Pragma", "no-cache")

            self.request.response.write(csv_content)
        else:
            msg = _('The class list has no learners.')
            IStatusMessage(self.request).addStatusMessage(msg,"info")

        self.request.response.redirect(
                '/'.join(self.context.getPhysicalPath()))

        return csv_content

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
