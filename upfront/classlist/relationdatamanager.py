from zope.component import adapts, getUtility
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from z3c.relationfield.interfaces import (
    IRelation,
    IRelationValue,
    )
from z3c.relationfield.relation import RelationValue

from z3c.form.datamanager import AttributeField

class RelationDataManager(AttributeField):
    """ A datamanager that convert UIDs to objects
    """

    adapts(Interface, IRelation)

    def get(self):
        """Gets the target"""
        rel = None
        try:
            rel = super(RelationDataManager, self).get()
        except AttributeError:
            # Not set yet
            pass
        if rel is not None:
            if rel.isBroken():
                # XXX: should log or take action here
                return
            return rel.to_id

    def set(self, value):
        """Sets the relationship target"""
        if value is None:
            return super(RelationDataManager, self).set(None)

        current = None
        try:
            current = super(RelationDataManager, self).get()
        except AttributeError:
            pass
        to_id = value
        if IRelationValue.providedBy(current):
            # If we already have a relation, just set the to_id
            current.to_id = to_id
        else:
            # otherwise create a relationship
            rel = RelationValue(to_id)
            super(RelationDataManager, self).set(rel)


