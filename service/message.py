import json

from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource, request

from conf.config import CASSANDRA_HOSTS, MESSAGE_KEYSPACE, MESSAGE_SENT_TOPIC
from model.audience import Audience
from model.message import MessageByReceiver, MessageBySender

from google.cloud import pubsub


class Message(Resource):
    def post(self):

        data = request.get_json(silent=True)

        sender_id = data.get('user_id')
        audience = data.get('audience', Audience.DIRECT)
        receiver_id = data.get('receiver_id', [])
        asset = data.get('asset', {})
        message = data.get('message')

        if not sender_id:
            return make_response("Missing field user_id", 500)

        if not audience:
            response_message = "Must specify the audience. Audience can be: " + Audience.DIRECT + ", " \
                               + Audience.FRIENDS + ", " + Audience.PUBLIC
            return make_response(response_message, 500)

        if audience == Audience.DIRECT:
            receiver_ids = [receiver_id]

        if audience == Audience.FRIENDS:
            receiver_ids = self._get_friends(sender_id)

        if asset and (not asset.get('asset_name')):
            return make_response("Must specify asset.asset_name", 500)

        asset_name = asset.get('asset_name')
        # public not implemented yet

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=MESSAGE_KEYSPACE)

        for receiver_id in receiver_ids:
            MessageByReceiver.create(
                receiver_id=receiver_id,
                sender_id=sender_id,
                audience=audience,
                message=message,
                asset_name=asset_name
            )
            MessageBySender.create(
                receiver_id=receiver_id,
                sender_id=sender_id,
                audience=audience,
                message=message,
                asset_name=asset_name
            )

            message_object = {
                "receiver_id": receiver_id,
                "sender_id": sender_id,
                "audience": audience,
                "message": message,
                "asset_name": asset_name
            }
            self._message_sent(message_object)

        return {
            "success": True
        }

    def _get_friends(self, sender_id):
        # return list of friends
        return []

    @staticmethod
    def _message_sent(message):
        client = pubsub.Client()
        topic = client.topic(MESSAGE_SENT_TOPIC)

        messageGrammar = {
            "verb": "message-sent",
            "subject": "message",
            "directObject": message
        }

        topic.publish(json.dumps(messageGrammar))
        return message
