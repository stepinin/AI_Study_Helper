let mode = "home"
let correctAnswers = []

function loadPage(page){

mode = page

let main = document.getElementById("main")
let topbar = document.getElementById("topbar")

topbar.style.display = "flex"

if(page === "home"){
main.innerHTML = `
<h1>💬 Чат</h1>
<div id="chat" class="chat"></div>
`

addBot("Приветствую! 👋")
addBot("Можете задать любой вопрос")
}

if(page === "explain"){
main.innerHTML = `
<h1>📚 Объяснение</h1>
<div id="chat" class="chat"></div>
`
addBot("Введите тему, я объясню просто")
}

if(page === "test"){
main.innerHTML = `
<h1>❓ Тест</h1>
<div id="chat" class="chat"></div>
`
addBot("Введите тему для теста")
}
}

function addMessage(text, type){
let chat = document.getElementById("chat")

let msg = document.createElement("div")
msg.className = "message " + type
msg.innerHTML = text.replace(/\n/g, "<br>")

chat.appendChild(msg)
chat.scrollTop = chat.scrollHeight
}

function addUser(text){ addMessage(text, "user") }
function addBot(text){ addMessage(text, "bot") }

async function send(){

let input = document.getElementById("input")
let text = input.value.trim()

if(!text) return

addUser(text)
input.value = ""

addBot("⏳ Думаю... Подождите...")

let url = "/chat"

if(mode === "explain") url = "/explain"
if(mode === "test") url = "/test"

let res = await fetch(url,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(
    mode === "home"
    ? {message: text}
    : {topic: text}
)
})

let data

try{
data = await res.json()
}catch{
addBot("❌ Ошибка сервера")
return
}

let chat = document.getElementById("chat")
chat.removeChild(chat.lastChild)

if(mode === "test"){

correctAnswers = data.answers || []

data.questions.forEach((q,i)=>{
addBot(`${q}<br><input id="q${i}" placeholder="A/B/C/D">`)
})

addBot(`<button onclick="finishTest()">Завершить тест</button>`)

}else{
addBot(data.answer)
}
}

window.onload = () => loadPage("home")
