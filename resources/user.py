from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from datetime import datetime
from blocklist import ACCESS_EXPIRES, REFRESH_EXPIRES, jwt_redis_blocklist
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
  @blp.arguments(UserSchema)
  def post(self, user_data):
      if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        
      user = UserModel(
          username=user_data["username"],
          password=pbkdf2_sha256.hash(user_data["password"]),
      )
      db.session.add(user)
      db.session.commit()

      return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
  @blp.arguments(UserSchema)
  def post(self, user_data):
    user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
    
    if user and pbkdf2_sha256.verify(user_data["password"], user.password):
      access_token = create_access_token(identity=user.id, fresh=True)
      refresh_token = create_refresh_token(identity=user.id)
      return {"user_id": user.id, "access_token": access_token, "refresh_token": refresh_token,"message": "Successfully logged in."}
    abort(401, message="Invalid credentials.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
  @jwt_required()
  def post(self):
    current_token = get_jwt()
    current_expDate = datetime.utcfromtimestamp(current_token['exp'])
    current_timeNow = datetime.utcnow()
    if current_expDate > current_timeNow:
      return {"message": "Access token is not expired yet"}, 200
    else:
      current_user = get_jwt_identity()
      new_token = create_access_token(identity=current_user, fresh=False)
      jti = get_jwt()["jti"]
      jwt_redis_blocklist.set(jti, "", ex=REFRESH_EXPIRES)
      return {"message": "Successfully refreshed token.", "access_token": new_token}, 200

@blp.route("/logout")
class UserLogout(MethodView):
  @jwt_required(verify_type=False)
  def delete(self):
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return {"message": "Successfully logged out."}

@blp.route("/user/<int:user_id>")
class User(MethodView):
  @blp.response(200, UserSchema)
  def get(self, user_id):
    user = UserModel.query.get_or_404(user_id)
    return user

  def delete(self, user_id):
    user = UserModel.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted."}, 200