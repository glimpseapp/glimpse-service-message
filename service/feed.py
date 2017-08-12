from flask_restful import Resource


class Feed(Resource):
    def get(self):
        return {"status": True}
