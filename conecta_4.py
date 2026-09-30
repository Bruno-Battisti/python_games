"""Jogo Conecta 4 (Connect Four) com interface gráfica em Tkinter."""
import tkinter as tk
from tkinter import messagebox

LINHAS = 6
COLUNAS = 7

CORES_JOGADOR = {"Vermelho": "red", "Amarelo": "yellow"}
COR_VAZIA = "white"


class Conecta4:
    def __init__(self, root):
        self.root = root
        self.root.title("Conecta 4")
        self.root.resizable(False, False)

        self.label_status = tk.Label(root, text="", font=("Arial", 16))
        self.label_status.grid(row=0, column=0, columnspan=COLUNAS, pady=10)

        self.frame_tabuleiro = tk.Frame(root, bg="blue")
        self.frame_tabuleiro.grid(row=1, column=0, columnspan=COLUNAS, padx=10, pady=10)

        self.celulas = []
        for linha in range(LINHAS):
            linha_celulas = []
            for coluna in range(COLUNAS):
                canvas = tk.Canvas(
                    self.frame_tabuleiro,
                    width=50,
                    height=50,
                    bg="blue",
                    highlightthickness=0,
                )
                canvas.grid(row=linha, column=coluna, padx=2, pady=2)
                circulo = canvas.create_oval(5, 5, 45, 45, fill=COR_VAZIA)
                canvas.bind("<Button-1>", lambda evento, c=coluna: self.jogar(c))
                linha_celulas.append((canvas, circulo))
            self.celulas.append(linha_celulas)

        botao_reiniciar = tk.Button(
            root, text="Reiniciar", font=("Arial", 12), command=self.reiniciar
        )
        botao_reiniciar.grid(row=2, column=0, columnspan=COLUNAS, pady=10)

        self.reiniciar()

    def reiniciar(self):
        self.tabuleiro = [[None] * COLUNAS for _ in range(LINHAS)]
        self.jogador_atual = "Vermelho"
        self.jogo_ativo = True
        self.label_status.config(text=f"Vez de: {self.jogador_atual}")
        for linha_celulas in self.celulas:
            for canvas, circulo in linha_celulas:
                canvas.itemconfig(circulo, fill=COR_VAZIA)

    def coluna_cheia(self, coluna):
        return self.tabuleiro[0][coluna] is not None

    def jogar(self, coluna):
        if not self.jogo_ativo or self.coluna_cheia(coluna):
            return

        for linha in range(LINHAS - 1, -1, -1):
            if self.tabuleiro[linha][coluna] is None:
                self.tabuleiro[linha][coluna] = self.jogador_atual
                canvas, circulo = self.celulas[linha][coluna]
                canvas.itemconfig(circulo, fill=CORES_JOGADOR[self.jogador_atual])
                break

        if self.checar_vencedor(linha, coluna):
            self.jogo_ativo = False
            self.label_status.config(text=f"{self.jogador_atual} venceu!")
            messagebox.showinfo("Fim de jogo", f"O jogador {self.jogador_atual} venceu!")
        elif all(self.coluna_cheia(c) for c in range(COLUNAS)):
            self.jogo_ativo = False
            self.label_status.config(text="Empate!")
            messagebox.showinfo("Fim de jogo", "Empate!")
        else:
            self.jogador_atual = "Amarelo" if self.jogador_atual == "Vermelho" else "Vermelho"
            self.label_status.config(text=f"Vez de: {self.jogador_atual}")

    def checar_vencedor(self, linha, coluna):
        jogador = self.tabuleiro[linha][coluna]
        direcoes = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dl, dc in direcoes:
            contagem = 1
            for sinal in (1, -1):
                l, c = linha + dl * sinal, coluna + dc * sinal
                while 0 <= l < LINHAS and 0 <= c < COLUNAS and self.tabuleiro[l][c] == jogador:
                    contagem += 1
                    l += dl * sinal
                    c += dc * sinal
            if contagem >= 4:
                return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    Conecta4(root)
    root.mainloop()
