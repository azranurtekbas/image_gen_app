(() => {
  const button = document.querySelector("#generate-button");
  const image = document.querySelector("#output-image");
  const stage = document.querySelector(".output-stage");
  if (!button || !image || !stage) return;

  const info = document.createElement("p");
  info.className = "result-info is-hidden";
  stage.after(info);
  let startedAt = 0;
  let modelLabel = "";
  let estimatedPrice = null;

  button.addEventListener("click", () => {
    startedAt = performance.now();
    modelLabel = document.querySelector("#modelTriggerLabel")?.textContent || "Model";
    const priceText = document.querySelector(".price-display")?.textContent || "";
    estimatedPrice = priceText.replace(/^Tahmini maliyet:\s*/, "") || "doğrulanmadı";
    info.classList.add("is-hidden");
  });
  image.addEventListener("load", () => {
    if (image.classList.contains("is-hidden") || !startedAt) return;
    const seconds = ((performance.now() - startedAt) / 1000).toFixed(1);
    info.textContent = `Üretim süresi: ${seconds} sn • Model: ${modelLabel} • Tahmini maliyet: ${estimatedPrice}`;
    info.classList.remove("is-hidden");
  });
})();
