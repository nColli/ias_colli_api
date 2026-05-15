from flask import request
from flask_restful import Resource

from .db import get_connection


def parse_user_json():
    data = request.get_json(force=True, silent=True)
    if not data:
        return None, ({"error": "Body JSON requerido"}, 400)
    missing = [f for f in ("nombre", "apellido", "rol") if f not in data]
    if missing:
        return None, ({"error": f"Campos requeridos: {', '.join(missing)}"}, 400)
    return data, None


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
        users = [
            {"id": r[0], "nombre": r[1], "apellido": r[2], "rol": r[3]} for r in rows
        ]
        return users, 200

    def post(self):
        data, err = parse_user_json()
        if err or data is None:
            return err
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (nombre, apellido, rol) VALUES (%s, %s, %s) RETURNING id",
            (data["nombre"], data["apellido"], data["rol"]),
        )
        fetch = cur.fetchone()
        if fetch is None:
            return None
        new_id = fetch[0]
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": new_id,
            "nombre": data["nombre"],
            "apellido": data["apellido"],
            "rol": data["rol"],
        }, 201


class User(Resource):
    def get(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nombre, apellido, rol FROM users WHERE id = %s", (user_id,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return {"error": "Usuario no encontrado en db"}, 404
        return {"id": row[0], "nombre": row[1], "apellido": row[2], "rol": row[3]}, 200

    def put(self, user_id):
        data, err = parse_user_json()
        if err or data is None:
            return err
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return {"error": "Usuario no encontrado"}, 404
        cur.execute(
            "UPDATE users SET nombre=%s, apellido=%s, rol=%s WHERE id=%s",
            (data["nombre"], data["apellido"], data["rol"], user_id),
        )
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": user_id,
            "nombre": data["nombre"],
            "apellido": data["apellido"],
            "rol": data["rol"],
        }, 200

    def delete(self, user_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, nombre, apellido, rol FROM users WHERE id = %s", (user_id,)
        )
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return {"error": "Usuario no encontrado"}, 404
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            "deleted": {
                "id": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "rol": row[3],
            }
        }, 200


def register_routes(api):
    api.add_resource(Health, "/health")
    api.add_resource(UserList, "/users")
    api.add_resource(User, "/users/<int:user_id>")
