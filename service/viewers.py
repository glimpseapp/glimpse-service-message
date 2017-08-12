from flask_restful import Resource


class Viewers(Resource):
    def get(self):
        return {"status": True}
