const input = document.querySelector("#image-input");
const dropZone = document.querySelector(".drop-zone");
const previewBox = document.querySelector(".preview-box");
const previewImage = document.querySelector("#preview-image");
const details = document.querySelector("#file-details");
const analyzeButton = document.querySelector("#analyze-button");
const errorMessage = document.querySelector("#upload-error");
let selectedFile = null;

const cropIcons = {Apple:"🍎", Blueberry:"🫐", Cherry:"🍒", Corn:"🌽", Grape:"🍇", Orange:"🍊", Peach:"🍑", Pepper:"🌶️", Potato:"🥔", Raspberry:"🍓", Soybean:"🫘", Squash:"🎃", Strawberry:"🍓", Tomato:"🍅"};
const cropNames = ["Apple","Blueberry","Cherry","Corn","Grape","Orange","Peach","Pepper","Potato","Raspberry","Soybean","Squash","Strawberry","Tomato"];
document.querySelector("#crop-grid").innerHTML = cropNames.map(name => `<div class="crop-tile"><span>${cropIcons[name] || "🌿"}</span><b>${name}</b></div>`).join("");

function showError(message) { errorMessage.textContent = message; }
function handleFile(file) {
  showError("");
  if (!file) return;
  const validTypes = ["image/jpeg", "image/png"];
  if (!validTypes.includes(file.type) || !/\.(jpe?g|png)$/i.test(file.name)) return showError("Please choose a JPG, JPEG, or PNG image.");
  if (file.size > 5 * 1024 * 1024) return showError("That image is larger than the 5 MB limit.");
  selectedFile = file;
  previewImage.src = URL.createObjectURL(file);
  previewImage.onload = () => URL.revokeObjectURL(previewImage.src);
  previewBox.classList.add("has-image");
  details.textContent = `${file.name} · ${(file.size / 1024).toFixed(1)} KB`;
  analyzeButton.disabled = false;
  document.querySelector("#status-badge").textContent = "Ready to analyze";
}
dropZone.addEventListener("click", event => { if (!event.target.closest("button")) input.click(); });
dropZone.addEventListener("keydown", event => { if (event.key === "Enter" || event.key === " ") input.click(); });
input.addEventListener("change", event => handleFile(event.target.files[0]));
["dragenter","dragover"].forEach(type => dropZone.addEventListener(type, event => { event.preventDefault(); dropZone.classList.add("dragging"); }));
["dragleave","drop"].forEach(type => dropZone.addEventListener(type, event => { event.preventDefault(); dropZone.classList.remove("dragging"); }));
dropZone.addEventListener("drop", event => handleFile(event.dataTransfer.files[0]));

function prettyName(value) { return value.replace(/___/g, " · ").replace(/_/g, " ").replace(/\s+/g, " ").replace(/\(including sour\)/g, "").trim(); }
function renderResults(data) {
  const confidence = Number(data.confidence) * 100;
  const rec = data.recommendations;
  const topRows = data.top_predictions.map((item, index) => `<div class="prediction-row"><span>${index + 1}. ${prettyName(item.class_name)}</span><b>${(Number(item.confidence) * 100).toFixed(1)}%</b></div><div class="bar"><i style="width:${Number(item.confidence) * 100}%"></i></div>`).join("");
  const care = rec ? `<div class="recommendation"><h4>♧ Recommended Treatment</h4><p>${rec.description}</p><ul>${rec.organic_control.slice(0, 2).map(item => `<li>${item}</li>`).join("")}</ul></div>` : `<div class="recommendation"><h4>♧ Recommended Treatment</h4><p>Recommendations are not currently available for this class.</p></div>`;
  document.querySelector("#result-content").innerHTML = `<div class="diagnosis"><img class="diagnosis-thumb" src="${previewImage.src}" alt=""><div><h4>${rec ? rec.disease_name : prettyName(data.predicted_class)}</h4><small>${rec ? rec.crop : "Supported crop"} · ${confidence.toFixed(1)}% confidence</small></div></div><div class="confidence"><div class="confidence-row"><span>Model confidence</span><b>${confidence.toFixed(1)}%</b></div><div class="bar"><i style="width:${confidence}%"></i></div></div><h4 class="top-title">Top 3 predictions</h4>${topRows}${care}`;
  document.querySelector("#result-empty").hidden = true;
  document.querySelector("#result-content").hidden = false;
}
analyzeButton.addEventListener("click", async () => {
  if (!selectedFile) return showError("Choose an image before analyzing.");
  analyzeButton.disabled = true;
  analyzeButton.innerHTML = "Analyzing your leaf... <span>◌</span>";
  document.querySelector("#status-badge").textContent = "Analyzing";
  try {
    const formData = new FormData(); formData.append("image", selectedFile);
    const response = await fetch("/predict", { method: "POST", body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed.");
    renderResults(data);
    document.querySelector("#status-badge").textContent = "Complete";
    document.querySelector("#result-status").textContent = "Analysis complete";
  } catch (error) {
    showError(error.message);
    document.querySelector("#status-badge").textContent = "Try again";
  } finally { analyzeButton.disabled = false; analyzeButton.innerHTML = "Analyze Disease <span>→</span>"; }
});
document.querySelector(".menu-button").addEventListener("click", event => { const links = document.querySelector(".nav-links"); const open = links.classList.toggle("open"); event.currentTarget.setAttribute("aria-expanded", open); });
