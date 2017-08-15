from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource, request

from conf.config import CASSANDRA_HOSTS, USER_KEYSPACE
from model.audience import Audience
from model.message import MessageByReceiver, MessageBySender


class Message(Resource):
    def post(self):

        data = request.get_json(silent=True)

        if not data.get('user_id'):
            return make_response("Missing field user_id", 500)

        if not data.get('audience'):
            return make_response("Must specify the audience", 500)

        sender_id = data.get('user_id')
        audience = data.get('audience', Audience.DIRECT)

        if audience == Audience.DIRECT:
            receiver_ids = [data.get('receiver_id')]

        if audience == Audience.FRIENDS:
            receiver_ids = self._get_friends(sender_id)

        message = data.get('message')

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=USER_KEYSPACE)

        for receiver_id in receiver_ids:
            MessageByReceiver.create(
                receiver_id=receiver_id,
                sender_id=sender_id,
                audience=audience,
                message=message
            )

            MessageBySender.create(
                receiver_id=receiver_id,
                sender_id=sender_id,
                audience=audience,
                message=message
            )

        return {
            "success" : True
        }

    def _get_friends(self, sender_id):
        # return list of friends
        return []