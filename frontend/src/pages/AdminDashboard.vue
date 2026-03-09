<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand fw-semibold" href="#">Placement Portal - Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
            <form class="d-flex me-3" role="search" @submit.prevent>
                <input class="form-control me-2" type="search" placeholder="Search" v-model="searchQuery" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            <ul class="navbar-nav mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link text-danger" style="cursor:pointer;" @click="logout">Logout</a>
                </li>
            </ul>
        </div>
    </div>
    </nav>
    <div class="container mt-5">
    <div class="container mt-4 shadow-sm p-3 bg-light rounded" v-if="searchQuery.trim().length > 0">
    <ul class="list-group">
        <li v-for="company in filteredCompanies" :key="'c-' + company.id" class="list-group-item">
            <strong>Company Name: </strong>{{ company.company_name }} | <strong>Email: </strong>{{ company.email }} | <strong>Website: </strong>{{ company.website }} | <strong>Approval Status: </strong>{{ company.approval_status }}</li>
        <li v-for="student in filteredStudents" :key="'s-' + student.id" class="list-group-item">
            <strong>Full Name: </strong>{{ student.full_name }} | <strong>Email: </strong>{{ student.email }} | <strong>Branch: </strong>{{ student.branch }} | <strong>CGPA: </strong>{{ student.cgpa }} | <strong>Blacklisted: </strong>{{ student.is_blacklisted }}</li>
        <li v-for="drive in filteredDrives" :key="'d-' + drive.id" class="list-group-item">
            <strong>Drive Name: </strong>{{ drive.drive_name }} | <strong>Description: </strong>{{ drive.description }} | <strong>Job Title: </strong>{{ drive.job_title }} | <strong>Salary: </strong>{{ drive.salary }} | <strong>Location: </strong>{{ drive.location }}</li>
    </ul>
    </div>
        <section class="card p-3 mb-4 shadow-sm">
            <h4 class="border-bottom pb-2 mb-3">Registered Companies</h4>
                <div v-for="company in companies" :key="company.id" class="row align-items-center border rounded p-2 mb-2">
                    <span class="col">{{ company.company_name }}</span>
                    <button class="btn btn-sm btn-danger col-auto" @click="blacklistCompany(company.id)">Blacklist</button>
                </div>
        </section>
        <section class="card p-3 mb-4 shadow-sm">
            <h4 class="border-bottom pb-2 mb-3">Registered Students</h4>
                <div v-for="student in students" :key="student.id" class="row align-items-center border rounded p-2 mb-2">
                    <span class="col">{{ student.full_name }}</span>
                    <button class="btn btn-sm btn-danger col-auto" @click="blacklistStudent(student.id)">Blacklist</button>
                </div>
        </section>
        <section class="card p-3 mb-4 shadow-sm">
            <h4 class="border-bottom pb-2 mb-3">Company Applications</h4>
                <div v-for="application in company_applications" :key="application.id" class="row align-items-center border rounded p-2 mb-2">
                    <span class="col">{{ application.company_name }}</span>
                    <button class="btn btn-sm btn-success me-2 col-auto" @click="approveCompany(application.id)">Approve</button>
                    <button class="btn btn-sm btn-danger col-auto" @click="rejectCompany(application.id)">Reject</button>
                </div>
        </section>
        <section class="card p-3 mb-4 shadow-sm">
            <h4 class="border-bottom pb-2 mb-3">Ongoing Drives</h4>
            <table class="table table-bordered table-striped mt-3">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Drive Name</th>
                        <th>Actions</th>
                    </tr> 
                </thead>
                <tbody> 
                <tr v-for="drive in ongoing_drives" :key="drive.id">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.drive_name }}</td>
                    <td>
                        <button class="btn btn-sm btn-primary me-2" @click="viewDrive(drive)">View Details</button>
                        <button class="btn btn-sm btn-success me-2" @click="completeDrive(drive.id)">Mark as Completed</button>
                        <button class="btn btn-sm btn-danger" @click="rejectDrive(drive.id)">Reject Drive</button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-if="showDetails" class="position-fixed top-50 start-50 translate-middle bg-white p-4 shadow rounded" style="z-index:1050; width:400px;">
                    <h3>{{ selectedDrive.drive_name }}</h3>
                    <p><strong>Job Title:</strong> {{ selectedDrive.job_title }}</p>
                    <p><strong>Company Email:</strong> {{ selectedDrive.company_email }}</p>
                    <p><strong>Description:</strong> {{ selectedDrive.description }}</p>
                    <p><strong>Salary:</strong> {{ selectedDrive.salary }}</p>
                    <p><strong>Location:</strong> {{ selectedDrive.location }}</p>
                    <button class="btn btn-secondary mt-2" @click="closeDetails">Back</button>
            </div>
        </section>
        <section class="card p-3 mb-4 shadow-sm">
            <h4 class="border-bottom pb-2 mb-3">All Applications</h4>
            <table class="table table-bordered table-hover mt-3">
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
                <tr v-for="application in applications" :key="application.id">
                    <td>{{ application.id }}</td>
                    <td>{{ application.name }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.drive_name }}</td>
                    <td>{{ application.applied_at }}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" @click="viewApplication(application)">View</button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-if="showApplicationDetails" class="position-fixed top-50 start-50 translate-middle bg-white p-4 shadow rounded" style="z-index:1050; width:400px;">
                    <h3>Student Application</h3>
                    <p><strong>Student Name:</strong> {{ selectedApplication.name }}</p>
                    <p><strong>Department:</strong> {{ selectedApplication.department }}</p>    
                    <p><strong>Company Name:</strong> {{ selectedApplication.company_name }}</p>
                    <p><strong>Drive Name:</strong> {{ selectedApplication.drive_name }}</p>
                    <p><strong>Date Applied:</strong> {{ selectedApplication.applied_at }}</p>
                    <p><strong>Status:</strong> {{ selectedApplication.status }}</p>
                    <p><strong>Remark:</strong> {{ selectedApplication.remark }}</p>
                    <button class="btn btn-secondary mt-2" @click="closeApplicationDetails">Back</button>
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
                showApplicationDetails: false,
                searchQuery: ''
            };
        },
        async mounted() {
            this.fetchDashboardData();
        }, methods: {
            async fetchDashboardData() {
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
            },
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

                    this.fetchDashboardData();
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

                    this.fetchDashboardData();
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

                    this.fetchDashboardData();
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

                    this.fetchDashboardData();
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
                        body: JSON.stringify({ action: "completed" })
                    });

                    if (!response.ok) {
                        throw new Error('Failed to complete drive');
                    }

                    this.fetchDashboardData();
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

                    this.fetchDashboardData();
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
            },
            async logout() {
                localStorage.removeItem("token");
                localStorage.removeItem("role");
                this.$router.push("/login");
            }
        }, computed: {
            filteredCompanies() {
                return this.companies.filter(company =>
                    company.company_name.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            },
            filteredStudents() {
                return this.students.filter(student =>
                    student.full_name.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            },
            filteredDrives() {
                return this.ongoing_drives.filter(drive =>
                    drive.drive_name.toLowerCase().includes(this.searchQuery.toLowerCase())
                );
            }
        }
    };
</script>