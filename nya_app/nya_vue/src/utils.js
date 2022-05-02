
const Utils = {
  argmax(arr) {
    let max = -9999999
    let idx = -1
    for (let [i, a] of arr.entries()) {
      if (a > max) {
        max = a
        idx = i
      }
    }
    return idx
  },
}

export default Utils;
