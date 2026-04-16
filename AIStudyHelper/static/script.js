let mode = "home"
let correctAnswers = []

function loadPage(page){

mode = page

let main = document.getElementById("main")
let topbar = document.getElementById("topbar")

if(page === "home"){
topbar.style.display = "flex"
main.innerHTML = `<h1>Главная страница</h1><div id="chat" class="chat"></div>`
addBot("Добро пожаловать! 👋")
addBot("<-- Выберите раздел слева")
addBot("Или можем просто пообщаться")
}

if(page === "explain"){
topbar.style.display = "flex"
main.innerHTML = `<h1>Объяснение темы</h1><div id="chat" class="chat"></div>`
addBot("Введите тему для объяснения")
}

if(page === "test"){
topbar.style.display = "flex"
main.innerHTML = `<h1>Тесты</h1><div id="chat" class="chat"></div>`
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
let text = input.value

if(!text) return

addUser(text)
input.value = ""

addBot("⏳ Думаю... Подождите...")

let url = (mode === "test") ? "/test" : "/explain"

let res = await fetch(url, {
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({topic:text})
})

let data

try {
    data = await res.json()
} catch {
    addBot("❌ Ошибка сервера")
    return
}

let chat = document.getElementById("chat")
chat.removeChild(chat.lastChild)

if(mode === "test"){

correctAnswers = data.answers

data.questions.forEach((q, i) => {
addBot(`
${q}

Введите ответ:
<input id="q${i}">
`)
})

addBot(`<button onclick="finishTest()">Завершить тест</button>`)

}else{
addBot(data.answer)
}

}

function finishTest(){

let score = 0

for(let i = 0; i < correctAnswers.length; i++){

let user = document.getElementById("q"+i).value.trim().toUpperCase()

if(user === correctAnswers[i]){
score++
}

}

addBot(`🏆 Результат: ${score} / ${correctAnswers.length} \n Правильные ответы: \n 1. ${correctAnswers[0]} \n 2. ${correctAnswers[1]} \n 3. ${correctAnswers[2]}`)
}

window.onload = () => loadPage("home")