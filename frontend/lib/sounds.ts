function playTone(frequency: number, durationMs: number) {
  const AudioWindow = window as Window & {
    webkitAudioContext?: typeof AudioContext;
  };
  const ContextClass = window.AudioContext || AudioWindow.webkitAudioContext;
  if (!ContextClass) {
    return;
  }
  const context = new ContextClass();
  const oscillator = context.createOscillator();
  const gain = context.createGain();
  oscillator.type = "sine";
  oscillator.frequency.value = frequency;
  gain.gain.value = 0.07;
  oscillator.connect(gain);
  gain.connect(context.destination);
  oscillator.start();
  window.setTimeout(function stopTone() {
    oscillator.stop();
    context.close();
  }, durationMs);
}

export function playCorrectSound() {
  playTone(880, 140);
}

export function playWrongSound() {
  playTone(220, 200);
}
