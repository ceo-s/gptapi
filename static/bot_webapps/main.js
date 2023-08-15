export const baseUrl = "https://4657-188-243-182-231.ngrok-free.app";

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
