<template>
    <div class="container py-5 d-flex justify-content-center">
        <div class="card shadow p-4" style="width: 500px;">
        <h3 class="text-center mb-3">Placement Portal Registration</h3>
        <p class="text-center text-muted mb-4">Please fill in the form below to create an account.</p>
        <form class="d-grid gap-3">
            <div>
                <label class="form-label" for="email">Email</label>
                <input v-model="email" class="form-control" type="email" id="email" required />
            </div>
            <div>
                <label class="form-label" for="password">Password</label>
                <input v-model="password" class="form-control" type="password" id="password" required />
            </div>
            <div>
                <label class="form-label" for="role">Role</label>
                <select v-model="role" class="form-select" id="role" required>
                    <option value="">Select Role</option>
                    <option value="student">Student</option>
                    <option value="company">Company</option>
                </select>
            </div>
            <div v-if="role === 'student'" class="border rounded p-3 mt-2">
                <div>
                    <label class="form-label" for="full_name">Full Name:</label>
                    <input v-model="full_name" class="form-control" type="text" id="full_name" required />
                </div>
                <div>
                    <label class="form-label" for="branch">Branch:</label>
                    <input v-model="branch" class="form-control" type="text" id="branch" required />
                </div>
                <div>
                    <label class="form-label" for="cgpa">CGPA:</label>
                    <input v-model="cgpa" class="form-control" type="number" step="0.01" id="cgpa" required />
                </div>
                <div>
                    <label class="form-label" for="year">Year:</label>
                    <input v-model="year" class="form-control" type="number" id="year" required />
                </div>
                <div>
                    <label class="form-label" for="phone">Phone Number:</label>
                    <input v-model="phone" class="form-control" type="tel" id="phone" required />
                </div>
                <div>
                    <label class="form-label" for="resume_path">Resume Path:</label>
                    <input v-model="resume_path" class="form-control" type="text" id="resume_path" required />
                </div>
            </div>
            <div v-else-if="role === 'company'" class="border rounded p-3 mt-2">
                <div>
                    <label class="form-label" for="company_name">Company Name:</label>
                    <input v-model="company_name" class="form-control" type="text" id="company_name" required />
                </div>
                <div>
                    <label class="form-label" for="hr_contact">HR Contact:</label>
                    <input v-model="hr_contact" class="form-control" type="text" id="hr_contact" required />
                </div>
                <div>
                    <label class="form-label" for="website">Website:</label>
                    <input v-model="website" class="form-control" type="url" id="website" required />
                </div>
                <div>
                    <label class="form-label" for="description">Description:</label>
                    <textarea v-model="description" class="form-control" id="description" rows="3" required></textarea>
                </div>
            </div>
            <button class="btn btn-success w-100 mt-3" type="button" @click="register">Register</button>
        </form>
        <button class="btn btn-outline-secondary w-100 mt-2" @click="$router.push('/login')">Already have an account? Login</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: '',
            password: '',
            role: '',
            full_name: '',
            branch: '',
            cgpa: '',
            year: '',
            phone: '',
            resume_path: '',
            company_name: '',
            hr_contact: '',
            website: '',
            description: ''
        };
    },
    methods: {
        async register() {
            try {
                const response = await fetch('http://127.0.0.1:5000/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password_hash: this.password,
                        role: this.role,
                        full_name: this.full_name,
                        branch: this.branch,
                        cgpa: this.cgpa,
                        year: this.year,
                        phone: this.phone,
                        resume_path: this.resume_path,
                        company_name: this.company_name,
                        hr_contact: this.hr_contact,
                        website: this.website,
                        description: this.description
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || 'Registration failed');
                }

                alert('Registration successful!');
                this.$router.push('/login');
            } catch (error) {
                alert('Error during registration: ' + error.message);
            }
        }
    }
};
</script>

<style scoped>
.register {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}
form div {
    margin-bottom: 15px;
}
label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}
input, select, textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}
button:hover {
    background-color: #0056b3;
}
</style>

