from flask_restful import Resource, reqparse
from .db import get_connection

parser = reqparse.RequestParser()
parser.add_argument("nombre", required=True, help="nombre requerido")
parser.add_argument("apellido", required=True, help="apellido requerido")
parser.add_argument("rol", required=True, help="rol requerido")


class Health(Resource):
    def get(self):
        return {"status": "ok"}, 200


class UserList(Resource):
    def get(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, apellido, rol FROM users")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        users = [{"id": r[0], "nombre": r[1], "apellido": r[2], "rol": r[3]} for r in rows]
        return users, 200

    def post(self):
        args = parser.parse_args()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (nombre, apellido, rol) VALUES (%s, %s, %s) RETURNING id",
            (args["nombre"], args["apellido"], args["rol"])
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"id": new_id, "nombre": args["nombre"], "apellido": args["apellido"], "rol": args["rol"]}, 201


class User(Resource):
    def get(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, apellido, rol FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return {"error": "Usuario no encontrado"}, 404
        return {"id": row[0], "nombre": row[1], "apellido": row[2], "rol": row[3]}, 200

    def put(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return {"error": "Usuario no encontrado"}, 404
        args = parser.parse_args()
        cur.execute(
            "UPDATE users SET nombre=%s, apellido=%s, rol=%s WHERE id=%s",
            (args["nombre"], args["apellido"], args["rol"], user_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"id": user_id, "nombre": args["nombre"], "apellido": args["apellido"], "rol": args["rol"]}, 200

    def delete(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, apellido, rol FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return {"error": "Usuario no encontrado"}, 404
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {"deleted": {"id": row[0], "nombre": row[1], "apellido": row[2], "rol": row[3]}}, 200


def register_routes(api):
    api.add_resource(Health, "/health")
    api.add_resource(UserList, "/users")
    api.add_resource(User, "/users/<int:user_id>")