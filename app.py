from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Datos en memoria
users = [
    {"id": 1, "nombre": "Juan", "apellido": "Perez", "rol": "admin"},
    {"id": 2, "nombre": "Ana", "apellido": "Garcia", "rol": "user"},
]

parser = reqparse.RequestParser()
parser.add_argument("nombre", required=True, help="nombre requerido")
parser.add_argument("apellido", required=True, help="apellido requerido")
parser.add_argument("rol", required=True, help="rol requerido")


class UserList(Resource):
    def get(self):
        return users, 200

    def post(self):
        args = parser.parse_args()
        new_id = max(u["id"] for u in users) + 1 if users else 1
        user = {
            "id": new_id,
            "nombre": args["nombre"],
            "apellido": args["apellido"],
            "rol": args["rol"],
        }
        users.append(user)
        return user, 201


class User(Resource):
    def get(self, user_id):
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return {"error": "Usuario no encontrado"}, 404
        return user, 200

    def put(self, user_id):
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return {"error": "Usuario no encontrado"}, 404
        args = parser.parse_args()
        user.update(args)
        return user, 200

    def delete(self, user_id):
        global users
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return {"error": "Usuario no encontrado"}, 404
        users = [u for u in users if u["id"] != user_id]
        return {"deleted": user}, 200


class Health(Resource):
    def get(self):
        return {"status": "ok"}, 200


api.add_resource(Health, "/health")
api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:user_id>")