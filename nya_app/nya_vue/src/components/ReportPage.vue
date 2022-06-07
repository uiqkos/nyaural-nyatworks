<template>
  <div class="container" style="margin-top: 4%; font-family: 'Liberation Mono',serif">
    <div class="display-5">
      {{ report.title }}
    </div>
    <hr/>
    <div v-html="html"></div>
  </div>
</template>

<script>
import {marked} from "marked";
import {useRoute} from "vue-router";
import Api from "@/Api";


export default {
  name: "ReportPage",
  data() {
    return {
      html: null,
      report: null
    }
  },
  async created() {
    const route = useRoute()
    this.report = await Api.reportByName(route.params.name)

    this.html = marked(this.report.text, {
      'baseUrl': Api.baseUrl + 'static/',
    })
  },
  // methods: {
  //   htmlReport() {
  //     return h
  //   }
  // }
}
</script>

<style scoped>

</style>