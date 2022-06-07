<template>
  <div class="container">
    <h1 class="nya-text" style="margin-top: 5%">Результаты анализа</h1>
    <CommentEntity :comment="this.rootComment"
                   :level="0"
                   :grads="this.grads"
                   :parent-request-params="this.requestParams"/>
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import CommentEntity from "@/components/CommentEntity";
import Api from "@/Api";

export default {
  name: "ResultPage",
  components: {CommentEntity},
  data() {
    return {
      page: 1,
      requestParams: null,
      grads: null,
      rootComment: {
        author: {}
      },
      per_page: 5
    }
  },
  async created() {
    const route = useRoute()
    this.params = route.params

    this.requestParams = this.params
    this.requestParams['page'] = this.page
    this.requestParams['per_page'] = this.per_page
    this.requestParams['styled'] = true
    this.requestParams['expand'] = ''

    let rootRequestParams = this.requestParams
    rootRequestParams['per_page'] = 1
    rootRequestParams['page'] = 1
    rootRequestParams['stats'] = 1

    let response = (await Api.predictParams(
        rootRequestParams
    ))

    this.rootComment = response.items[0]
    this.grads = response.grads

  },
  methods: {
    nextPage() {
      this.page += 1
    }
  }
}
</script>

<style scoped>

.round img {
  border-radius: 100%
}

.action-icons a {
  padding-left: 7px;
  vertical-align: middle;
  color: #99abb4
}

.action-icons a:hover {
  color: #1976d2
}

.mt-100 {
  margin-top: 100px
}

.mb-100 {
  margin-bottom: 100px
}
</style>