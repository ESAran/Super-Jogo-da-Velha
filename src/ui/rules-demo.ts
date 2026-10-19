const steps = [
  ["Comece onde quiser", "Na primeira jogada, X pode escolher qualquer casa de qualquer mini tabuleiro.", "X começa • escolha livre"],
  ["X marcou no canto superior direito", "Veja a casa rosa: sua posição indica o destino de O. Não importa em qual mini tabuleiro X estava.", "Casa marcada → próximo tabuleiro"],
  ["O joga no mini do canto superior direito", "O contorno azul mostra onde O deve jogar. Dentro dele, O pode escolher qualquer casa vazia.", "O joga • mini superior direito"],
  ["O marcou no centro. X vai para o centro", "A regra se repete a cada turno: a casa escolhida manda o adversário para o mini tabuleiro da mesma posição.", "X joga • mini central"],
];

export function rulesDemoFrame(step: number): string {
  const [title, description, status] = steps[step];
  return `<div class="lesson-board" role="img" aria-label="${status}. X marca a casa superior direita do mini central; O responde no centro do mini superior direito.">${Array.from({length: 9}, (_, mini) => `<div class="lesson-mini ${step === 0 ? 'available' : (step === 2 && mini === 2) || (step === 3 && mini === 4) ? 'destination' : ''}">${Array.from({length: 9}, (_, cell) => {
    const x = mini === 4 && cell === 2 && step >= 1;
    const o = mini === 2 && cell === 4 && step >= 3;
    return `<span class="lesson-cell ${x ? 'mark-x' : o ? 'mark-o' : ''}">${x ? 'X' : o ? 'O' : ''}</span>`;
  }).join('')}</div>`).join('')}</div><div class="lesson-explanation"><span class="lesson-kicker">NA PRÁTICA • ${step + 1} / 4</span><h2>${title}</h2><p>${description}</p><div class="lesson-status">${status}</div><div class="lesson-dots" aria-hidden="true">${steps.map((_, i) => `<i class="${i === step ? 'current' : ''}"></i>`).join('')}</div></div>`;
}

export function mountRulesDemo(root: HTMLElement): () => void {
  const frame = root.querySelector<HTMLElement>('[data-lesson-frame]');
  const play = root.querySelector<HTMLButtonElement>('[data-lesson-play]');
  if (!frame || !play) return () => {};
  let step = 0;
  let timer: ReturnType<typeof setInterval> | undefined;
  const paint = () => { frame.innerHTML = rulesDemoFrame(step); };
  const pause = () => { clearInterval(timer); timer = undefined; play.textContent = '▶ Reproduzir'; };
  const start = () => { timer = setInterval(() => { step = (step + 1) % steps.length; paint(); }, 4500); play.textContent = 'Ⅱ Pausar'; };
  play.onclick = () => timer === undefined ? start() : pause();
  root.querySelector<HTMLButtonElement>('[data-lesson-next]')!.onclick = () => { pause(); step = (step + 1) % steps.length; paint(); };
  root.querySelector<HTMLButtonElement>('[data-lesson-reset]')!.onclick = () => { pause(); step = 0; paint(); };
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) start();
  return pause;
}
