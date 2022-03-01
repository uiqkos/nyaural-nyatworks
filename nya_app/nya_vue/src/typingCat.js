// let keyboardLayoutMap = '1234567890-=qwertyuiop[] asdfghjkl;\'\\ zxcvbnm,./ '
let keyboardLayoutMap = ['1234567890-=', 'qwertyuiop[]', 'asdfghjkl;\'\\', 'zxcvbnm,./']

function missclick(ch) {
  let isLower = ch.toLowerCase() === ch
  let vertical = 0
  let horizontal = 0

  if (!isLower) {
    ch = ch.toLowerCase()
  }

  for (let i = 0; i < keyboardLayoutMap.length; i++) {
    if (keyboardLayoutMap[i].includes(ch)) {
      if (Math.random() < 0.5) vertical = Math.max(0, i - 1)
      else vertical = Math.min(keyboardLayoutMap.length - 1, i + 1)

      let j = keyboardLayoutMap[i].indexOf(ch)
      if (Math.random() < 0.5) horizontal = Math.max(0, j - 1)
      else horizontal = Math.min(keyboardLayoutMap[i].length - 1, j + 1)
    }
  }
  let rch = keyboardLayoutMap[vertical][horizontal]
  if (!isLower) rch = rch.toUpperCase()

  return rch
}

function nextInt() {
  return (Math.random() * (400 - 100) + 100)
}

export async function typingText(text_ids, textSources, cursor, completeClass, spaces) {
  if (completeClass === undefined) {
    completeClass = 'nya-decoration-lg-1'
  }

  cursor.classList.add('nya-text-header')
  cursor.classList.add('nya-first-color')

  setInterval(function () {
    if (cursor.style.visibility === 'hidden')
      cursor.style.visibility = 'visible';
    else
      cursor.style.visibility = 'hidden';
  }, 500)

  for (let i = 0; i < text_ids.length; i++) {
    let text = document.getElementById(text_ids[i])
    let source = textSources[i]

    for (let j = 0; j < source.length; j++) {
      if (Math.random() > 0.85 && j !== source.length - 1) {
        let randomch = missclick(source[j])
        while (source[j] === randomch) {
          randomch = missclick(source[j])/*alphabet[Math.floor(Math.random() * (alphabet.length - 1))]*/
        }
        text.innerHTML += randomch
        await new Promise(r => setTimeout(r, nextInt()))
        text.innerHTML = text.innerHTML.slice(0, text.innerHTML.length - 1)
        await new Promise(r => setTimeout(r, nextInt()))
      }
      text.innerHTML += source[j]
      await new Promise(r => setTimeout(r, nextInt()))
    }

    text.classList.add(completeClass)
    if (i < spaces.length)
      spaces[i].innerHTML += ' '
  }
}
