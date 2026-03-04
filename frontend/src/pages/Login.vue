<template>
    <div class="login">
        <h1>Login to the Placement Portal</h1>
        <p>Please enter your credentials to access your dashboard.</p>
        <form>
            <div>
                <label for="email">Email:</label>
                <input v-model="email" type="email" id="email" name="email" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input v-model="password" type="password" id="password" name="password" required />
            </div>
            <button type="button" @click="login">Login</button>
        </form>
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

