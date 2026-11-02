(() => {
  const API_BASE = window.location.origin;
  const $ = (selector) => document.querySelector(selector);
  const trigger = $("#videoModelTrigger"), label = $("#videoModelTriggerLabel"), list = $("#videoModelList");
  const prompt = $("#videoPromptInput"), input = $("#videoReferenceInput"), dropZone = $("#videoDropZone"), refs = $("#videoReferencePreview");
  const refLabel = $("#videoReferenceLabel"), resolutions = $("#videoResolutionOptions"), durations = $("#videoDurationOptions");
  const rangeWrap = $("#videoDurationRangeWrap"), range = $("#videoDurationRange"), rangeValue = $("#videoDurationValue");
  const audioSetting = $("#videoAudioSetting"), audioToggle = $("#videoAudioToggle"), voiceSetting = $("#videoVoiceSetting"), voiceToggle = $("#videoVoiceToggle");
  const price = $("#videoPrice"), error = $("#videoError"), button = $("#generateVideoButton");
  const placeholder = $("#videoPlaceholder"), loading = $("#videoLoading"), loadingText = $("#videoLoadingText"), output = $("#videoOutput"), resultInfo = $("#videoResultInfo");
  let videoModels = [], videoSelectedModelId = null, videoModel = null, videoSelectedResolution = null, videoSelectedDuration = null;
  let videoAudioEnabled = false, videoVoiceControlEnabled = false, videoReferenceFileIds = [], priceTimer = null, latestPrice = null, modelsLoaded = false;

  function showError(message) { error.textContent = message; error.hidden = false; }
  function clearError() { error.hidden = true; }
  function setPanel(tabName) {
    document.querySelectorAll(".app-tab").forEach((tab) => { const active = tab.dataset.tab === tabName; tab.classList.toggle("active", active); tab.setAttribute("aria-selected", String(active)); });
    document.querySelectorAll(".app-panel").forEach((panel) => panel.classList.toggle("active", panel.id === `${tabName}Panel`));
  }
  async function loadVideoModels() {
    if (modelsLoaded) return;
    try { videoModels = await (await fetch(`${API_BASE}/api/video-models`)).json(); modelsLoaded = true; renderModelList(); }
    catch (exception) { showError(exception.message || "Video modelleri yüklenemedi."); }
  }
  document.addEventListener("click", (event) => {
    const tab = event.target.closest(".app-tab"); if (!tab) return;
    event.stopImmediatePropagation(); setPanel(tab.dataset.tab); if (tab.dataset.tab === "video") loadVideoModels();
  }, true);

  function renderModelList() {
    list.innerHTML = "";
    videoModels.forEach((model) => {
      const item = document.createElement("li"); item.textContent = `${model.label} (${model.provider})`; item.onclick = () => selectModel(model); list.append(item);
    });
    if (videoModels[0]) selectModel(videoModels[0]);
  }
  function selectModel(model) {
    videoSelectedModelId = model.id; videoModel = model; label.textContent = `${model.label} (${model.provider})`;
    [...list.children].forEach((item) => item.classList.toggle("selected", item.textContent === label.textContent)); list.hidden = true;
    videoReferenceFileIds = []; refs.innerHTML = ""; input.value = ""; videoAudioEnabled = false; videoVoiceControlEnabled = false; audioToggle.checked = false; voiceToggle.checked = false;
    renderModelSettings();
  }
  function optionButton(container, text, selected, handler) {
    const item = document.createElement("button"); item.type = "button"; item.textContent = text; item.className = "aspect-option" + (selected ? " is-selected" : ""); item.onclick = handler; container.append(item);
  }
  function renderModelSettings() {
    if (!videoModel) return;
    const referenceMode = videoModel.input_mode === "reference_to_video";
    refLabel.textContent = referenceMode ? `Referans görseller (en fazla ${videoModel.max_reference_images})` : "Başlangıç görseli";
    input.multiple = referenceMode; input.disabled = false; dropZone.classList.remove("is-disabled");
    resolutions.innerHTML = ""; videoSelectedResolution = videoModel.resolutions[0];
    videoModel.resolutions.forEach((resolution, index) => optionButton(resolutions, resolution, index === 0, () => { videoSelectedResolution = resolution; [...resolutions.children].forEach((button) => button.classList.remove("is-selected")); resolutions.children[index].classList.add("is-selected"); updatePrice(); }));
    durations.innerHTML = ""; rangeWrap.classList.add("is-hidden");
    if (videoModel.duration.fixed_options) {
      videoSelectedDuration = videoModel.duration.fixed_options[0];
      videoModel.duration.fixed_options.forEach((duration, index) => optionButton(durations, `${duration}sn`, index === 0, () => { videoSelectedDuration = duration; [...durations.children].forEach((button) => button.classList.remove("is-selected")); durations.children[index].classList.add("is-selected"); updatePrice(); }));
    } else {
      const limits = videoModel.duration; videoSelectedDuration = limits.min; range.min = limits.min; range.max = limits.max; range.step = limits.step || 1; range.value = limits.min; rangeValue.textContent = `${limits.min} sn`; rangeWrap.classList.remove("is-hidden");
    }
    audioSetting.classList.toggle("is-hidden", !videoModel.supports_audio); voiceSetting.classList.toggle("is-hidden", !(videoModel.supports_audio && videoModel.supports_voice_control)); syncVoiceState(); updatePrice();
  }
  function syncVoiceState() { voiceSetting.classList.toggle("is-disabled", !videoAudioEnabled); if (!videoAudioEnabled) { videoVoiceControlEnabled = false; voiceToggle.checked = false; } }
  range.oninput = () => { videoSelectedDuration = Number(range.value); rangeValue.textContent = `${videoSelectedDuration} sn`; updatePrice(); };
  audioToggle.onchange = () => { videoAudioEnabled = audioToggle.checked; syncVoiceState(); updatePrice(); };
  voiceToggle.onchange = () => { videoVoiceControlEnabled = voiceToggle.checked; updatePrice(); };

  async function uploadReferences(files) {
    const incoming = [...files]; if (!incoming.length || !videoModel) return;
    const capacity = videoModel.max_reference_images - videoReferenceFileIds.length;
    if (incoming.length > capacity) { showError(`Bu model en fazla ${videoModel.max_reference_images} referans kabul eder.`); return; }
    clearError();
    for (const file of incoming) {
      if (!file.type.startsWith("image/")) { showError("Lütfen yalnızca görsel dosyası seçin."); continue; }
      const form = new FormData(); form.append("file", file);
      try {
        const response = await fetch(`${API_BASE}/api/upload-reference`, { method: "POST", body: form }); const data = await response.json(); if (!response.ok) throw Error(data.detail);
        videoReferenceFileIds.push(data.file_id); addThumbnail(file, data.file_id);
      } catch (exception) { showError(exception.message || "Referans görseli yüklenemedi."); }
    }
    input.value = ""; updatePrice();
  }
  function addThumbnail(file, fileId) {
    const item = document.createElement("div"), image = document.createElement("img"), remove = document.createElement("button"); item.className = "video-reference-item"; image.src = URL.createObjectURL(file); image.alt = "Referans"; remove.type = "button"; remove.textContent = "×";
    remove.onclick = () => { videoReferenceFileIds = videoReferenceFileIds.filter((id) => id !== fileId); URL.revokeObjectURL(image.src); item.remove(); updatePrice(); }; item.append(image, remove); refs.append(item);
  }
  input.onchange = () => uploadReferences(input.files);
  dropZone.addEventListener("dragover", (event) => { event.preventDefault(); dropZone.classList.add("is-dragging"); });
  dropZone.addEventListener("dragleave", () => dropZone.classList.remove("is-dragging"));
  dropZone.addEventListener("drop", (event) => { event.preventDefault(); dropZone.classList.remove("is-dragging"); uploadReferences(event.dataTransfer.files); });

  function updatePrice() {
    clearTimeout(priceTimer); priceTimer = setTimeout(async () => {
      if (!videoModel || !videoSelectedResolution || !videoSelectedDuration) return;
      const query = new URLSearchParams({ model_id: videoSelectedModelId, resolution: videoSelectedResolution, duration: videoSelectedDuration, audio: videoAudioEnabled, voice_control: videoVoiceControlEnabled, num_references: videoReferenceFileIds.length });
      try { latestPrice = await (await fetch(`${API_BASE}/api/estimate-video-price?${query}`)).json(); const amount = latestPrice.estimated_usd; price.textContent = amount == null ? "Tahmini maliyet: hesaplanamadı" : `Tahmini maliyet: ~$${Number(amount).toFixed(3)}${latestPrice.unverified ? " ⚠" : ""}`; price.title = latestPrice.unverified ? "Bu fiyat doğrulanmadı, gerçek maliyet farklı olabilir" : ""; price.classList.remove("is-hidden", "price-pulse"); void price.offsetWidth; price.classList.add("price-pulse"); }
      catch (exception) { price.classList.add("is-hidden"); }
    }, 200);
  }
  trigger.onclick = (event) => { event.stopPropagation(); list.hidden = !list.hidden; };
  list.onclick = (event) => event.stopPropagation(); document.addEventListener("click", () => { list.hidden = true; });
  button.onclick = async () => {
    if (!videoModel) return showError("Bir video modeli seçin."); if (!prompt.value.trim()) return showError("Video üretmek için bir prompt yazın.");
    if (!videoReferenceFileIds.length) return showError(videoModel.input_mode === "reference_to_video" ? "En az bir referans görseli ekleyin." : "Bir başlangıç görseli ekleyin.");
    clearError(); button.disabled = true; placeholder.classList.add("is-hidden"); output.classList.add("is-hidden"); resultInfo.classList.add("is-hidden"); loading.classList.remove("is-hidden");
    const startedAt = performance.now(); let interval = setInterval(() => { loadingText.textContent = `Video üretiliyor... ${Math.floor((performance.now() - startedAt) / 1000)} sn`; }, 1000);
    try {
      const body = { model_id: videoSelectedModelId, prompt: prompt.value.trim(), resolution: videoSelectedResolution, duration: videoSelectedDuration, audio: videoAudioEnabled, voice_control: videoVoiceControlEnabled };
      if (videoModel.input_mode === "image_to_video") body.starting_image_file_id = videoReferenceFileIds[0]; else body.reference_file_ids = videoReferenceFileIds;
      const response = await fetch(`${API_BASE}/api/generate-video`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }); const data = await response.json(); if (!response.ok) throw Error(data.detail);
      output.src = `${API_BASE}${data.output_url}?t=${Date.now()}`; output.classList.remove("is-hidden"); const cost = data.estimated_cost?.estimated_usd; resultInfo.textContent = `Üretim süresi: ${data.generation_time_seconds} sn • Model: ${videoModel.label} • Tahmini maliyet: ${cost == null ? "hesaplanamadı" : `~$${Number(cost).toFixed(3)}`}`; resultInfo.classList.remove("is-hidden");
    } catch (exception) { placeholder.classList.remove("is-hidden"); showError(exception.message || "Video üretilemedi."); }
    finally { clearInterval(interval); loadingText.textContent = "Video üretiliyor..."; loading.classList.add("is-hidden"); button.disabled = false; }
  };
})();
