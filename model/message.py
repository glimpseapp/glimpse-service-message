import time
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.util import datetime_from_timestamp


def date_now():
    return datetime_from_timestamp(time.time())


class MessageBySender(Model):
    sender_id = columns.Text(primary_key=True)
    time = columns.DateTime(default=date_now)  # rename to creation_date

    receiver_id = columns.Text()
    message = columns.Text()
    audience = columns.Text()

    asset_name = columns.Text()

    def to_object(self):
        return {
            'sender_id': str(self.sender_id),
            'receiver_id': str(self.receiver_id),
            'time': self.time.isoformat(),
            'message': self.message,
            'audience': self.audience,
            'asset_name': self.asset_name,
        }


class MessageByReceiver(Model):

    receiver_id = columns.Text(primary_key=True)
    time = columns.DateTime(default=date_now)  # rename to creation_date

    sender_id = columns.Text()
    message = columns.Text()
    audience = columns.Text()

    asset_name = columns.Text()

    def to_object(self):
        return {
            'sender_id': str(self.sender_id),
            'receiver_id': str(self.receiver_id),
            'time': self.time.isoformat(),
            'message': self.message,
            'audience': self.audience,
            'asset_name': self.asset_name,
        }

