import os
import csv
from email.mime import application
from flask_restful import Api, Resource
from flask import app, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_caching import Cache
from datetime import datetime
from celery_tasks import csv_report
from models import db, User, StudentProfile, CompanyProfile, PlacementDrive, Application


cache = Cache()
api = Api()

def dashboard_cache_key():
    user_email = get_jwt_identity()
    return f"dashboard:{user_email}"


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
            login_data = {"email": user.email, "role": user.role, "name": "Admin"}
        else:
            return {'message': 'invalid user role!'}, 400
        
        token = create_access_token(identity=user.email)
        
        return {'message': 'Login successful!', 'token': token, 'login_data': login_data}, 200

api.add_resource(UserLogin, '/login')


class AdminDashboard(Resource):

    @jwt_required()
    @cache.cached(timeout=120, key_prefix=dashboard_cache_key)
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
            if not stu.is_blacklisted:
                students_list.append({"id": stu.user.id, "email": stu.user.email, "full_name": stu.full_name, "branch": stu.branch, "year": stu.year, "cgpa": stu.cgpa, "phone": stu.phone, "resume_path": stu.resume_path, "is_blacklisted": stu.is_blacklisted})

        for comp in companies:
            if comp.approval_status == "approved":
                companies_list.append({"id": comp.user.id, "email": comp.user.email, "company_name": comp.company_name, "hr_contact": comp.hr_contact, "website": comp.website, "description": comp.description, "approval_status": comp.approval_status})
            elif comp.approval_status == "pending":
                companies_applications.append({"id": comp.user.id, "email": comp.user.email, "company_name": comp.company_name, "hr_contact": comp.hr_contact, "website": comp.website, "description": comp.description, "approval_status": comp.approval_status})

        for drive in drives:
            if drive.status == "ongoing":
                ongoing_drives.append({"id": drive.id, "drive_name": drive.drive_name, "company_email": drive.company.user.email, "job_title": drive.job_title, "description": drive.job_description, "salary": drive.salary, "location": drive.location})
        
        for apl in applications:
            applications_list.append({"id": apl.id, "name": apl.student.full_name, "department": apl.student.branch, "company_name": apl.drive.company.company_name, "student_email": apl.student.user.email, "drive_name": apl.drive.drive_name, "applied_at": apl.applied_at.isoformat(), "job_title": apl.drive.job_title, "job_description": apl.drive.job_description, "status": apl.status, "remark": apl.remark})
            
        return {"students": students_list, "companies": companies_list, "drives": ongoing_drives, "applications": applications_list, "company_applications": companies_applications}, 200

    
    @jwt_required()
    def put(self, id):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "admin":
            return {"message": "Admin Privlage Required!"}, 403
        
        data = request.get_json() or {}
        action = data.get("action")
        
        target_user = User.query.filter_by(id=id).first()
        drive = PlacementDrive.query.filter_by(id=id).first()
        if action == "blacklist" and not target_user:
            return {"message": "User not found!"}, 404
        elif action in ["completed", "reject_drive"] and not drive:
            return {"message": "Drive not found!"}, 404
        student_profile = StudentProfile.query.filter_by(user_id=id).first()
        company_profile = CompanyProfile.query.filter_by(user_id=id).first()

        if action == "blacklist" and student_profile:
            student_profile.is_blacklisted = True
            target_user.is_active = False
            for apl in student_profile.applications:
                apl.status = "rejected"
                apl.remark = "Student blacklisted by admin"
        elif action == "blacklist" and company_profile:
            company_profile.is_blacklisted = True
            target_user.is_active = False
            company_profile.approval_status = "blacklisted"
            for drive in company_profile.drives:
                drive.status = "rejected"
                for apl in drive.applications:
                    apl.status = "rejected"
                    apl.remark = "Company blacklisted by admin"
        elif action == "approve" and company_profile:
            company_profile.approval_status = "approved"
        elif action == "reject" and company_profile:
            company_profile.approval_status = "rejected"
            company_profile.is_blacklisted = True
            target_user.is_active = False
        elif action == "reject_drive" and drive:
            drive.status = "rejected"
            for apl in drive.applications:
                apl.status = "rejected"
                apl.remark = "Drive rejected by admin"
        elif action == "completed" and drive:
            drive.status = "completed"
            for apl in drive.applications:
                if apl.status != "selected":
                    apl.status = "rejected"
                    apl.remark = "Drive completed by admin"
        else:
            return {"message": "Invalid action!"}, 400
        
        db.session.commit()
        cache.delete(dashboard_cache_key())
        return {"message": "Admin action completed successfully!"}, 200

