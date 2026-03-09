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
        <div>
            <h3>Interview Notification</h3>
            
            <p>Hello <strong>{application.student.full_name}</strong>,</p>

            <p><strong>Interview Details:</strong></p>
            <ul>
                <li><strong>Position:</strong> {application.drive.job_title}</li>
                <li><strong>Company:</strong> {application.drive.company.company_name}</li>
            </ul>

            <p><strong>Company Remarks:</strong></p>
            <blockquote>{application.remark}</blockquote>

            <p>Please make sure to prepare well and be on time for the interview.</p>

            <hr>
            <p>Regards,<br>
            <strong>Placement Portal</strong></p>
        </div>
        """

        send_email(application.student.user.email, subject, body)

    return "Daily reminders sent"


@shared_task
def monthly_report_companies():

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
        <div>
            <h3>Monthly Placement Report</h3>
            
            <p>Hello <strong>{company.company_name}</strong>,</p>
            
            <p>Here's your monthly placement report from the <strong>Placement Portal v2</strong>.</p>
            
            <p><strong>Monthly Activity Summary:</strong></p>
            <table border="1" cellpadding="10" cellspacing="0">
                <tr>
                    <td><strong>Total Applications</strong></td>
                    <td>{total}</td>
                </tr>
                <tr>
                    <td><strong>Shortlisted</strong></td>
                    <td>{shortlisted}</td>
                </tr>
                <tr>
                    <td><strong>Selected for Interview</strong></td>
                    <td>{interview}</td>
                </tr>
                <tr>
                    <td><strong>Successfully Hired</strong></td>
                    <td><strong>{hired}</strong></td>
                </tr>
            </table>

            <p>We hope you found the right talent for your organization. Please log in to your dashboard to view & download the detailed report and manage your placement drives.</p>

            <hr>
            <p>Regards,<br>
            <strong>Placement Portal Team</strong></p>
        </div>
        """

        send_email(company.user.email, subject, body)

    return "Monthly Placement Report sent"


@shared_task
def monthly_report_admin():

    completed_drives = PlacementDrive.query.filter_by(status="completed").count()
    ongoing_drives = PlacementDrive.query.filter_by(status="ongoing").count()
    applied_students = Application.query.filter_by(status="applied").count()
    selected_students = Application.query.filter_by(status="selected").count()

    subject = "Monthly Placement Report"

    body = f"""
    <div>
        <h2>Monthly Admin Placement Report</h2>
        
        <p>Hello <strong>Admin</strong>,</p>
        
        <p>Here is the monthly summary of activities on the <strong>Placement Portal v2</strong>.</p>
        
        <h3>Drive Statistics</h3>
        <table border="1" cellpadding="8" cellspacing="0">
            <tr bgcolor="#f2f2f2">
                <td><strong>Category</strong></td>
                <td><strong>Count</strong></td>
            </tr>
            <tr>
                <td>Total Placement Drives</td>
                <td>{completed_drives + ongoing_drives}</td>
            </tr>
            <tr>
                <td>Concluded Drives</td>
                <td>{completed_drives}</td>
            </tr>
            <tr>
                <td>Ongoing Drives</td>
                <td>{ongoing_drives}</td>
            </tr>
        </table>

        <h3>Student Participation</h3>
        <ul>
            <li><strong>Active Student Applications:</strong> {applied_students}</li>
            <li><strong>Selected Students:</strong> {selected_students}</li>
        </ul>

        <p>For a more detailed view, please log in to your <strong>Admin Dashboard</strong>.</p>
        
        <hr>
        <p>Regards,<br>
        <strong>Placement Portal System</strong></p>
    </div>
    """

    send_email('admin@gmail.com', subject, body)


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