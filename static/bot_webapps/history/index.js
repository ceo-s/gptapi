import { initTg, placeBackButton } from "../main.js";

let tg = initTg();
placeBackButton(tg, "/pages/history-menu/");
// const container = document.querySelector(".container");
// const history = document.getElementById("history");
// const userId = getUserId();

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

//   console.log(json);
//   return json.settings.history;
// }

// const historyJson = await getHistory();

// async function generateHistoryRepresentation() {
//   // const items = document.createElement("div");
//   const items = document.createDocumentFragment();
//   items.id = "history";

//   historyJson.forEach((el) => {
//     let item = document.createElement("div");
//     item.classList.add("history-item");
//     let itemRole = document.createElement("h3");
//     itemRole.classList.add("history-itemRole");
//     let itemContent = document.createElement("p");
//     itemContent.classList.add("history-itemContent");

//     if (el.role == "assistant") {
//       itemRole.innerText = "Чат-бот:";
//     } else {
//       itemRole.innerText = el.name.concat(":");
//     }
//     itemContent.innerText = el.content;
//     item.appendChild(itemRole);
//     item.appendChild(itemContent);
//     items.appendChild(item);
//   });
//   return items;
// }

// const historyFragment = await generateHistoryRepresentation();
// history.appendChild(historyFragment);
