from flask_restful import Resource


class View(Resource):
    def get(self):
        return {"status": True}
