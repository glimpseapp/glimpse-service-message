from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource, request

from conf.config import CASSANDRA_HOSTS, USER_KEYSPACE
from model.message import MessageByReceiver


class Feed(Resource):
    def post(self):

        data = request.get_json(silent=True)

        if not data.get('user_id'):
            return make_response("Missing field user_id", 500)

        user_id = data.get('user_id')

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=USER_KEYSPACE)

        feed_result = MessageByReceiver.filter(receiver_id=user_id)
        feeds = []

        for feed in feed_result:
            feeds.append(feed.to_object())

        return {
            "tot": feed_result.count(),
            "feed": feeds
        }
