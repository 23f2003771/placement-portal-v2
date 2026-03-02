import { createRouter, createWebHistory } from 'vue-router'

import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import AdminDashboard from '@/pages/AdminDashboard.vue'
import StudentDashboard from '@/pages/StudentDashboard.vue'
import CompanyDashboard from '@/pages/CompanyDashboard.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: AdminDashboard
    },
    {
      path: '/student-dashboard',
      name: 'student-dashboard',
      component: StudentDashboard
    },
    {
      path: '/company-dashboard',
      name: 'company-dashboard',
      component: CompanyDashboard
    }
  ],
})

export default router
