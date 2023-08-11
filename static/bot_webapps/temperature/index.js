import { initTg, getUserId, baseUrl } from "../main.js";

let tg = initTg();
const slider = document.getElementById("temp");
const output = document.getElementById("t-out");

function initValue() {
  let tempValue = output.value;
  slider.value = tempValue;
  return tempValue;
}

let tempValue = initValue();

slider.addEventListener(
  "input",
  (ev) => {
    tg.MainButton.show();
  },
  { once: true }
);

slider.addEventListener("input", (ev) => {
  output.value = ev.target.value;
  tempValue = ev.target.value;
});

tg.MainButton.text = "СОХРАНИТЬ";
tg.onEvent("mainButtonClicked", () => {
  tg.sendData(tempValue);
});
