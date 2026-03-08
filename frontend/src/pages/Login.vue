<template>
    <div class="container vh-100 d-flex justify-content-center align-items-center">
        <div class="card shadow p-4" style="width: 400px;">
        <h3 class="text-center mb-3">Placement Portal Login</h3>
        <p class="text-center text-muted mb-4">Please enter your credentials to access your dashboard.</p>
        <form class="d-grid gap-3">
            <div>
                <label class="form-label" for="email">Email</label>
                <input v-model="email" class="form-control" type="email" id="email" required />
            </div>
            <div>
                <label class="form-label" for="password">Password</label>
                <input v-model="password" class="form-control" type="password" id="password" required />
            </div>
            <button class="btn btn-primary w-100" type="button" @click="login">Login</button>
        </form>
        <button class="btn btn-outline-secondary w-100" @click="$router.push('/')">Register</button>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                email : '',
                password : ''
            };
        },
        methods: {
           async login() {
                try {
                    const response = await fetch('http://127.0.0.1:5000/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            email: this.email,
                            password_hash: this.password
                        })
                    });

                    const data = await response.json();

                    if (!response.ok) {
                        throw new Error(data.message || 'Login failed');
                    }

                    localStorage.setItem('token', data.token);
                    localStorage.setItem('role',data.login_data.role)
                    localStorage.setItem('name',data.login_data.name)

                    if (data.login_data.role === 'student') {
                        this.$router.push('/student-dashboard');
                    } else if (data.login_data.role === 'company') {
                        this.$router.push('/company-dashboard');
                    } else if (data.login_data.role === 'admin') {
                        this.$router.push('/admin-dashboard');
                    } else {
                        throw new Error('Unknown user role');
                    }

                    alert('Login successful!');
                } catch (error) {
                    alert('Error during login: ' + error.message);
                }
            }
        }
    };
</script>

