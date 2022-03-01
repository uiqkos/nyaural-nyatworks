import axios from 'axios'

const http = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-type": "application/vnd.api+json"
  }
})

const Api = {
  allModels() {
    return http.get('/models/').then(response => response)
  },
  predict(input, text, toxic, sentiment, sarcasm, page, per_page, styled, stats) {
    return http.get('/predict', {
      params: {
        input, text, toxic, sentiment, sarcasm, page, per_page, styled, stats
      }
    })
  }
}

export default Api
