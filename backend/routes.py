from flask_restful import Api, Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache
from models import db, User, StudentProfile, CompanyProfile, PlacementDrive, Application


cache = Cache()
api = Api()


class UserRegistration(Resource):

    def post(self):
        data = request.get_json()
        role = data['role']
        if not data or 'email' not in data or 'password_hash' not in data or 'role' not in data or not data['email'] or not data['password_hash'] or not data['role']:
            return {'message' : 'email/password/role is required to register'}, 400
        
        user = User.query.filter_by(email=data['email']).first()

        if user:
            return {'message': 'user already registered!'}, 409
        
        new_user = User(email=data['email'], password_hash=data['password_hash'], role=data['role'])
        
        db.session.add(new_user)
        db.session.flush()

        if role=="student":
            if 'full_name' not in data or 'branch' not in data or 'cgpa' not in data or 'year' not in data or 'phone' not in data or 'resume_path' not in data or not data['full_name'] or not data['cgpa'] or not data['year'] or not data ['resume_path'] or not data['phone'] or not data['branch']:
                return {'message': "Incomplete data!"}, 400
            
            student_profile = StudentProfile(user_id=new_user.id, full_name=data['full_name'], cgpa=data['cgpa'], year=data['year'], branch=data['branch'], phone=data['phone'], resume_path=data['resume_path'])
            db.session.add(student_profile)

        elif role=="company":
            if 'company_name' not in data or 'hr_contact' not in data or 'website' not in data or 'description' not in data or not data['company_name'] or not data['hr_contact'] or not data['website'] or not data ['description']:
                return {'message': "Incomplete Data!"}, 400
            
            company_profile = CompanyProfile(user_id=new_user.id, company_name=data['company_name'], hr_contact=data['hr_contact'], website=data['website'], description=data['description'])
            db.session.add(company_profile)

        else:
            return {'message': 'invalid role'}, 400

        db.session.commit()
        return {'message': 'user registered sucessfully!'}, 201

api.add_resource(UserRegistration, '/')


class UserLogin(Resource):

    def post(self):
        data = request.get_json()

        if not data or 'email' not in data or 'password_hash' not in data or not data['email'] or not data['password_hash']:
            return {'message' : 'email and password is required!'}, 400
        
        user = User.query.filter_by(email=data['email'], password_hash=data['password_hash']).first()

        if not user:
            return {'message': 'invalid credentials!'}, 401
        
        token = create_access_token(identity=user.email)

        return {'message': 'Login successful!', 'token': token}, 200

api.add_resource(UserLogin, '/login')