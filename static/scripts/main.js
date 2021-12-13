let alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
        let randomch = alphabet[Math.floor(Math.random() * (alphabet.length - 1))]
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