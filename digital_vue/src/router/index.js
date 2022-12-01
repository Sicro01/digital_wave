import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import PlanDetailView from '@/views/PlanDetailView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/plan',
    name: 'plan',
    component: PlanDetailView
  },
  // {
  //   path: '/:phase_slug',
  //   name: 'phase',
  //   component: PlanDetailView,
  // },
  // {
  //   path: '/:plan_slug',
  //   name: 'plan',
  //   component: PlanDetailView,
  //   // component: PlanDetailView,
  // },
  // {
  //   path: '/:plan/:phase_slug',
  //   name: 'planPhase',
  //   component: PlanDetailView,
  // },
  // {
  //   path: '/:phase_slug/:strategy_slug',
  //   name: 'strategy',
  //   component: PlanDetailView,
  // },
  // {
  //   path: '/:plan/:phase_slug/:strategy_slug',
  //   name: 'planPhaseStrategy',
  //   component: PlanDetailView,
  // },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
