<template>
    <div class="student-dashboard">
        <section class="company-list">
            <h2>Available Companies and Drives</h2>
            <div v-for="company in organizations" :key="company.id" class="company-card">
                <table>
                    <thead>
                        <tr>
                            <th>Company Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{{ company.company_name }}</td>
                            <td><button @click="viewdrives(company)">View Drives</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-if="showDrives" class="drive-list">
                <h3>Drives for {{ selectedCompany.company_name }}</h3>
                <h4>Overview</h4>
                <p>{{ selectedCompany.description }}</p>
                <table>
                    <thead>
                        <tr>
                            <th>Drive Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="drive in selectedCompany.drives" :key="drive.id">
                            <td>{{ drive.drive_name }}</td>
                            <td><button @click="viewDetails(drive)">View Details</button></td>
                        </tr>
                    </tbody>
                </table>
                <button @click="selectedCompany = null; showDrives = false">Back</button>
            </div>
            <div v-if="showDetails" class="drive-details">
                <h3>{{ selectedDrive.drive_name }}</h3>
                <p><strong>Job Title:</strong> {{ selectedDrive.job_title }}</p>
                <p><strong>Description:</strong> {{ selectedDrive.description }}</p>
                <p><strong>Application Deadline:</strong> {{ selectedDrive.application_deadline }}</p>
                <p><strong>Eligibility Criteria:</strong> {{ selectedDrive.eligiblility_criteria }}</p>
                <p><strong>Interview Type:</strong> {{ selectedDrive.interview_type }}</p>
                <button @click="applyToDrive(selectedDrive.id)">Apply to Drive</button>
                <button @click="selectedDrive = null; showDetails = false">Back</button>
            </div>
        </section>
                <section>
            <h2>Applied Drives</h2>
            <table>
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
                <tr v-for="drive in applied_drives" :key="drive.id", class="row">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.drive_name }}</td>
                    <td>{{ drive.company_name }}</td>
                    <td>{{ drive.application_deadline }}</td>
                    <td>
                        <button @click="viewDriveDetails(drive)">View Details</button>
                    </td>
                </tr>
                </tbody>
            </table>
            <div v-if="showAppliedDetails" class="drive-details">
                <h3>{{ selectedAppliedDrive.drive_name }}</h3>
                <p><strong>Company Name:</strong> {{ selectedAppliedDrive.company_name }}</p>
                <p><strong>Job Title:</strong> {{ selectedAppliedDrive.job_title }}</p>
                <p><strong>Description:</strong> {{ selectedAppliedDrive.description }}</p>
                <p><strong>Application Deadline:</strong> {{ selectedAppliedDrive.application_deadline }}</p>
                <p><strong>Status:</strong> {{ selectedAppliedDrive.status }}</p>
                <p><strong>Remark:</strong> {{ selectedAppliedDrive.remark }}</p>
                <button @click="selectedAppliedDrive = null; showAppliedDetails = false">Back</button>
            </div>
        </section>
        <section>
            <h2>Student Application History</h2>
            <table>
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
                <tr v-for="history in history" :key="history.id", class="row">
                    <td>{{ history.id }}</td>
                    <td>{{ history.interview_type }}</td>
                    <td>{{ history.job_title }}</td>
                    <td>{{ history.status }}</td>
                    <td>{{ history.remark }}</td>
                </tr>
                </tbody>
            </table>
        </section>
        <section class="export-csv">
            <button @click="exportCSV">Export Data as CSV</button>
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
                showAppliedDetails: false

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
                localStorage.removeItem("token");
                this.$router.push("/login");
            }
        }
    }

</script>