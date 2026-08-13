export function speakText(text: string) {
  if (typeof window === "undefined") {
    return;
  }
  if (!window.speechSynthesis) {
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "es-ES";
  utterance.rate = 0.92;
  window.speechSynthesis.speak(utterance);
}
