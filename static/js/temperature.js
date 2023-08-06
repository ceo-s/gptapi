let tg = window.Telegram.WebApp;
tg.expand();

tg.showConfirm("DAta", tg.colorScheme);

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

tg.onEvent("mainButtonClicked", () => {
  tg.sendData(tempValue);
});
