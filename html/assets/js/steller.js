const answerEl = document.getElementById('chat-answer');
const promptEl = document.getElementById('chat-input');
const buttonEl = document.getElementById('chat-send');

function addNewQuestion() {
    let logsEl = document.createElement('p');
    logsEl.classList.add('chat-log');
    logsEl.innerText = "I'm thinking..."
    answerEl.appendChild(logsEl);

    fetch('http://localhost:8000/' + promptEl.value, {
        method: 'POST'
        })
        .then(response => {
        return response.json();
        })
        .then(data => {
            console.log(data);
            logsEl.innerText = "You : \"" + promptEl.value + "\"\n\nMy answer: " + data;
    });

    promptEl.innerText = "";
    promptEl.ariaPlaceholder = "Anything else ?";
};