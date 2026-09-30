"""Jogo Sokoban com interface gráfica em Tkinter."""
import tkinter as tk
from tkinter import messagebox

TAMANHO_CELULA = 50

NIVEIS = [
    [
        "#####",
        "# @ #",
        "# $ #",
        "# . #",
        "#####",
    ],
    [
        "#######",
        "#  @  #",
        "# $ $ #",
        "# . . #",
        "#######",
    ],
]

DELTAS = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
TECLAS = {
    "Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right",
    "w": "Up", "s": "Down", "a": "Left", "d": "Right",
}

COR_PAREDE = "#4a4a4a"
COR_CHAO = "#dcd6c8"
COR_ALVO = "#e8b923"
COR_CAIXA = "#8b5e3c"
COR_CAIXA_NO_ALVO = "#2ecc71"
COR_JOGADOR = "#2e86de"


class Sokoban:
    def __init__(self, root):
        self.root = root
        self.root.title("Sokoban")
        self.root.resizable(False, False)

        self.label_status = tk.Label(root, text="", font=("Arial", 14))
        self.label_status.grid(row=0, column=0, pady=10)

        self.canvas = tk.Canvas(root, bg=COR_CHAO, highlightthickness=0)
        self.canvas.grid(row=1, column=0)

        botao_reiniciar = tk.Button(
            root, text="Reiniciar Nível", font=("Arial", 12), command=self.carregar_nivel
        )
        botao_reiniciar.grid(row=2, column=0, pady=10)

        self.root.bind("<Key>", self.mover)

        self.nivel_atual = 0
        self.carregar_nivel()

    def carregar_nivel(self):
        mapa = NIVEIS[self.nivel_atual]
        self.paredes = set()
        self.alvos = set()
        self.caixas = set()
        self.jogador = None

        for linha, texto in enumerate(mapa):
            for coluna, char in enumerate(texto):
                if char == "#":
                    self.paredes.add((linha, coluna))
                elif char == ".":
                    self.alvos.add((linha, coluna))
                elif char == "$":
                    self.caixas.add((linha, coluna))
                elif char == "@":
                    self.jogador = (linha, coluna)
                elif char == "*":
                    self.alvos.add((linha, coluna))
                    self.caixas.add((linha, coluna))
                elif char == "+":
                    self.alvos.add((linha, coluna))
                    self.jogador = (linha, coluna)

        self.linhas = len(mapa)
        self.colunas = max(len(texto) for texto in mapa)
        self.canvas.config(
            width=self.colunas * TAMANHO_CELULA, height=self.linhas * TAMANHO_CELULA
        )

        self.label_status.config(text=f"Nível {self.nivel_atual + 1} de {len(NIVEIS)}")
        self.desenhar()

    def mover(self, evento):
        direcao = TECLAS.get(evento.keysym)
        if direcao is None:
            return

        dl, dc = DELTAS[direcao]
        linha, coluna = self.jogador
        novo_jogador = (linha + dl, coluna + dc)

        if novo_jogador in self.paredes:
            return

        if novo_jogador in self.caixas:
            nova_caixa = (linha + 2 * dl, coluna + 2 * dc)
            if nova_caixa in self.paredes or nova_caixa in self.caixas:
                return
            self.caixas.remove(novo_jogador)
            self.caixas.add(nova_caixa)

        self.jogador = novo_jogador
        self.desenhar()
        self.checar_vitoria()

    def checar_vitoria(self):
        if self.caixas != self.alvos:
            return

        if self.nivel_atual + 1 < len(NIVEIS):
            messagebox.showinfo("Nível completo!", "Você resolveu o nível! Vamos para o próximo.")
            self.nivel_atual += 1
            self.carregar_nivel()
        else:
            messagebox.showinfo("Parabéns!", "Você completou todos os níveis!")

    def desenhar(self):
        self.canvas.delete("all")

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                x0, y0 = coluna * TAMANHO_CELULA, linha * TAMANHO_CELULA
                x1, y1 = x0 + TAMANHO_CELULA, y0 + TAMANHO_CELULA
                cor = COR_PAREDE if (linha, coluna) in self.paredes else COR_CHAO
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor, outline="black")

                if (linha, coluna) in self.alvos:
                    self.canvas.create_oval(
                        x0 + 15, y0 + 15, x1 - 15, y1 - 15, fill=COR_ALVO, outline=""
                    )

                if (linha, coluna) in self.caixas:
                    cor_caixa = COR_CAIXA_NO_ALVO if (linha, coluna) in self.alvos else COR_CAIXA
                    self.canvas.create_rectangle(
                        x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill=cor_caixa, outline="black"
                    )

                if (linha, coluna) == self.jogador:
                    self.canvas.create_oval(
                        x0 + 8, y0 + 8, x1 - 8, y1 - 8, fill=COR_JOGADOR, outline="black"
                    )


if __name__ == "__main__":
    root = tk.Tk()
    Sokoban(root)
    root.mainloop()
