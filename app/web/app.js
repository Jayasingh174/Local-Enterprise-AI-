const out = document.getElementById("out"); 
const tx = document.getElementById("tx"); 
const msg = document.getElementById("msg"); 
const useRag = document.getElementById("useRag"); 
document.getElementById("btnIngest").onclick = async () => { 
out.textContent = "Ingesting..."; 
const r = await fetch("/ingest", { method: "POST" }); 
const j = await r.json(); 
out.textContent = JSON.stringify(j, null, 2); 
}; 
document.getElementById("btnSend").onclick = async () => { 
out.textContent = "Thinking..."; 
const r = await fetch("/chat", { 
method: "POST", 
headers: { "Content-Type": "application/json" }, 
body: JSON.stringify({ message: msg.value, use_rag: useRag.checked }) 
}); 
const j = await r.json();
out.textContent = j.answer || JSON.stringify(j, null, 2); 
window.__lastAnswer = j.answer || ""; 
}; 
document.getElementById("btnSpeak").onclick = async () => { 
const text = window.__lastAnswer || ""; 
if (!text) return; 
const r = await fetch("/tts", { 
method: "POST", 
headers: { "Content-Type": "application/json" }, 
body: JSON.stringify({ text }) 
}); 
const j = await r.json(); 
if (!j.ok) { out.textContent = JSON.stringify(j, null, 2); return; } 
const audio = new Audio(j.audio_url); 
audio.play(); 
}; 
// Voice recording 
let mediaRecorder; 
let chunks = []; 
const btnRec = document.getElementById("btnRec"); 
const btnStop = document.getElementById("btnStop");
btnRec.onclick = async () => { 
chunks = []; 
const stream = await navigator.mediaDevices.getUserMedia({ audio: true }); 
mediaRecorder = new MediaRecorder(stream); 
mediaRecorder.ondataavailable = (e) => chunks.push(e.data); 
mediaRecorder.onstop = async () => { 
const blob = new Blob(chunks, { type: "audio/webm" }); 
const file = new File([blob], "voice.webm", { type: "audio/webm" }); 
const fd = new FormData(); 
fd.append("file", file); 
tx.textContent = "Transcribing..."; 
const r = await fetch("/stt", { method: "POST", body: fd }); 
const j = await r.json(); 
tx.textContent = j.text || "(no transcript)"; 
// Auto send transcript to chat 
msg.value = j.text || ""; 
document.getElementById("btnSend").click(); 
}; 
mediaRecorder.start(); 
btnRec.disabled = true; 
btnStop.disabled = false;
}; 
btnStop.onclick = () => { 
mediaRecorder.stop(); 
btnRec.disabled = false; 
btnStop.disabled = true; 
}; 
