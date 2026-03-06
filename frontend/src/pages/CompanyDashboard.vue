<template>
    <div class="company-dashboard">
        <div class="first-row">
        <section class="create-drive">
            <h2>Create New Placement Drive</h2>
            <form>
                <input v-model="drive_name" placeholder="Drive Name" required />
                <input v-model="job_title" placeholder="Job Title" required />
                <textarea v-model="job_description" placeholder="Job Description" required></textarea>
                <input v-model="eligiblility_criteria" placeholder="Eligibility Criteria" required />
                <input v-model="application_deadline" type="date" placeholder="Application Deadline" required />
                <select v-model="interview_type" required>
                    <option value="" disabled>Select Interview Type</option>
                    <option value="online">Online</option>
                    <option value="offline">Offline</option>
                </select>
                <button type="button" @click="createDrive">Create Drive</button>
            </form>
        </section>
        <section class="ongoing-drives">
            <h2>Ongoing Placement Drives</h2>
            <table>
                <thead>
                    <tr>
                        <th>Sr No.</th>
                        <th>Drive Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="drive in ongoing_drives" :key="drive.id">
                        <td>{{ drive.id }}</td>
                        <td>{{ drive.drive_name }}</td>
                        <td>
                            <button @click="viewApplications(drive)">View Applications</button>
                            <button @click="markDriveCompleted(drive.id)">Mark Completed</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </section>
        </div>
        <section class="closed-drives">
            <h2>Closed Placement Drives</h2>
            <table>
                <thead>
                    <tr>
                        <th>Sr No.</th>
                        <th>Drive Name</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="drive in closed_drives" :key="drive.id">
                        <td>{{ drive.id }}</td>
                        <td>{{ drive.drive_name }}</td>
                    </tr>
                </tbody>
            </table>
        </section>
        <section>
            <div v-if="showApplications">
                <h3>Applications for {{ selectedDrive.drive_name }}</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Application ID</th>
                            <th>Student Name</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="application in selectedDrive.applications" :key="application.id">
                            <td>{{ application.id }}</td>
                            <td>{{ application.student_name }}</td>
                            <td>{{ application.status }}</td>
                            <td>
                                <button @click="viewDetails(application)">View Details</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <button @click="closeApplications">Back</button>
            </div>

            <div v-if="showDetails">
                <h3>Application Details for {{ selectedApplication.full_name }}</h3>
                <p><strong>Application ID:</strong> {{ selectedApplication.id }}</p>
                <p><strong>Branch Name:</strong> {{ selectedApplication.branch }}</p>
                <p><strong>CGPA:</strong> {{ selectedApplication.cgpa }}</p>
                <p><strong>Email:</strong> {{ selectedApplication.student_email }}</p>
                <p><strong>Resume Link:</strong> <a :href="selectedApplication.resume_path" target="_blank">View Resume</a></p>
                <p><strong>Status:</strong> {{ selectedApplication.status }}</p>
                <div class="status-radios">
                    <input v-model="remark" placeholder="Add Remark (optional)" />
                    <input type="radio" id="select" value="selected" v-model="updated_status">
                    <label for="select">Select</label>
                    <input type="radio" id="reject" value="rejected" v-model="updated_status">
                    <label for="reject">Reject</label>
                    <input type="radio" id="waitlist" value="waitlisted" v-model="updated_status">
                    <label for="waitlist">Waitlist</label>
                    <input type="radio" id="shortlist" value="shortlisted" v-model="updated_status">
                    <label for="shortlist">Shortlist</label>
                    <input type="radio" id="interview" value="interview" v-model="updated_status">
                    <label for="interview">Interview</label>
                    <button @click="changeApplicationStatus(selectedApplication.id, updated_status, remark)">Update Status</button>
                </div>
                <button @click="closeDetails">Back</button>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    data() {
        return {
            ongoing_drives: [],
            closed_drives: [],
            application_status: "",
            drive_name: "",
            job_title: "",
            job_description: "",
            eligiblility_criteria: "",
            application_deadline: "",
            interview_type: "",
            remark: "",
            updated_status: "applied",
            selectedApplication: null,
            showDetails: false,
            selectedDrive: null,
            showApplications: false
        };
    },
    async mounted() {
        this.fetchDashboardData();
    },
    methods: {
        async fetchDashboardData() {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    this.$router.push("/login");
                    return;
                }

                const response = await fetch("http://localhost:5000/company/dashboard", {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                const data = await response.json();

                this.ongoing_drives = data.ongoing_drives;
                this.closed_drives = data.closed_drives;
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            }
        },
        async createDrive() {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    this.$router.push("/login");
                    return;
                }

                const response = await fetch("http://localhost:5000/company/dashboard", {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        drive_name: this.drive_name,
                        job_title: this.job_title,
                        description: this.job_description,
                        application_deadline: this.application_deadline,
                        eligiblility_criteria: this.eligiblility_criteria,
                        interview_type: this.interview_type
                    })
                });

                if (!response.ok) {
                    throw new Error("Failed to create new drive");
                }

                this.fetchDashboardData();
                alert("Drive created successfully!");
            } catch (error) {
                alert("Failed to create new drive " + error.message);
            }
        },
        async markDriveCompleted(driveId) {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    this.$router.push("/login");
                    return;
                }

                const response = await fetch(
                    `http://localhost:5000/company/dashboard/${driveId}`,
                    {
                        method: "PUT",
                        headers: {
                            Authorization: `Bearer ${token}`,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            status: "completed"
                        })
                    }
                );

                if (!response.ok) {
                    throw new Error("Failed to update drive status");
                }

                this.fetchDashboardData();
                alert("Drive status updated successfully!");
            } catch (error) {
                alert("Failed to update drive status " + error.message);
            }
        },
        async changeApplicationStatus(applicationId, status, remark) {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    this.$router.push("/login");
                    return;
                }

                const response = await fetch(
                    `http://localhost:5000/company/dashboard/${applicationId}`,
                    {
                        method: "PUT",
                        headers: {
                            Authorization: `Bearer ${token}`,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            status: status,
                            remark: remark
                        })
                    }
                );

                if (!response.ok) {
                    throw new Error("Failed to update application status");
                }

                this.fetchDashboardData();
                alert("Application status updated successfully!");
            } catch (error) {
                alert("Failed to update application status " + error.message);
            }
        },
        viewDetails(application) {
            this.selectedApplication = application;
            this.showDetails = true;
        },
        viewApplications(drive) {
            this.selectedDrive = drive;
            this.showApplications = true;
        },
        closeDetails() {
            this.showDetails = false;
            this.selectedApplication = null;
        },
        closeApplications() {
            this.showApplications = false;
            this.selectedDrive = null;
        },
        async logout() {
            localStorage.removeItem("token");
            this.$router.push("/login");
        }
    }
};
</script>