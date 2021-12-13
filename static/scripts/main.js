let alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

let keyboardLayoutMap = '1234567890-=qwertyuiop[] asdfghjkl;\'\\ zxcvbnm,./ '

function missclick(ch) {
  let i = keyboardLayoutMap.indexOf(ch)
  let vertical = (Math.floor(Math.random() * 3) - 1) * 12
  let horizontal = (Math.floor(Math.random() * 3) - 1)
  let rch = keyboardLayoutMap[Math.min(Math.max(0, vertical + horizontal + i), keyboardLayoutMap.length - 1)]
  return rch === ' ' ? ch : rch;
}

function nextInt() {
  return (Math.random() * (400 - 100) + 100)
}

export async function typingText(text_ids, textSources, cursor_id, completeClass) {
  if (completeClass == undefined) {
    completeClass = 'nya-decoration-lg-1'
  }

  let cursor = document.getElementById(cursor_id)

  cursor.style.color = "#5A189A"

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
      if (Math.random() > 0.85 && j != source.length - 1) {
        let randomch =  missclick(source[j])
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
  }
}
