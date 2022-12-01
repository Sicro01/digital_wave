import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PlanDetailView from '@/views/old/PlanDetailView orig.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:plan_slug',
    name: 'plan',
    component: PlanDetailView,
  },
  {
    path: '/:plan_slug/phase_slug',
    name: 'phase',
    component: PlanDetailView
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