api.add_resource(AdminDashboard, '/admin/dashboard', '/admin/dashboard/<int:id>')


class CompanyDashboard(Resource):

    @jwt_required()
    @cache.cached(timeout=120, key_prefix=dashboard_cache_key)
    def get(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "company" or not user.company_profile or user.company_profile.approval_status != "approved":
            return {"message": "only approved comanies allowed!"}, 403
        
        drives = PlacementDrive.query.filter_by(company_id=user.company_profile.id).all()

        ongoing_drives = []
        closed_drives = []

        for drive in drives:
            if drive.status == "ongoing":
                applications = []
                for apl in drive.applications:
                    applications.append({"id": apl.id, "student_email": apl.student.user.email, "full_name": apl.student.full_name, "branch": apl.student.branch, "year": apl.student.year, "cgpa": apl.student.cgpa, "phone": apl.student.phone, "resume_path": apl.student.resume_path, "status": apl.status})
                ongoing_drives.append({"id": drive.id, "drive_name": drive.drive_name, "job_title": drive.job_title, "description": drive.job_description, "deadline": drive.application_deadline.isoformat(), "applications": applications, "salary": drive.salary, "location": drive.location})
            elif drive.status == "completed":
                closed_drives.append({"id": drive.id, "drive_name": drive.drive_name, "job_title": drive.job_title, "description": drive.job_description, "deadline": drive.application_deadline.isoformat()})
        
        return {"ongoing_drives": ongoing_drives, "closed_drives": closed_drives}, 200
    
    
    @jwt_required()
    def post(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "company" or not user.company_profile or user.company_profile.approval_status != "approved":
            return {"message": "only approved comanies allowed!"}, 403
        
        data = request.get_json()

        if not data or 'drive_name' not in data or 'job_title' not in data or 'description' not in data or 'application_deadline' not in data or 'eligiblility_criteria' not in data or 'interview_type' not in data or 'salary' not in data or 'location' not in data or not data['drive_name'] or not data['job_title'] or not data['description'] or not data['application_deadline'] or not data['eligiblility_criteria'] or not data['interview_type'] or not data['salary'] or not data['location']:
            return {'message': "Incomplete Data!"}, 400
        
        deadline = datetime.strptime(data['application_deadline'], "%Y-%m-%d")
        
        new_drive = PlacementDrive(company_id=user.company_profile.id, drive_name=data['drive_name'], job_title=data['job_title'], job_description=data['description'], application_deadline=deadline, eligiblility_criteria=data['eligiblility_criteria'], interview_type=data['interview_type'], salary=data['salary'], location=data['location'])
        
        db.session.add(new_drive)
        db.session.commit()
        cache.delete(dashboard_cache_key())

        return {"message": "Placement Drive Created Successfully!"}, 201
    

    @jwt_required()
    def put(self, id):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "company" or not user.company_profile or user.company_profile.approval_status != "approved":
            return {"message": "only approved comanies allowed!"}, 403
        
        data = request.get_json() or {}
        status = data.get("status")

        if status == "completed":
            drive = PlacementDrive.query.get(id)

            if not drive:
                return {"message": "Drive not found!"}, 404

            if drive.company_id != user.company_profile.id:
                return {"message": "Unauthorized action!"}, 403

            drive.status = "completed"

            for apl in drive.applications:
                if apl.status != "selected":
                    apl.status = "rejected"
                    apl.remark = "Drive completed by company"
        else:
            application = Application.query.get(id)

            if not application:
                return {"message": "Application not found!"}, 404

            if application.drive.company_id != user.company_profile.id:
                return {"message": "Unauthorized action!"}, 403

            application.status = status
            application.remark = data.get("remark", None)

        db.session.commit()
        cache.delete(dashboard_cache_key())

        return {"message": f"Status updated to {status} successfully!"}, 200
    
api.add_resource(CompanyDashboard, '/company/dashboard', '/company/dashboard/<int:id>')


class StudentDashboard(Resource):

    @jwt_required()
    @cache.cached(timeout=120, key_prefix=dashboard_cache_key)
    def get(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "student":
            return {"message": "Student Privlage Required!"}, 403
        
        companies = CompanyProfile.query.filter_by(approval_status="approved", is_blacklisted=False).all()
        applications = Application.query.filter_by(student_id=user.student_profile.id).all()

        applied_drives = []
        for apl in applications:
            if apl.status not in ["rejected", "selected"]:
                applied_drives.append({"id": apl.id, "drive_name": apl.drive.drive_name, "company_name": apl.drive.company.company_name, "job_title": apl.drive.job_title, "description": apl.drive.job_description, "application_deadline": apl.drive.application_deadline.isoformat(), "status": apl.status, "remark": apl.remark})
        
        organizations = []
        for comp in companies:
            drives = []
            for drive in comp.drives:
                if drive.status == "ongoing":
                    drives.append({"id": drive.id, "drive_name": drive.drive_name, "job_title": drive.job_title, "description": drive.job_description, "application_deadline": drive.application_deadline.isoformat(), "eligiblility_criteria": drive.eligiblility_criteria, "interview_type": drive.interview_type, "salary": drive.salary, "location": drive.location})
            organizations.append({"id": comp.id, "company_name": comp.company_name, "hr_contact": comp.hr_contact, "website": comp.website, "description": comp.description, "drives": drives})
        
        history = []
        for apl in applications:
            if apl.status in ["rejected", "selected"]:
                history.append({"id": apl.id, "drive_name": apl.drive.drive_name, "company_name": apl.drive.company.company_name, "job_title": apl.drive.job_title, "description": apl.drive.job_description, "interview_type": apl.drive.interview_type, "status": apl.status, "remark": apl.remark})

        return {"applied_drives": applied_drives, "organizations": organizations, "history": history}, 200
    

    @jwt_required()
    def post(self, id):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role != "student":
            return {"message": "Student Privlage Required!"}, 403
        
        drive = PlacementDrive.query.filter_by(id=id, status="ongoing").first()

        if not drive:
            return {"message": "Drive not found or not accepting applications!"}, 404
        
        if drive.company.is_blacklisted:
            return {"message": "Cannot apply to drives of blacklisted companies!"}, 403
        
        existing_application = Application.query.filter_by(student_id=user.student_profile.id, drive_id=drive.id).first()
        if existing_application:
            return {"message": "Already applied to this drive!"}, 409
        
        new_application = Application(student_id=user.student_profile.id, drive_id=drive.id)
        
        db.session.add(new_application)
        db.session.commit()
        cache.delete(dashboard_cache_key())

        return {"message": "Applied to drive successfully!"}, 201
    
api.add_resource(StudentDashboard, '/student/dashboard', '/student/dashboard/<int:id>')


class CSVExport(Resource):

    @jwt_required()
    def post(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if user.role not in ["student", "company"]:
            return {"message": "Unauthorized Access!"}, 403
        
        user = User.query.filter_by(email=get_jwt_identity()).first()

        if not user:
            return {"message": "User not found!"}, 404
        
        os.makedirs("static", exist_ok=True)
        filepath = os.path.join("static", get_jwt_identity().replace("@", "_") + "_report.csv")
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if user.role == "student":
                writer.writerow(["Application ID", "Drive ID", "Drive Name", "Company Name", "Job Title", "Status", "Remark"])
                applications = Application.query.filter_by(student_id=user.student_profile.id).all()
                for app in applications:
                    writer.writerow([app.id, app.drive_id, app.drive.drive_name, app.drive.company.company_name, app.drive.job_title, app.status, app.remark])
            elif user.role == "company":
                writer.writerow(["Drive ID", "Job Title", "Total Applications", "Total Shortlisted", "Total Interviewed", "Total Selected"])
                drives = PlacementDrive.query.filter_by(company_id=user.company_profile.id).all()
                for drive in drives:
                    writer.writerow([drive.id, drive.job_title, len(drive.applications), len(drive.applications.filter_by(status="shortlisted").all()), len(drive.applications.filter_by(status="interview").all()), len(drive.applications.filter_by(status="selected").all())])

        file_url = f"http://127.0.0.1:5000/static/{get_jwt_identity().replace("@", "_")}_report.csv"
        csv_report.delay(email=get_jwt_identity(), file_url=file_url)

        return {"message": "CSV report generation started. You will receive an email once it's ready."}, 202
    
api.add_resource(CSVExport, '/export/csv')


class Logout(Resource):

    @jwt_required()
    def post(self):
        user = User.query.filter_by(email=get_jwt_identity()).first()
        if not user:
            return {"message": "User not found! Please login first."}, 404
        
        cache.delete(dashboard_cache_key())

        return {"message": "Logout successful! Please discard your token on client side."}, 200

api.add_resource(Logout, '/logout')