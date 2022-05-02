import {createRouter, createWebHashHistory} from "vue-router";
import About from "@/components/About";
import HomePage from "@/components/HomePage";
import PredictPage from "@/components/PredictPage";
import ResultPage from "@/components/ResultPage";
import ReportsPage from "@/components/ReportsPage";
import ReportPage from "@/components/ReportPage";

const routes = [
  {path: '/', alias: '/home', name: 'home', component: HomePage},
  {path: '/rating', name: 'rating', component: About},
  {path: '/reports', name: 'reports', component: ReportsPage},
  {path: '/report', name: 'report', params: true, component: ReportPage},
  {path: '/predict', name: 'predict', component: PredictPage},
  {path: '/result', name: 'result', params: true, component: ResultPage},
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
