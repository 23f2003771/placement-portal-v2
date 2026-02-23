from flask_restful import Api, Resource
from flask import app, request
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
        
        user = User.query.filter_by(email=data['email'], password_hash=data['password_hash'], is_active=True).first()

        if not user:
            return {'message': 'invalid credentials!'}, 401

        if user.role == "student":
            login_data = {"id": user.id, "name": user.student_profile.full_name, "email": user.email, "role": user.role, "is_active": user.is_active}
        elif user.role == "company":
            login_data = {"id": user.id, "name": user.company_profile.company_name, "email": user.email, "role": user.role, "is_active": user.is_active}
        elif user.role == "admin":
            login_data = {"email": user.email, "role": user.role}
        else:
            return {'message': 'invalid user role!'}, 400
        
        token = create_access_token(identity=user.email)
        
        return {'message': 'Login successful!', 'token': token, 'login_data': login_data}, 200

api.add_resource(UserLogin, '/login')


class AdminDashboard(Resource):

    @jwt_required()
    def get(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "admin":
            return {"message": "Admin Privlage Required!"}, 403
        
        students = StudentProfile.query.all()
        companies = CompanyProfile.query.all()
        drives = PlacementDrive.query.all()
        applications = Application.query.all()

        students_list = []
        companies_list = []
        applications_list = []
        ongoing_drives = []
        companies_applications = []

        for stu in students:
            students_list.append({"email": stu.user.email, "full_name": stu.full_name, "branch": stu.branch, "year": stu.year, "cgpa": stu.cgpa, "phone": stu.phone, "resume_path": stu.resume_path, "is_blacklisted": stu.is_blacklisted})

        for comp in companies:
            if comp.approval_status == "approved":
                companies_list.append({"email": comp.user.email, "company_name": comp.company_name, "hr_contact": comp.hr_contact, "website": comp.website, "description": comp.description, "approval_status": comp.approval_status, "is_blacklisted": comp.is_blacklisted})
            elif comp.approval_status == "pending":
                companies_applications.append({"email": comp.user.email, "company_name": comp.company_name, "hr_contact": comp.hr_contact, "website": comp.website, "description": comp.description, "approval_status": comp.approval_status, "is_blacklisted": comp.is_blacklisted})

        for drive in drives:
            if drive.status == "ongoing":
                ongoing_drives.append({"drive_name": drive.drive_name, "company_email": drive.company.user.email, "description": drive.description, "deadline": drive.deadline, "is_active": drive.is_active})
        
        for apl in applications:
            applications_list.append({"student_email": apl.student.user.email, "drive_name": apl.drive.drive_name, "applied_at": apl.applied_at, "status": apl.status, "remark": apl.remark})
            
        return {"students": students_list, "companies": companies_list, "drives": ongoing_drives, "applications": applications_list, "company_applications": companies_applications}, 200

    
    @jwt_required()
    def put(self, id):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "admin":
            return {"message": "Admin Privlage Required!"}, 403
        
        data = request.get_json()
        
        target_user = User.query.filter_by(id=id).first()
        drive = PlacementDrive.query.filter_by(id=id).first()
        if not target_user and data["action"] in ["blacklist", "unblacklist"]:
            return {"message": "User not found!"}, 404
        elif not drive and data["action"] == "completed":
            return {"message": "Drive not found!"}, 404
        student_profile = StudentProfile.query.filter_by(user_id=id).first()
        company_profile = CompanyProfile.query.filter_by(user_id=id).first()

        if data['action'] == "completed" and drive:
            drive.status = "completed"
        elif data['action'] == "blacklist" and student_profile:
            student_profile.is_blacklisted = True
            target_user.is_active = False
            for apl in student_profile.applications:
                apl.status = "rejected"
                apl.remark = "Student blacklisted by admin"
        elif data['action'] == "unblacklist" and student_profile:
            student_profile.is_blacklisted = False
            target_user.is_active = True
            for apl in student_profile.applications:
                if apl.status == "rejected" and apl.remark == "Student blacklisted by admin":
                    apl.status = "applied"
                    apl.remark = None
        elif data['action'] == "blacklist" and company_profile:
            company_profile.is_blacklisted = True
            target_user.is_active = False
            for drive in company_profile.drives:
                drive.status = "rejected"
                for apl in drive.applications:
                    apl.status = "rejected"
                    apl.remark = "Company blacklisted by admin"
        elif data['action'] == "unblacklist" and company_profile:
            company_profile.is_blacklisted = False
            target_user.is_active = True
            for drive in company_profile.drives:
                if drive.status == "rejected":
                    drive.status = "pending"
                    for apl in drive.applications:
                        if apl.status == "rejected" and apl.remark == "Company blacklisted by admin":
                            apl.status = "applied"
                            apl.remark = None
        else:
            return {"message": "Invalid action!"}, 400
        
        db.session.commit()
        return {"message": f"User {data['action']}ed successfully!"}, 200

api.add_resource(AdminDashboard, '/admin/dashboard', '/admin/dashboard/<int:id>')


class CompanyDashboard(Resource):
    @jwt_required()
    def get(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "company" or user.company_profile.approval_status != "approved":
            return {"message": "only approved comanies allowed!"}, 403
        
        drives = PlacementDrive.query.filter_by(company_id=user.company_profile.id).all()

        upcoming_drives = []
        closed_drives = []

        for drive in drives:
            if drive.status == "ongoing":
                applications = []
                for apl in drive.applications:
                    applications.append({"id": apl.id, "student_email": apl.student.user.email, "full_name": apl.student.full_name, "branch": apl.student.branch, "year": apl.student.year, "cgpa": apl.student.cgpa, "phone": apl.student.phone, "resume_path": apl.student.resume_path, "status": apl.status})
                upcoming_drives.append({"id": drive.id, "drive_name": drive.drive_name, "job_title": drive.job_title, "description": drive.description, "deadline": drive.application_deadline, "applications": applications})
            elif drive.status == "completed":
                closed_drives.append({"id": drive.id, "drive_name": drive.drive_name, "job_title": drive.job_title, "description": drive.description, "deadline": drive.application_deadline})
        
        return {"upcoming_drives": upcoming_drives, "closed_drives": closed_drives}, 200
    
    
    @jwt_required()
    def post(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "company" or user.company_profile.approval_status != "approved":
            return {"message": "only approved comanies allowed!"}, 403
        
        data = request.get_json()

        if not data or 'drive_name' not in data or 'job_title' not in data or 'description' not in data or 'application_deadline' not in data or 'eligiblility_criteria' not in data or 'interview_type' not in data or not data['drive_name'] or not data['job_title'] or not data['description'] or not data['application_deadline'] or not data['eligiblility_criteria'] or not data['interview_type']:
            return {'message': "Incomplete Data!"}, 400
        
        new_drive = PlacementDrive(company_id=user.company_profile.id, drive_name=data['drive_name'], job_title=data['job_title'], description=data['description'], application_deadline=data['application_deadline'], eligiblility_criteria=data['eligiblility_criteria'], interview_type=data['interview_type'])
        
        db.session.add(new_drive)
        db.session.commit()

        return {"message": "Placement Drive Created Successfully!"}, 201
    

    @jwt_required()
    def put(self, id):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "company" or user.company_profile.approval_status != "approved":
            return {"message": "only approved comanies allowed!"}, 403
        
        application = Application.query.filter_by(id=id).first()

        if not application:
            return {"message": "Application not found!"}, 404
        
        if application.drive.company_id != user.company_profile.id:
            return {"message": "Unauthorized action!"}, 403
        
        data = request.get_json()

        if 'status' not in data or not data['status'] or data['status'] not in ['accepted', 'rejected', 'shortlisted', 'waitlisted']:
            return {"message": "Invalid status!"}, 400
        
        application.status = data['status']
        application.remark = data.get('remark', None)

        db.session.commit()

        return {"message": f"Application {data['status']} successfully!"}, 200
    
api.add_resource(CompanyDashboard, '/company/dashboard', '/company/dashboard/<int:id>')