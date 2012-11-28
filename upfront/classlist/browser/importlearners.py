import json
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
from upfront.classlist.content.classlist import IClassList

grok.templatedir('templates')
class ImportLearnersView(grok.View):
    """ Import Learners from a spreadsheet
    """
    grok.context(IClassList)
    grok.name('import-learners')
    grok.template('importlearners')
    grok.require('zope2.View')

