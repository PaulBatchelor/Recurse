let answer = document.getElementById("answer");
let spoiler = document.getElementById("spoiler");
let question = document.getElementById("question");
let btn_yes = document.getElementById("btn_yes");
let btn_no = document.getElementById("btn_no");
var card_pos = 0;
let main = document.getElementById("main");

var flashcards = []
// let flashcards = [
//     {
//         question: "Question for first card?",
//         answer: "Answer for first card"
//     },
//     {
//         question: "Question for second card?",
//         answer: "Answer for second card"
//     },
// ];

let results = Array(flashcards.length);

function updateCard(pos) {
    if (pos >= flashcards.length) {
        let end_of_cards = document.createElement('div');
        let p = document.createElement('p');
        p.innerText = 'Oops no more cards';
        let restart = document.createElement('input');
        restart.type = 'button';
        restart.value = 'restart';
        restart.addEventListener('click', () => {
            card_pos = 0;
            console.log(results);
            updateCard(0);
            document.body.innerHTML='';
            document.body.appendChild(main);
        });
        end_of_cards.appendChild(p);
        end_of_cards.appendChild(restart);
        document.body.innerHTML='';
        document.body.appendChild(end_of_cards);
        return;
    }
    spoiler.open = false;
    question.textContent = flashcards[pos].question
    answer.innerText = flashcards[pos].answer
}

btn_yes.addEventListener("click", () => {
    console.log("yes");
    results[card_pos] = true;
    card_pos += 1
    updateCard(card_pos)
});

btn_no.addEventListener("click", () => {
    console.log("no");
    results[card_pos] = false;
    card_pos += 1
    updateCard(card_pos)
});


async function load_flashcards() {
    flashcards = await fetch('http://localhost:8001/v1/get/flashcards')
        .then(response => response.json())
    console.log(flashcards)
    updateCard(0)
}

load_flashcards()