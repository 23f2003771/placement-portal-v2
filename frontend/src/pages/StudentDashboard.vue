<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand fw-semibold" href="#">Placement Portal - Student Dashboard</a>
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
    <div class="container mt-4 mb-5">
        <div class="container mt-4 shadow-sm p-3 bg-light rounded" v-if="searchQuery.trim().length > 0">
            <ul class="list-group">
                <li v-for="company in filteredCompanies" :key="'c-' + company.id" class="list-group-item">
                    <strong>Company Name: </strong>{{ company.company_name }} | <strong>Contact: </strong>{{ company.hr_contact }} | <strong>Website: </strong>{{ company.website }}</li>
                <li v-for="drive in filteredDrives" :key="'d-' + drive.id" class="list-group-item">
                    <strong>Drive Name: </strong>{{ drive.drive_name }} | <strong>Job Title: </strong>{{ drive.job_title }} | <strong>Deadline: </strong>{{ drive.application_deadline }} | <strong>Eligibility: </strong>{{ drive.eligiblility_criteria }} | <strong>Interview Type: </strong>{{ drive.interview_type }}</li>
            </ul>
        </div>
        <section class="card shadow-sm p-3 mb-4">
            <h4 class="mb-3 border-bottom pb-2">Available Companies and Drives</h4>
            <div v-for="company in organizations" :key="company.id" class="company-card">
                <table class="table table-bordered table-striped table-hover mt-3">
                    <thead>
                        <tr>
                            <th>Company Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ company.company_name }}</td>
                            <td><button class="btn btn-sm btn-primary" @click="viewdrives(company)">View Drives</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-if="showDrives" class="position-fixed top-50 start-50 translate-middle bg-white p-4 shadow rounded" style="z-index:1000; width:400px;">
                <h3>Drives for {{ selectedCompany.company_name }}</h3>
                <h4>Overview</h4>
                <p>{{ selectedCompany.description }}</p>
                <table class="table table-sm table-bordered">
                    <thead>
                        <tr>
                            <th>Drive Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="drive in selectedCompany.drives" :key="drive.id">
                            <td>{{ drive.drive_name }}</td>
                            <td><button class="btn btn-sm btn-outline-primary" @click="viewDetails(drive)">View Details</button></td>
                        </tr>
                    </tbody>
                </table>
                <button class="btn btn-secondary mt-2" @click="selectedCompany = null; showDrives = false">Back</button>
            </div>
            <div v-if="showDetails" class="position-fixed top-50 start-50 translate-middle bg-white p-4 shadow rounded" style="z-index:1050; width:450px;">
                <h3>{{ selectedDrive.drive_name }}</h3>
                <p><strong>Job Title:</strong> {{ selectedDrive.job_title }}</p>
                <p><strong>Description:</strong> {{ selectedDrive.description }}</p>
                <p><strong>Application Deadline:</strong> {{ selectedDrive.application_deadline }}</p>
                <p><strong>Eligibility Criteria:</strong> {{ selectedDrive.eligiblility_criteria }}</p>
                <p><strong>Salary:</strong> {{ selectedDrive.salary }}</p>
                <p><strong>Location:</strong> {{ selectedDrive.location }}</p>
                <p><strong>Interview Type:</strong> {{ selectedDrive.interview_type }}</p>
                <button class="btn btn-success btn-sm me-2" @click="applyToDrive(selectedDrive.id)">Apply to Drive</button>
                <button class="btn btn-secondary mt-2" @click="selectedDrive = null; showDetails = false">Back</button>
            </div>
        </section>
            <section class="card shadow-sm p-3 mb-4">
            <h4 class="mb-3 border-bottom pb-2">Applied Drives</h4>
            <table class="table table-bordered table-striped table-hover mt-3">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Drive Name</th>
                        <th>Company Name</th>
                        <th>Deadline</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="drive in applied_drives" :key="drive.id">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.drive_name }}</td>
                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.application_deadline }}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" @click="viewDriveDetails(drive)">View Details</button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-if="showAppliedDetails" class="position-fixed top-50 start-50 translate-middle bg-white p-4 shadow rounded" style="z-index:1050; width:450px;">
                <h4 class="mb-3 border-bottom pb-2">{{ selectedAppliedDrive.drive_name }}</h4>
                <p><strong>Company Name:</strong> {{ selectedAppliedDrive.company_name }}</p>
                <p><strong>Job Title:</strong> {{ selectedAppliedDrive.job_title }}</p>
                <p><strong>Description:</strong> {{ selectedAppliedDrive.description }}</p>
                <p><strong>Application Deadline:</strong> {{ selectedAppliedDrive.application_deadline }}</p>
                <p><strong>Status:</strong> {{ selectedAppliedDrive.status }}</p>
                <p><strong>Remark:</strong> {{ selectedAppliedDrive.remark }}</p>
                <button class="btn btn-secondary mt-2" @click="selectedAppliedDrive = null; showAppliedDetails = false">Back</button>
            </div>
        </section>
        <section class="card shadow-sm p-3 mb-4">
            <h4 class="mb-3 border-bottom pb-2">Student Application History</h4>
            <table class="table table-bordered table-striped table-hover mt-3">
                <thead>
                    <tr>
                        <th>Drive Id</th>
                        <th>Interview Type</th>
                        <th>Job Title</th>
                        <th>Result</th>
                        <th>Remark</th>
                    </tr>
                </thead>
                <tbody>
                <tr v-for="history in history" :key="history.id">
                    <td>{{ history.id }}</td>
                    <td>{{ history.interview_type }}</td>
                    <td>{{ history.job_title }}</td>
                    <td>{{ history.status }}</td>
                    <td>{{ history.remark }}</td>
                </tr>
                </tbody>
            </table>
        </section>
        <section class="text-center mt-4">
            <button class="btn btn-outline-success" @click="exportCSV">Export Data as CSV</button>
        </section>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                applied_drives: [],
                organizations: [],
                history: [],
                selectedCompany: null,
                showDrives: false,
                selectedDrive: null,
                showDetails: false,
                showHistory: false,
                selectedAppliedDrive: null,
                showAppliedDetails: false,
                searchQuery: ''

            }
        },
        mounted() {
            this.fetchDashboardData();
        },
        methods: {
            async fetchDashboardData() {
                try {
                    const token = localStorage.getItem("token");
                    if (!token) {
                        console.error("No token found. Please log in.");
                        return;
                    }

                    const response = await fetch("http://localhost:5000/student/dashboard", {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    });

                    const data = await response.json();

                    this.applied_drives = data.applied_drives;
                    this.organizations = data.organizations;
                    this.history = data.history;
                } catch (error) {
                    console.error("Error fetching dashboard data:", error);
                }
            },
            async applyToDrive(driveId) {
                try {
                    const token = localStorage.getItem("token");
                    if (!token) {
                        console.error("No token found. Please log in.");
                        return;
                    }

                    const response = await fetch(`http://localhost:5000/student/dashboard/${driveId}`, {
                        method: "POST",
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        alert("Successfully applied to the drive!");
                        this.fetchDashboardData();
                    } else if (response.status === 409) {
                        alert(`You have already applied to this drive! Please wait for the response.`);
                    } else {
                        const errorData = await response.json();
                        alert(`Failed to apply: ${errorData.message}`);
                    }

                } catch (error) {
                    console.error("Error applying to drive:", error);
                }
            },
            async exportCSV() {
                try {
                    const token = localStorage.getItem("token");
                    if (!token) {
                        console.error("No token found. Please log in.");
                        return;
                    }

                    const response = await fetch("http://localhost:5000/export/csv", {
                        method: "POST",
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        alert("CSV report generation started. You will receive an email once it's ready.");
                    } else {
                        const errorData = await response.json();
                        alert(`Failed to start CSV export: ${errorData.message}`);
                    }
                } catch (error) {
                    console.error("Error exporting CSV:", error);
                }
            },
            viewdrives(company) {
                this.selectedCompany = company;
                this.showDrives = true;
            },
            viewDetails(drive) {
                this.selectedDrive = drive;
                this.showDetails = true;
            },
            viewDriveDetails(drive) {
                this.selectedAppliedDrive = drive;
                this.showAppliedDetails = true;
            },
            async logout() {
                const token = localStorage.getItem('token');
                if (!token) {             
                    this.$router.push('/login');
                    return;
                }

                const response = await fetch('http://localhost:5000/logout', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                    
                localStorage.removeItem("token");
                localStorage.removeItem("role");
                this.$router.push("/login");
            }
        }, computed : {

                filteredCompanies() {
                    return this.organizations.filter(company =>
                    company.company_name.toLowerCase().includes(this.searchQuery.toLowerCase())
                    );
                },
                filteredDrives() {
                    return this.organizations.flatMap(org => org.drives).filter(drive =>
                    drive.drive_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    drive.job_title.toLowerCase().includes(this.searchQuery.toLowerCase())
                    );
                }
            
        }
    }

</script>