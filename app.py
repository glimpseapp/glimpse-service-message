#!flask/bin/python
from flask import Flask
from flask_restful import Api

from conf.config import HTTP_HOST, HTTP_PORT
from service.feed import Feed
from service.healthz import Healthz
from service.message import Message

app = Flask(__name__)
api = Api(app)

api.add_resource(Healthz, '/healthz')
api.add_resource(Feed, '/feed')
api.add_resource(Message, '/message')

if __name__ == '__main__':
    app.run(host=HTTP_HOST, port=HTTP_PORT)
