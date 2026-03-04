<template>
    <div class="admin-dashboard">
        <section>
            <h2>Registered Companies</h2>
                <div v-for="company in companies" :key="company.id", class="row">
                    <span>{{ company.company_name }}</span>
                    <button @click="blacklistCompany(company.id)">Blacklist</button>
                </div>
        </section>
        <section>
            <h2>Registered Students</h2>
                <div v-for="student in students" :key="student.id", class="row">
                    <span>{{ student.full_name }}</span>
                    <button @click="blacklistStudent(student.id)">Blacklist</button>
                </div>
        </section>
        <section>
            <h2>Company Applications</h2>
                <div v-for="application in company_applications" :key="application.id", class="row">
                    <span>{{ application.company_name }}</span>
                    <button  @click="approveCompany(application.id)">Approve</button>
                    <button @click="rejectCompany(application.id)">Reject</button>
                </div>
        </section>
        <section>
            <h2>Ongoing Drives</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Drive Name</th>
                        <th>Actions</th>
                    </tr> 
                </thead>
                <tbody> 
                <tr v-for="drive in ongoing_drives" :key="drive.id", class="row">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.drive_name }}</td>
                    <td>
                        <button @click="viewDrive(drive)">View Details</button>
                        <button @click="completeDrive(drive.id)">Mark as Completed</button>
                        <button @click="rejectDrive(drive.id)">Reject Drive</button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-if="showDetails" class="popup" @click="closeDetails">
                    <h3>{{ selectedDrive.drive_name }}</h3>
                    <p><strong>Job Title:</strong> {{ selectedDrive.job_title }}</p>
                    <p><strong>Company Email:</strong> {{ selectedDrive.company_email }}</p>
                    <p><strong>Description:</strong> {{ selectedDrive.description }}</p>
                    <p><strong>Salary:</strong> {{ selectedDrive.salary }}</p>
                    <p><strong>Location:</strong> {{ selectedDrive.location }}</p>
                    <button @click="closeDetails">Close</button>
            </div>
        </section>
        <section>
            <h2>All Applications</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Student Name</th>
                        <th>Company Name</th>
                        <th>Drive Name</th>
                        <th>Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="application in applications" :key="application.id", class="row">
                    <td>{{ application.id }}</td>
                    <td>{{ application.name }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.drive_name }}</td>
                    <td>{{ application.applied_at }}</td>
                    <td>
                        <button @click="viewApplication(application)">View</button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-if="showApplicationDetails" class="popup" @click="closeApplicationDetails">
                    <h3>Student Application</h3>
                    <p><strong>Student Name:</strong> {{ selectedApplication.name }}</p>
                    <p><strong>Department:</strong> {{ selectedApplication.department }}</p>    
                    <p><strong>Company Name:</strong> {{ selectedApplication.company_name }}</p>
                    <p><strong>Drive Name:</strong> {{ selectedApplication.drive_name }}</p>
                    <p><strong>Date Applied:</strong> {{ selectedApplication.applied_at }}</p>
                    <p><strong>Status:</strong> {{ selectedApplication.status }}</p>
                    <p><strong>Remark:</strong> {{ selectedApplication.remark }}</p>
                    <button @click="closeApplicationDetails">Close</button>
            </div>
        </section>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                students : [],
                companies : [],
                applications : [],
                ongoing_drives : [],
                company_applications : [],
                selectedDrive: null,
                showDetails: false,
                selectedApplication: null,
                showApplicationDetails: false
            };
        },
        async mounted() {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    this.$router.push('/login');
                    return;
                }

                const response = await fetch('http://localhost:5000/admin/dashboard', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch dashboard data');
                }

                const data = await response.json();
                this.students = data.students;
                this.companies = data.companies;
                this.applications = data.applications;
                this.ongoing_drives = data.drives;
                this.company_applications = data.company_applications;
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
            }
        }, methods: {
            async blacklistCompany(companyId) {
                const token = localStorage.getItem('token');
                if (!token) {
                    this.$router.push('/login');
                    return;
                }

                 try {
                    const response = await fetch(`http://localhost:5000/admin/dashboard/${companyId}`, {
                        method: 'PUT',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ action: "blacklist" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to blacklist company');
                    }

                    alert('Company blacklisted successfully!');
                } catch (error) {
                    alert('Error blacklisting company: ' + error.message);
                }
            },
            async blacklistStudent(studentId) {
                try {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        this.$router.push('/login');
                        return;
                    }

                    const response = await fetch(`http://localhost:5000/admin/dashboard/${studentId}`, {
                        method: 'PUT',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ action: "blacklist" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to blacklist student');
                    }

                    alert('Student blacklisted successfully!');
                } catch (error) {
                    alert('Error blacklisting student: ' + error.message);
                }
            },
            async approveCompany(applicationId) {
                try {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        this.$router.push('/login');
                        return;
                    }

                    const response = await fetch(`http://localhost:5000/admin/dashboard/${applicationId}`, {
                        method: 'PUT',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ action: "approve" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to approve company application');
                    }

                    alert('Company application approved successfully!');
                } catch (error) {
                    alert('Error approving company application: ' + error.message);
                }
            },
            async rejectCompany(applicationId) {
                try {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        this.$router.push('/login');
                        return;
                    }

                    const response = await fetch(`http://localhost:5000/admin/dashboard/${applicationId}`, {
                        method: 'PUT',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ action: "reject" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to reject company application');
                    }

                    alert('Company application rejected successfully!');
                } catch (error) {
                    alert('Error rejecting company application: ' + error.message);
                }
            },
            async viewDrive(drive) {
                this.selectedDrive = drive;
                this.showDetails = true;
            },
            async closeDetails() {
                this.showDetails = false;
                this.selectedDrive = null;
            },
            async completeDrive(driveId) {
                try {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        this.$router.push('/login');
                        return;
                    }

                    const response = await fetch(`http://localhost:5000/admin/dashboard/${driveId}`, {
                        method: 'PUT',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ action: "complete_drive" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to complete drive');
                    }

                    alert('Drive marked as completed successfully!');
                } catch (error) {
                    alert('Error completing drive: ' + error.message);
                }
            },
            async rejectDrive(driveId) {
                try {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        this.$router.push('/login');
                        return;
                    }

                    const response = await fetch(`http://localhost:5000/admin/dashboard/${driveId}`, {
                        method: 'PUT',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ action: "reject_drive" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to reject drive');
                    }

                    alert('Drive rejected successfully!');
                } catch (error) {
                    alert('Error rejecting drive: ' + error.message);
                }
            },
            async viewApplication(application) {
                this.selectedApplication = application;
                this.showApplicationDetails = true;
                
            },
            async closeApplicationDetails() {
                this.showApplicationDetails = false;
                this.selectedApplication = null;
            }
        }
    };
</script>

<style scoped>
    .admin-dashboard {
        padding: 20px;
    }
    .row {
        display: flex;
        gap: 10px;
        margin-bottom: 5px;
        border: 1px solid #ccc;
        justify-content: space-between;
        padding: 10px;
        margin-top: 8px;
    }
    section {
        margin-bottom: 30px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: left;
    }
</style>