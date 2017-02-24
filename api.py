from flask import Flask, Blueprint, request, jsonify, make_response
from models import User, UsersSchema, db, UrlSchema, LinkSchema
from flask_restful import Resource, Api
from marshmallow import ValidationError
from app import app


# app = Flask(__name__)
api = Api(app)


class UsersList(Resource):
    def get(self):
        users_query = User.query.all()
        results = schema.dump(users_query, many=True).data
        return results
    
    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            schema.validate(raw_dict)
            user_dict = raw_dict['data']['attributes']
            user = User(user_dict['email'], user_dict['name'],user_dict['is_active'])
            user.add(user)            
            query = User.query.get(user.id)
            results = schema.dump(query).data                
            return results, 201
        
        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp               
                
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

class UsersUpdate(Resource):
    def get(self, id):
        user_query = User.query.get_or_404(id)
        result = schema.dump(user_query).data
        return result

    def patch(self, id):
        user = User.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        
        try:
            schema.validate(raw_dict)
            user_dict = raw_dict['data']['attributes']
            for key, value in user_dict.items():
                
                setattr(user, key, value)
          
            user.update()            
            return self.get(id)
            
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp               
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp

    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            delete = user.delete(user)
            response = make_response()
            response.status_code = 204
            return response
            
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp


class HelloWorld(Resource):
    def get(self):
        return {'helo': 'world'}
        

# api.add_resource(UsersList, '/.json')
api.add_resource(UsersUpdate, '/<int:id>.json')
api.add_resource(HelloWorld, '/')



# class CreateUser(Resource):
#     def post(self):
#         return {'status': 'success'}

# api.add_resource(CreateUser, '/')
api.add_resource(UsersList, '/users')

if __name__=='__main__':
    app.run(debug=True) 