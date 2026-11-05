/* Lightweight screenshot viewer; native dialog handles Escape and focus trapping. */
(() => {
  const triggers = document.querySelectorAll("a[data-project-lightbox]");
  if (!triggers.length || typeof HTMLDialogElement === "undefined") return;

  const dialog = document.createElement("dialog");
  dialog.className = "projectLightbox";
  dialog.setAttribute("aria-label", "Enlarged project screenshot");
  dialog.innerHTML = `<div class="projectLightboxInner">
    <button class="projectLightboxClose" type="button" aria-label="Close image viewer">Close</button>
    <img alt="" />
    <p class="projectLightboxCaption"></p>
  </div>`;
  document.body.append(dialog);

  const image = dialog.querySelector("img");
  const caption = dialog.querySelector(".projectLightboxCaption");
  const closeButton = dialog.querySelector(".projectLightboxClose");
  let returnTo = null;

  triggers.forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      if (typeof dialog.showModal !== "function") return;
      event.preventDefault();
      returnTo = trigger;
      image.src = trigger.href;
      image.alt = trigger.querySelector("img")?.alt || "Project screenshot";
      caption.textContent = image.alt;
      dialog.showModal();
      closeButton.focus();
    });
  });
  closeButton.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener("close", () => {
    image.removeAttribute("src");
    if (returnTo && returnTo.isConnected) returnTo.focus();
    returnTo = null;
  });
})();
