export const baseUrl = "https://babyfalcon.ru";

export function initTg() {
  let tg = window.Telegram.WebApp;
  tg.expand();
  return tg;
}

export function getUserId() {
  return parseInt(document.getElementById("user-id").innerText);
}

export function placeBackButton(tg, route) {
  tg.BackButton.show();

  tg.BackButton.onClick(() => {
    window.location.assign(`${baseUrl}${route}${getUserId()}`);
  });
}
