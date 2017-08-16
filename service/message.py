from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource, request

from conf.config import CASSANDRA_HOSTS, USER_KEYSPACE
from model.audience import Audience
from model.message import MessageByReceiver, MessageBySender


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

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=USER_KEYSPACE)

        for receiver_id in receiver_ids:
            MessageByReceiver.create(
                receiver_id=receiver_id,
                sender_id=sender_id,
                audience=audience,
                message=message,
                asset_name=asset_name,
            )

            MessageBySender.create(
                receiver_id=receiver_id,
                sender_id=sender_id,
                audience=audience,
                message=message,
                asset_name=asset_name,
            )

        return {
            "success": True
        }

    def _get_friends(self, sender_id):
        # return list of friends
        return []
