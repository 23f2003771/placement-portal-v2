import time
from celery import shared_task
from models import Application, CompanyProfile, PlacementDrive
from send_mail import send_email


@shared_task
def daily_reminder():

    print("Started daily reminders")

    applications = Application.query.filter_by(status='interview').all()

    for application in applications:

        subject = "Interview Reminder"

        body = f"""
        Hello {application.student.full_name},

        Please visit the placement portal to check new internships.

        Regards,
        Placement Portal
        """

        send_email(application.student.user.email, subject, body)

    return "Daily reminders sent"


@shared_task
def monthly_report():

    companies = CompanyProfile.query.filter_by(is_blacklisted=False).all()

    hired = 0
    total = 0
    interview = 0
    shortlisted = 0
    for company in companies:
        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        for drive in drives:
            applications = Application.query.filter_by(drive_id=drive.id).all()
            for application in applications:
                total = total + 1
                if application.status == "selected":
                    hired = hired + 1
                elif application.status == "interview":
                    interview = interview + 1
                elif application.status == "shortlisted":
                    shortlisted = shortlisted + 1

        subject = "Monthly Placement Report"

        body = f"""
        Hello {company.company_name},
        Here's your monthly placement report from the Placement Portal v2.

        You Received {total} applications from our students this month.
        Out of those {shortlisted} students we shortlisted, {interview} students were selected for interviews, and {hired} were hired.


        We hope you found the right talent for your organization. Please log in to your dashboard to view & download detailed report and manage your placement drives.
        
        """

        send_email(company.user.email, subject, body)

    return "Monthly Placement Report sent"


@shared_task
def csv_report(email, file_url):

    print("Generating CSV report...")
    to = email

    time.sleep(5)
    subject = "CSV Export Completed"

    body = f"""Your requested CSV export is ready.
            You can download the file from the following link: <a href="{file_url}">Download CSV</a>"""

    send_email(to, subject, body)

    print("CSV report generated successfully.")