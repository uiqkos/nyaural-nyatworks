<template>
  <div class="container">
    <h1 class="nya-text" style="margin-top: 5%">Отчеты</h1>
    <table class="table">
      <thead>
      <tr>
        <th scope="col">заголовок</th>
        <th scope="col">дата</th>
        <th scope="col">тэги</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="report in reports" :key="report">
        <td>
          <router-link :to="{name: 'report', params: {name: report.name}}" >
            {{ report.title }}
          </router-link>
        </td>

        <td>{{ report.date.slice(0, 10) }}</td>
        <td>
          <div v-for="tag in report.tags" :key="tag" >
            <span :class="'badge bg-' + bgByGrad(tag.grad)">
              {{ tag.name }}
            </span>
          </div>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Api from "@/Api";

export default {
  name: "ReportsPage",
  data() {
    return {
      'reports': []
    }
  },
  async created() {
    this.reports = await Api.allReports()
  },
  methods: {
    bgByGrad(grad) {
      switch (grad) {
        case 0:
          return 'danger'
        case 1:
          return 'primary'
        case 2:
          return 'success'
        default:
          return 'secondary'
      }
    }
  }
}
</script>

<style scoped>

</style>