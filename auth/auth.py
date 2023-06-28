# ======= Flask imports ===========
from flask import Flask, request, jsonify
from flask import Blueprint
# ======= File imports ===========
from db import data_base
from auth.auth_db import AuthDb

auth = Blueprint('auth', __name__)

authDbObj = AuthDb()
dataBaseObj = data_base() 

@auth.route('/login', methods=["POST"])
def login():
    try:
        req = request.get_json()
        userId, passwd = req["username"], req["password"]
        # === check if user & passwd match
        res = authDbObj.checkUserValidity(userId, passwd)
        if res == False:
            return jsonify({"msg": "Username/Password is incorrect"}), 400
        else:
            # === return user_id
            query = f"select user_id from users where username =  '{userId}'"
            res = dataBaseObj.selectQuery(query, True)
            if res is not None:
                return jsonify({"msg": "success", "id": res[0]}), 200
            else:
                return jsonify({"msg": "Something went wrong"}), 400
    except Exception as e:
        print(e)
        return jsonify({"msg": "Something went wrong"}), 500


@auth.route('/signup', methods=["POST"])
def singup():
    try:
        req = request.get_json()
        username, passwd = req["username"], req["password"]
        # === check if user
        res = authDbObj.getUsers(username)
        if res:
            return jsonify({"msg": "Username already exists"}), 400
        else:
            res = authDbObj.insertUser(username, str(passwd))
            return jsonify({"msg": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": "Something went wrong"}), 500
