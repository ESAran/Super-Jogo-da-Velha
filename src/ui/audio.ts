export class GameAudio {
  private context: AudioContext | null = null;
  private enabled = true;

  isEnabled(): boolean {
    return this.enabled;
  }

  toggle(): boolean {
    this.enabled = !this.enabled;
    if (this.enabled) {
      this.playSequence([220, 330], 0.045, "square", 0.025);
    }
    return this.enabled;
  }

  move(playerIndex: number): void {
    this.playSequence(playerIndex === 0 ? [180, 240] : [260, 190], 0.055, "square", 0.035);
  }

  miniWon(): void {
    this.playSequence([220, 330, 440], 0.06, "sawtooth", 0.03);
  }

  win(): void {
    this.playSequence([196, 247, 294, 392, 494], 0.105, "square", 0.04);
  }

  error(): void {
    this.playSequence([130, 92], 0.08, "sawtooth", 0.025);
  }

  select(): void {
    this.playSequence([280], 0.04, "square", 0.018);
  }

  private getContext(): AudioContext | null {
    if (!this.enabled) {
      return null;
    }

    this.context ??= new AudioContext();
    return this.context;
  }

  private playSequence(
    frequencies: number[],
    duration: number,
    type: OscillatorType,
    volume: number,
  ): void {
    const context = this.getContext();
    if (context === null) {
      return;
    }

    const start = context.currentTime;

    frequencies.forEach((frequency, index) => {
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      const noteStart = start + index * duration * 0.82;

      oscillator.type = type;
      oscillator.frequency.setValueAtTime(frequency, noteStart);
      gain.gain.setValueAtTime(volume, noteStart);
      gain.gain.exponentialRampToValueAtTime(0.0001, noteStart + duration);

      oscillator.connect(gain);
      gain.connect(context.destination);
      oscillator.start(noteStart);
      oscillator.stop(noteStart + duration);
    });
  }
}
