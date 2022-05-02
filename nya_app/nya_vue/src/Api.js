
const baseUrl = new URL("http://192.168.1.147:8000")
const params = {
  headers: {
    "Content-type": "application/json"
  }
}

const Api = {
  baseUrl: baseUrl,
  async allModels() {
    return await fetch(baseUrl + 'models', params)
      .then(response => response.json())
  },
  async predict(input, text, toxic, sentiment, sarcasm, page, per_page, styled, expand) {
    return await fetch(
      baseUrl + 'predict?' + new URLSearchParams({
        input, text, toxic, sentiment, sarcasm, page, per_page, styled, expand
      })
    ).then(response => response.json())
  },
  async predictParams(params) {
    return await this.predict(...Object.values(params))
  },
  async allReports() {
    return await fetch(baseUrl + 'reports', params)
      .then(response => response.json())
  },
  async reportByName(name) {
    return await fetch(baseUrl + 'reports/' + name, params)
      .then(response => response.json())
  },
}

export default Api
