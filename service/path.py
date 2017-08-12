from flask_restful import Resource


class Path(Resource):
    def get(self):
        return {"status": True}
