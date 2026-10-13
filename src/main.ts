import "./styles.css";
import { GameApp } from "./ui/app";

const root = document.querySelector<HTMLElement>("#app");

if (root === null) {
  throw new Error("Elemento principal da aplicacao nao encontrado.");
}

new GameApp(root);
