import { initTg, getUserId, baseUrl } from "../main.js";

let tg = initTg();
tg.BackButton.hide();
const userId = getUserId();

const curLen = document.getElementById("cur-len");
const del_button = document.getElementById("del");

del_button.addEventListener("click", (ev) => {
  tg.showConfirm(
    "Все сообщения будут безвозвратно удалены! Продолжить?",
    (confirmed) => {
      if (confirmed) {
        resetHistory();
        curLen.innerText = "0";
        tg.showAlert("История была успешно очищена.");
      }
    }
  );
});

function resetHistory() {
  fetch(`${baseUrl}/db/update-user-data/`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: userId,
      settings: {
        history: [],
      },
    }),
  });
}
// const container = document.querySelector(".container");
// const stats = document.getElementById("stats");
// const change_button = document.getElementById("change");
// const history_button = document.getElementById("history");
// const del_button = document.getElementById("reset");
// const change_page = document.getElementById("change-page");
// const history_page = document.getElementById("history-page");

// function closeMenu() {
//   container.classList.add("hidden");
// }

// change_button.addEventListener("click", (ev) => {
//   closeMenu();
//   change_page.classList.remove("hidden");
// });

// history_button.addEventListener("click", (ev) => {
//   closeMenu();
//   history_page.classList.remove("hidden");
// });

// del_button.addEventListener("click", (ev) => {
//   tg.showConfirm("Вы уверены?", (confirmed) => {});
// });

// const slider = document.getElementById("new-len");
// function initValue() {
//   let val = parseInt(document.querySelector("#max-len").innerHTML);
//   slider.value = val;
//   return val;
// }

// let val = initValue();

// slider.addEventListener(
//   "input",
//   (ev) => {
//     tg.MainButton.show();
//   },
//   { once: true }
// );

// slider.addEventListener("input", (ev) => {
//   output.value = ev.target.value;
//   val = ev.target.value;
// });

// tg.onEvent("mainButtonClicked", () => {
//   tg.sendData(val);
// });
