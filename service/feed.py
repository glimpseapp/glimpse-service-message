import json

import requests
from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource, request

from conf.config import CASSANDRA_HOSTS, MESSAGE_KEYSPACE
from conf.service import IMAGES_URL_BULK_URL
from model.message import MessageByReceiver


class Feed(Resource):
    def post(self):

        data = request.get_json(silent=True)

        if not data.get('user_id'):
            return make_response("Missing field user_id", 500)

        user_id = data.get('user_id')

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=MESSAGE_KEYSPACE)

        feed_result = MessageByReceiver.filter(receiver_id=user_id)
        feeds = []
        asset_names = []

        for feed in feed_result:
            feed_object = feed.to_object()
            feeds.append(feed_object)

            asset_names.append(feed_object.get('asset_name'))

        images_url = self._get_images_url(asset_names)

        feed_response = []
        for feed in feeds:
            feed['asset_url'] = images_url.get(feed.get("asset_name")).get("image_url")
            feed_response.append(feed)

        return {
            "tot": len(feed_result),
            "feed": feed_response
        }

    @staticmethod
    def _get_images_url(asset_names):
        payload = json.dumps({"images": asset_names})
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        response = requests.post(IMAGES_URL_BULK_URL, data=payload, headers=headers)
        data = response.json()
        return data.get("images")