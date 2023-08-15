import { initTg, getUserId, baseUrl, placeBackButton } from "../main.js";

let tg = initTg();
placeBackButton(tg, "/pages/history-menu/");

const container = document.querySelector(".container");
const slider = document.getElementById("range");
const curLen = document.getElementById("cur-len");
const maxLen = document.getElementById("max-len");

function initLenValue(element) {
  let maxLenValue = parseInt(element.innerText);
  slider.value = maxLenValue;
  return maxLenValue;
}

const curLenValue = initLenValue(curLen);
let maxLenValue = initLenValue(maxLen);

slider.addEventListener(
  "input",
  (ev) => {
    tg.MainButton.show();
  },
  { once: true }
);

let valuesAreMessed = false;

function reactiveDataGeneration(ev) {
  maxLen.innerText = String(ev.target.value);
  maxLenValue = ev.target.value;
  if (curLenValue > maxLenValue) {
    curLen.innerText = String(ev.target.value);
    if (valuesAreMessed === false) {
      valuesAreMessed = true;
      showAlertMessage();
    }
  } else if (valuesAreMessed) {
    curLen.innerText = curLenValue;
    valuesAreMessed = false;
    hideAlertMessage();
  }
}

function initAlertMessage() {
  const alertMessage = document.createElement("p");
  alertMessage.id = "alertMessage";
  alertMessage.classList.add("alarm");
  alertMessage.innerText = `ВНИМАНИЕ!
  Новое максимльное значение меньше количества сохранённых сообщений в истории.
  После сохранения в истории останутся только n последних сообщений!`;
  return alertMessage;
}

const alertMessage = initAlertMessage();

function showAlertMessage() {
  container.appendChild(alertMessage);
  curLen.classList.add("alarm");
}

function hideAlertMessage() {
  container.removeChild(alertMessage);
  curLen.classList.remove("alarm");
}

slider.addEventListener("input", reactiveDataGeneration);

const userId = getUserId();

tg.MainButton.text = "СОХРАНИТЬ";
tg.onEvent("mainButtonClicked", async () => {
  await fetch(`${baseUrl}/pages/post-change-history-limit/`, {
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: userId,
      settings: { history_size: maxLenValue },
    }),
  });
  // await tg.MainButton.showProgress();
  // await initNewHistorySettings(maxLenValue);
  // await tg.MainButton.hideProgress();
  window.location.href = `${baseUrl}/pages/history-menu/${userId}`;
});

// async function initNewHistorySettings(newLen) {
//   if (valuesAreMessed) {
//     const historyJson = await getHistory();
//     const newHistory = historyJson.slice(curLenValue - newLen);
//     await setHistory(newLen, newHistory);
//   } else {
//     await tg.showAlert("else");
//     await setHistory(newLen, null);
//   }
// }

// async function getHistory() {
//   let res = await fetch(`${baseUrl}/db/get-user-data/`, {
//     method: "post",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       id: userId,
//     }),
//   });
//   const json = await res.json();

//   return json.settings.history;
// }

// async function setHistory(newLen, history) {
//   const settings = { history_size: newLen };

//   if (history !== null) {
//     settings.history = history;
//   }

//   await fetch(`${baseUrl}/db/update-user-data/`, {
//     method: "post",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       id: userId,
//       settings,
//     }),
//   });
// }
