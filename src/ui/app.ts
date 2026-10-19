import { mountRulesDemo, rulesDemoFrame } from "./rules-demo";
import { GameEngine, Player } from "../game/engine";
import { BasicMachineStrategy, MachineStrategy, MachineDifficulty, MediumMachineStrategy } from "../game/machine";
import { GameAudio } from "./audio";

type Screen = "menu" | "setup" | "game" | "rules" | "history" | "credits" | "achievements";

interface HistoryEntry {
  id: string;
  playerOne: string;
  playerTwo: string;
  winner: string | null;
  winnerKind?: "human" | "machine";
  playedAt: string;
}

const HISTORY_KEY = "sjv84.history.v1";
const SAY_MY_NAME_KEY = "sjv84.achievement.say-my-name.v1";
const UNNAMED_KEY = "sjv84.achievement.unnamed.v1";
const TOTAL_WINS_KEY = "sjv84.total-wins.v1";
const TEN_WINS_KEY = "sjv84.achievement.ten-wins.v1";
const BOMBONERA_KEY = "sjv84.achievement.vasco-na-bombonera.v1";

function escapeHtml(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export class GameApp {
  private readonly root: HTMLElement;
  private readonly audio = new GameAudio();
  private disposeRulesDemo: (() => void) | undefined;
  private screen: Screen = "menu";
  private game: GameEngine | null = null;
  private machineMode = false;
  private difficulty: MachineDifficulty = "easy";
  private readonly mediumStrategy = new MediumMachineStrategy();
  private machineTimer: ReturnType<typeof setTimeout> | null = null;
  private lastMove: { mini: number; cell: number } | null = null;
  private matchSaved = false;
  private notice = "";
  private sayMyNameUnlocked = this.readAchievement(SAY_MY_NAME_KEY);
  private unnamedUnlocked = this.readAchievement(UNNAMED_KEY);
  private totalWins = this.readTotalWins();
  private tenWinsUnlocked = this.readAchievement(TEN_WINS_KEY) || this.totalWins >= 10;
  private bomboneraUnlocked = this.readAchievement(BOMBONERA_KEY);

  constructor(root: HTMLElement, private readonly machineStrategy: MachineStrategy = new BasicMachineStrategy()) {
    this.root = root;
    this.bindEvents();
    this.render();
  }

  private bindEvents(): void {
    this.root.addEventListener("click", (event) => {
      const target = event.target;
      if (!(target instanceof Element)) {
        return;
      }

      const button = target.closest<HTMLButtonElement>("button[data-action]");
      if (button === null) {
        return;
      }

      this.handleAction(button);
    });

    this.root.addEventListener("submit", (event) => {
      const form = event.target;
      if (!(form instanceof HTMLFormElement) || !form.matches("[data-player-form]")) {
        return;
      }

      event.preventDefault();
      this.startMatch(new FormData(form));
    });
  }

  private handleAction(button: HTMLButtonElement): void {
    const action = button.dataset.action;

    if (action !== "play-cell") {
      this.audio.select();
    }

    switch (action) {
      case "local-game":
        this.machineMode = false;
        this.goTo("setup");
        break;
      case "machine-game":
        this.machineMode = true;
        this.goTo("setup");
        break;
      case "rules":
      case "history":
      case "credits":
      case "achievements":
        this.goTo(action);
        break;
      case "menu":
        this.cancelMachineTurn();
        this.game = null;
        this.goTo("menu");
        break;
      case "restart":
        this.restartMatch();
        break;
      case "toggle-sound":
        this.audio.toggle();
        this.render();
        break;
      case "play-cell":
        this.playCell(button);
        break;
    }
  }

  private goTo(screen: Screen): void {
    this.screen = screen;
    this.notice = "";
    this.render();
  }

  private startMatch(data: FormData): void {
    try {
      const playerOne = new Player(
        String(data.get("player-one") ?? ""),
        this.machineMode ? "X" : String(data.get("symbol-one") ?? ""),
      );
      const playerTwo = new Player(
        String(data.get("player-two") ?? (this.machineMode ? "Computador" : "")),
        this.machineMode ? "O" : String(data.get("symbol-two") ?? ""),
        this.machineMode ? "machine" : "human",
      );

      const difficulty = this.machineMode ? String(data.get("difficulty") ?? "easy") : "easy";
      if (difficulty !== "easy" && difficulty !== "medium") {
        throw new Error("Essa dificuldade ainda nao esta disponivel.");
      }
      this.difficulty = difficulty;
      this.cancelMachineTurn();
      this.game = new GameEngine(playerOne, playerTwo);
      this.matchSaved = false;
      this.lastMove = null;
      this.notice = "SISTEMA SINCRONIZADO // JOGADOR 1 INICIA";
      const unlockedNames: string[] = [];
      if (
        !this.sayMyNameUnlocked &&
        [playerOne, playerTwo].some((player) => player.name.toLowerCase() === "heisenberg")
      ) {
        this.sayMyNameUnlocked = true;
        try {
          localStorage.setItem(SAY_MY_NAME_KEY, "true");
        } catch {
          // Mantem a conquista nesta sessao mesmo sem armazenamento disponivel.
        }
        unlockedNames.push("Say my name.");
      }
      if (
        !this.unnamedUnlocked &&
        [playerOne, playerTwo].some((player) => player.name.toLowerCase() === "valdemort")
      ) {
        this.unnamedUnlocked = true;
        try {
          localStorage.setItem(UNNAMED_KEY, "true");
        } catch {
          // Mantem a conquista nesta sessao mesmo sem armazenamento disponivel.
        }
        unlockedNames.push("AQUELE QUE NÃO DEVE SER NOMEADO");
      }
      if (unlockedNames.length > 0) {
        this.notice = `CONQUISTA LIBERADA // ${unlockedNames.join(" // ")}`;
      }
      this.screen = "game";
      this.render();
    } catch (error) {
      this.audio.error();
      this.notice = error instanceof Error ? error.message : "Falha ao iniciar partida.";
      this.render();
    }
  }

  private restartMatch(): void {
    if (this.game === null) {
      return;
    }

    this.cancelMachineTurn();
    this.game = new GameEngine(
      new Player(this.game.playerOne.name, this.game.playerOne.symbol, this.game.playerOne.kind),
      new Player(this.game.playerTwo.name, this.game.playerTwo.symbol, this.game.playerTwo.kind),
    );
    this.matchSaved = false;
    this.lastMove = null;
    this.notice = "NOVA RODADA INICIALIZADA";
    this.render();
  }

  private cancelMachineTurn(): void {
    if (this.machineTimer !== null) clearTimeout(this.machineTimer);
    this.machineTimer = null;
  }

  private isMachineTurn(): boolean {
    return this.game !== null && !this.game.finished && this.game.currentPlayer.kind === "machine";
  }

  private scheduleMachineTurn(): void {
    if (!this.isMachineTurn() || this.machineTimer !== null) return;
    const game = this.game;
    this.machineTimer = setTimeout(() => {
      this.machineTimer = null;
      if (this.game !== game || this.screen !== "game" || !this.isMachineTurn()) return;
      const strategy = this.difficulty === "medium" ? this.mediumStrategy : this.machineStrategy;
      const move = strategy.chooseMove(game!);
      if (move !== null) this.performMove(move.mini, move.cell);
    }, 700);
  }

  private playCell(button: HTMLButtonElement): void {
    if (this.game === null || this.isMachineTurn()) return;
    this.performMove(Number(button.dataset.mini), Number(button.dataset.cell));
  }

  private performMove(mini: number, cell: number): void {
    if (this.game === null) return;
    const playerIndex = this.game.currentPlayer === this.game.playerOne ? 0 : 1;

    try {
      const result = this.game.play(mini, cell);
      this.lastMove = { mini, cell };
      this.audio.move(playerIndex);

      if (result.gameWon) {
        this.notice = "SEQUENCIA MESTRA CONFIRMADA";
        this.audio.win();
      } else if (result.draw) {
        this.notice = "SISTEMA SATURADO // EMPATE";
      } else if (result.miniWon) {
        this.notice = "SETOR DOMINADO";
        this.audio.miniWon();
      } else {
        this.notice = result.nextRequiredMini === null
          ? "DESTINO LIVRE // ESCOLHA UM SETOR"
          : `ROTA FIXADA // SETOR ${result.nextRequiredMini + 1}`;
      }

      if (this.game.finished && !this.matchSaved) {
        this.saveCurrentMatch();
      }

      this.scheduleMachineTurn();
      this.render();
    } catch (error) {
      this.audio.error();
      this.notice = error instanceof Error ? error.message : "Jogada invalida.";
      this.render();
    }
  }

  private saveCurrentMatch(): void {
    if (this.game === null || !this.game.finished || this.matchSaved) {
      return;
    }

    const history = this.readHistory();
    history.unshift({
      id: crypto.randomUUID(),
      playerOne: this.game.playerOne.name,
      playerTwo: this.game.playerTwo.name,
      winner: this.game.winner?.name ?? null,
      winnerKind: this.game.winner?.kind,
      playedAt: new Date().toISOString(),
    });

    this.matchSaved = true;
    const unlockedNames: string[] = [];
    if (this.game.winner !== null && this.game.winner.kind === "human") {
      this.totalWins += 1;
      if (!this.tenWinsUnlocked && this.totalWins >= 10) {
        this.tenWinsUnlocked = true;
        unlockedNames.push("LIÃO!");
      }
      const winner = this.game.winner;
      const opponent = winner === this.game.playerOne ? this.game.playerTwo : this.game.playerOne;
      const quadrants = this.game.board.getMacroCells();
      const winnerQuadrants = quadrants.filter((symbol) => symbol === winner.symbol).length;
      const opponentQuadrants = quadrants.filter((symbol) => symbol === opponent.symbol).length;
      if (
        !this.bomboneraUnlocked &&
        winner.name.toLowerCase() === "vasco" &&
        opponent.name.toLowerCase() === "boca" &&
        winnerQuadrants < opponentQuadrants
      ) {
        this.bomboneraUnlocked = true;
        unlockedNames.push("Vasco na Bombonera");
      }
    }
    if (unlockedNames.length > 0) {
      this.notice = `CONQUISTA LIBERADA // ${unlockedNames.join(" // ")}`;
    }

    try {
      localStorage.setItem(TOTAL_WINS_KEY, String(this.totalWins));
      if (this.tenWinsUnlocked) {
        localStorage.setItem(TEN_WINS_KEY, "true");
      }
      if (this.bomboneraUnlocked) {
        localStorage.setItem(BOMBONERA_KEY, "true");
      }
      localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 20)));
    } catch {
      // O jogo continua funcionando mesmo quando o navegador bloqueia armazenamento local.
    }
  }

  private readTotalWins(): number {
    const historyWins = this.readHistory().filter((entry) => typeof entry?.winner === "string" && entry.winnerKind !== "machine").length;
    try {
      const saved = Number(localStorage.getItem(TOTAL_WINS_KEY));
      return Number.isSafeInteger(saved) && saved >= 0 ? Math.max(saved, historyWins) : historyWins;
    } catch {
      return historyWins;
    }
  }

  private readAchievement(key: string): boolean {
    try {
      return localStorage.getItem(key) === "true";
    } catch {
      return false;
    }
  }

  private readHistory(): HistoryEntry[] {
    try {
      const stored = localStorage.getItem(HISTORY_KEY);
      if (stored === null) {
        return [];
      }

      const parsed: unknown = JSON.parse(stored);
      return Array.isArray(parsed) ? (parsed as HistoryEntry[]) : [];
    } catch {
      return [];
    }
  }

  private render(): void {
    this.disposeRulesDemo?.();
    let content = "";

    switch (this.screen) {
      case "menu":
        content = this.renderMenu();
        break;
      case "setup":
        content = this.renderSetup();
        break;
      case "game":
        content = this.renderGame();
        break;
      case "rules":
        content = this.renderRules();
        break;
      case "history":
        content = this.renderHistory();
        break;
      case "credits":
        content = this.renderCredits();
        break;
      case "achievements":
        content = this.renderAchievements();
        break;
    }

    this.root.innerHTML = `
      <div class="noise" aria-hidden="true"></div>
      <div class="scanlines" aria-hidden="true"></div>
      <main class="shell">
        ${this.renderHeader()}
        ${content}
      </main>
    `;
    this.disposeRulesDemo = this.screen === "rules" ? mountRulesDemo(this.root) : undefined;
  }

  private renderHeader(): string {
    const soundLabel = this.audio.isEnabled() ? "SOM: ON" : "SOM: OFF";

    return `
      <header class="system-header">
        <div class="brand-lockup">
          <span class="eyebrow">REDE LOCAL</span>
          <h1 class="glitch" data-text="SUPER JOGO DA VELHA">SUPER JOGO DA VELHA</h1>
        </div>
        <button class="sound-toggle" data-action="toggle-sound" type="button" aria-label="Alternar som">
          <span class="status-dot ${this.audio.isEnabled() ? "is-on" : ""}"></span>${soundLabel}
        </button>
      </header>
    `;
  }

  private renderMenu(): string {
    return `
      <section class="menu-layout">
        <div class="hero-copy">
          <p class="signal">SINAL DETECTADO // 09 SETORES ATIVOS</p>
          <h2>Super Jogo<br>da Velha</h2>
          <p class="hero-subtitle">Nove jogos.<br><em>Uma guerra.</em></p>
          <p class="intro">
            Cada movimento reprograma o destino do adversario. Domine tres setores
            antes que o sistema domine voce.
          </p>
          <div class="version-line"><span></span>WEB 1.0.0 // SEM CONEXAO EXTERNA</div>
        </div>

        <nav class="main-menu" aria-label="Menu principal">
          <button class="menu-option is-primary" data-action="local-game" type="button">
            <span class="option-code">01</span>
            <span><strong>JOGADOR VS JOGADOR</strong><small>duelo local // iniciar</small></span>
            <span class="option-arrow">↗</span>
          </button>
          <button class="menu-option" data-action="machine-game" type="button">
            <span class="option-code">02</span>
            <span><strong>JOGADOR VS MAQUINA</strong><small>duelo contra o computador // iniciar</small></span>
            <span class="option-arrow">↗</span>
          </button>
          <div class="menu-grid">
            <button data-action="rules" type="button">REGRAS</button>
            <button data-action="history" type="button">ARQUIVO</button>
            <button data-action="achievements" type="button">CONQUISTAS</button>
            <button data-action="credits" type="button">CREDITOS</button>
          </div>
          ${this.renderNotice()}
        </nav>
      </section>
    `;
  }

  private renderSetup(): string {
    return `
      <section class="panel setup-panel">
        <div class="panel-heading">
          <span>CONFIGURACAO DE IDENTIDADE</span>
          <strong>${this.machineMode ? "VS MAQUINA" : "01 / 02"}</strong>
        </div>
        <form class="player-form" data-player-form>
          <fieldset class="player-config player-one">
            <legend>JOGADOR 1</legend>
            <label>NOME DE OPERADOR<input name="player-one" maxlength="18" value="Godric" required /></label>
            <label>SIMBOLO<input name="symbol-one" maxlength="1" value="X" ${this.machineMode ? "readonly" : ""} required /></label>
          </fieldset>
          <div class="versus-mark">VS</div>
          <fieldset class="player-config player-two">
            <legend>${this.machineMode ? "COMPUTADOR" : "JOGADOR 2"}</legend>
            <label>NOME DE OPERADOR<input name="player-two" maxlength="18" value="${this.machineMode ? "Computador" : "Salazar"}" required /></label>
            <label>SIMBOLO<input name="symbol-two" maxlength="1" value="O" ${this.machineMode ? "readonly" : ""} required /></label>
          </fieldset>
          ${this.machineMode ? `
          <fieldset class="player-config difficulty-config">
            <legend>DIFICULDADE</legend>
            <label>NIVEL DO COMPUTADOR
              <select name="difficulty" aria-describedby="difficulty-help">
                <option value="easy" ${this.difficulty === "easy" ? "selected" : ""}>Fácil</option>
                <option value="medium" ${this.difficulty === "medium" ? "selected" : ""}>Médio</option>
                <option value="hard" disabled>Difícil — em breve</option>
              </select>
            </label>
            <small id="difficulty-help">Fácil: conquistar e bloquear. Médio: também conecta peças e avalia o próximo destino.</small>
          </fieldset>` : ""}
          <div class="form-actions">
            <button class="ghost-button" data-action="menu" type="button">← CANCELAR</button>
            <button class="launch-button" type="submit">INICIAR PARTIDA <span>↗</span></button>
          </div>
        </form>
        ${this.renderNotice()}
      </section>
    `;
  }

  private renderGame(): string {
    if (this.game === null) {
      this.screen = "menu";
      return this.renderMenu();
    }

    const game = this.game;
    const requiredText = game.requiredMini === null ? "LIVRE" : String(game.requiredMini + 1).padStart(2, "0");

    return `
      <section class="game-layout">
        <aside class="game-sidebar left-sidebar">
          ${this.renderPlayerCard(game.playerOne, game.currentPlayer === game.playerOne, 1)}
          ${this.renderPlayerCard(game.playerTwo, game.currentPlayer === game.playerTwo, 2)}
          <div class="route-panel">
            <span>PROXIMO SETOR</span>
            <strong>${requiredText}</strong>
            <small>${game.requiredMini === null ? "rota aberta" : "destino obrigatorio"}</small>
          </div>
          <button class="ghost-button full" data-action="menu" type="button">ABORTAR PARTIDA</button>
        </aside>

        <div class="board-stage">
          <div class="board-meta"><span>GRADE PRINCIPAL // 3×3</span><b>${game.finished ? "PARTIDA ENCERRADA" : this.isMachineTurn() ? "MAQUINA ESCOLHENDO JOGADA..." : "SUA VEZ DE MARCAR"}</b></div>
          <div class="ultimate-board" role="grid" aria-label="Super Jogo da Velha">
            ${game.board.getMiniBoards().map((_, index) => this.renderMiniBoard(index)).join("")}
          </div>
          ${this.renderNotice()}
        </div>

        <aside class="game-sidebar right-sidebar">
          <div class="macro-panel">
            <div class="panel-heading compact"><span>MAPA DE DOMINIO</span><strong>9X</strong></div>
            <div class="macro-board">
              ${game.board.getMacroCells().map((cell, index) => `
                <div class="macro-cell ${cell === null && game.board.getMini(index).isClosed() ? "is-draw" : ""} ${this.symbolClass(cell)}">
                  ${cell === null ? (game.board.getMini(index).isClosed() ? "·" : index + 1) : escapeHtml(cell)}
                </div>
              `).join("")}
            </div>
          </div>
          <div class="telemetry">
            <span>ESTADO</span>
            <strong>${game.finished ? "ENCERRADO" : "EM CURSO"}</strong>
            <span>PROTOCOLO</span>
            <strong>ULTIMATE / ${game.playerTwo.kind === "machine" ? `MAQUINA / ${this.difficulty === "medium" ? "MÉDIO" : "FÁCIL"}` : "LOCAL"}</strong>
          </div>
        </aside>

        ${game.finished ? this.renderOutcome() : ""}
      </section>
    `;
  }

  private renderPlayerCard(player: Player, active: boolean, number: number): string {
    return `
      <div class="player-card player-${number} ${active ? "is-active" : ""}">
        <div><span>OPERADOR 0${number}</span><i>${active ? "ATIVO" : "AGUARDE"}</i></div>
        <strong>${escapeHtml(player.symbol)}</strong>
        <p>${escapeHtml(player.name)}</p>
      </div>
    `;
  }

  private renderMiniBoard(miniIndex: number): string {
    if (this.game === null) {
      return "";
    }

    const mini = this.game.board.getMini(miniIndex);
    const winner = mini.getWinner();
    const playable = !this.game.finished && (
      this.game.requiredMini === null ||
      this.game.requiredMini === miniIndex ||
      !this.game.rules.isMiniAvailable(this.game.board, this.game.requiredMini)
    ) && !mini.isClosed();

    return `
      <section class="mini-board ${playable ? "is-playable" : ""} ${winner !== null ? `is-won ${this.symbolClass(winner)}` : ""}" aria-label="Mini tabuleiro ${miniIndex + 1}">
        <span class="mini-index">0${miniIndex + 1}</span>
        ${mini.getCells().map((cell, cellIndex) => {
          const valid = !this.isMachineTurn() && (this.game?.isMoveValid(miniIndex, cellIndex) ?? false);
          const last = this.lastMove?.mini === miniIndex && this.lastMove.cell === cellIndex;
          return `
            <button
              class="game-cell ${this.symbolClass(cell)} ${last ? "is-last" : ""}"
              data-action="play-cell"
              data-mini="${miniIndex}"
              data-cell="${cellIndex}"
              type="button"
              aria-label="Setor ${miniIndex + 1}, posicao ${cellIndex + 1}${cell === null ? "" : `, marcada com ${escapeHtml(cell)}`}"
              ${valid ? "" : "disabled"}
            ><span>${cell === null ? "" : escapeHtml(cell)}</span></button>
          `;
        }).join("")}
        ${winner === null ? "" : `<div class="mini-winner" aria-hidden="true">${escapeHtml(winner)}</div>`}
      </section>
    `;
  }

  private renderOutcome(): string {
    if (this.game === null) {
      return "";
    }

    const title = this.game.draw ? "EMPATE DE SISTEMA" : "DOMINIO TOTAL";
    const message = this.game.winner === null
      ? "Todos os setores foram encerrados sem uma sequencia mestre."
      : `${escapeHtml(this.game.winner.name)} venceu com o simbolo ${escapeHtml(this.game.winner.symbol)}.`;

    return `
      <div class="outcome-backdrop">
        <div class="outcome-card">
          <span>TRANSMISSAO FINALIZADA</span>
          <h2>${title}</h2>
          <p>${message}</p>
          <div>
            <button class="ghost-button" data-action="menu" type="button">MENU</button>
            <button class="launch-button" data-action="restart" type="button">JOGAR NOVAMENTE ↗</button>
          </div>
        </div>
      </div>
    `;
  }

  private renderRules(): string {
    return this.renderInfoPanel(
      "COMO JOGAR",
      `
        <header class="rules-intro"><span class="lesson-kicker">9 MINI TABULEIROS. UMA GRANDE DISPUTA.</span><h1>Uma jogada decide<br>o próximo destino.</h1><p>Jogue o jogo da velha dentro de cada mini tabuleiro.<br>Conquiste <strong>três minis em linha</strong> para vencer a partida.</p></header>
        <section class="rules-lesson" aria-label="Demonstração das jogadas">
          <div class="lesson-frame" data-lesson-frame>${rulesDemoFrame(0)}</div>
          <div class="lesson-controls"><span>EXEMPLO ANIMADO</span><div><button type="button" data-lesson-play>▶ Reproduzir</button><button type="button" data-lesson-next>Próximo →</button><button type="button" data-lesson-reset aria-label="Reiniciar demonstração">↺</button></div></div>
        </section>
        <h2 class="rules-reference-title">Bateu a dúvida? Consulte aqui.</h2>
        <div class="rules-grid rules-reference">
          <article><b>01 / ONDE JOGAR</b><h3>A casa indica o destino</h3><p>Primeira jogada: qualquer casa. Depois, jogue no mini indicado pela última casa marcada pelo adversário. Escolha uma casa vazia dentro dele.</p></article>
          <article><b>02 / COMO CONQUISTAR</b><h3>Três marcas ganham um mini</h3><p>Faça uma linha, coluna ou diagonal com seu símbolo. Esse mini fica conquistado e não recebe mais jogadas.</p></article>
          <article><b>03 / COMO VENCER</b><h3>Três minis ganham o jogo</h3><p>Conquiste três mini tabuleiros alinhados na horizontal, vertical ou diagonal do tabuleiro grande. Não basta conquistar três em qualquer lugar.</p><div class="lesson-win" aria-label="Exemplo: três mini tabuleiros conquistados por X na primeira linha">${Array.from({length:9}, (_, i) => `<span class="${i < 3 ? 'won' : ''}">${i < 3 ? 'X' : '·'}</span>`).join('')}</div></article>
          <article><b>04 / EXCEÇÕES</b><h3>Destino fechado? Escolha livre.</h3><p>Se o mini de destino já foi conquistado ou empatou, escolha qualquer mini ainda aberto. Um mini cheio sem vencedor fica empatado e não conta para ninguém.</p><p>Se todos os minis fecharem sem três conquistas alinhadas, a partida termina empatada.</p></article>
        </div>
        <aside class="rules-tip"><strong>LEMBRETE RÁPIDO</strong><span>Casa escolhida → mini do adversário.<br>Três casas → um mini. Três minis em linha → vitória.</span></aside>
      `,
    );
  }

  private renderHistory(): string {
    const history = this.readHistory();
    const rows = history.length === 0
      ? `<div class="empty-state"><strong>SEM REGISTROS</strong><p>Conclua uma partida para alimentar o arquivo local.</p></div>`
      : `<div class="history-list">${history.map((entry, index) => `
          <article>
            <span>${String(index + 1).padStart(2, "0")}</span>
            <div><strong>${escapeHtml(entry.playerOne)} × ${escapeHtml(entry.playerTwo)}</strong><small>${new Date(entry.playedAt).toLocaleString("pt-BR")}</small></div>
            <b>${entry.winner === null ? "EMPATE" : `VENCEDOR: ${escapeHtml(entry.winner)}`}</b>
          </article>
        `).join("")}</div>`;

    return this.renderInfoPanel("ARQUIVO DE PARTIDAS", rows);
  }

  private renderAchievements(): string {
    const history = this.readHistory();
    const achievements = [
      { code: "A-01", name: "PRIMEIRO SINAL", detail: "Conclua uma partida", unlocked: history.length >= 1 },
      { code: "A-02", name: "DOMINADOR", detail: "Venca uma partida", unlocked: history.some((entry) => entry.winner !== null && entry.winnerKind !== "machine") },
      { code: "A-03", name: "ARQUIVISTA", detail: "Conclua cinco partidas", unlocked: history.length >= 5 },
      {
        code: "A-04",
        name: this.sayMyNameUnlocked ? "Say my name." : "CONQUISTA SECRETA",
        detail: this.sayMyNameUnlocked ? "Inicie uma partida usando o nome Heisenberg" : "???",
        unlocked: this.sayMyNameUnlocked,
      },
      {
        code: "A-05",
        name: this.unnamedUnlocked ? "AQUELE QUE NÃO DEVE SER NOMEADO" : "CONQUISTA SECRETA",
        detail: this.unnamedUnlocked ? "Inicie uma partida usando o nome valdemort" : "???",
        unlocked: this.unnamedUnlocked,
      },
      { code: "A-06", name: "LIÃO!", detail: "Vença 10 partidas", unlocked: this.tenWinsUnlocked },
      {
        code: "A-07",
        name: this.bomboneraUnlocked ? "Vasco na Bombonera" : "CONQUISTA SECRETA",
        detail: this.bomboneraUnlocked
          ? "Vença como Vasco contra Boca, conquistando menos quadrantes que o adversário"
          : "???",
        unlocked: this.bomboneraUnlocked,
      },
    ];

    return this.renderInfoPanel(
      "CONQUISTAS",
      `<div class="achievement-list">${achievements.map((item) => `
        <article class="${item.unlocked ? "is-unlocked" : ""}">
          <span>${item.code}</span><div><strong>${item.name}</strong><small>${item.detail}</small></div><b>${item.unlocked ? "LIBERADA" : "BLOQUEADA"}</b>
        </article>
      `).join("")}</div>`,
    );
  }

  private renderCredits(): string {
    return this.renderInfoPanel(
      "CREDITOS DO SISTEMA",
      `
        <div class="credits-card">
          <span>PROJETO ORIGINAL E DESENVOLVIMENTO</span>
          <h2>EDUARDO ARAN</h2>
          <p>Super Jogo da Velha nasceu como um projeto Python de terminal e agora opera diretamente no navegador.</p>
          <div><b>ENGINE</b> TYPESCRIPT</div><div><b>INTERFACE</b> HTML / CSS</div><div><b>REDE</b> OFFLINE</div>
        </div>
      `,
    );
  }

  private renderInfoPanel(title: string, content: string): string {
    return `
      <section class="panel info-panel">
        <div class="panel-heading"><span>${title}</span><strong>SYS</strong></div>
        ${content}
        <button class="ghost-button" data-action="menu" type="button">← VOLTAR AO MENU</button>
      </section>
    `;
  }

  private renderNotice(): string {
    if (this.notice.length === 0) {
      return "";
    }

    return `<div class="notice" role="status"><span></span>${escapeHtml(this.notice)}</div>`;
  }

  private symbolClass(symbol: string | null): string {
    if (symbol === null || this.game === null) {
      return "";
    }

    return symbol === this.game.playerOne.symbol ? "symbol-one" : "symbol-two";
  }
}
