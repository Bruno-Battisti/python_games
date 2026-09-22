"""Jogo da Velha (Tic-Tac-Toe) com interface gráfica em Tkinter."""
import tkinter as tk
from tkinter import messagebox

LINHAS_VITORIA = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # linhas
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colunas
    (0, 4, 8), (2, 4, 6),             # diagonais
]


class JogoDaVelha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha")
        self.root.resizable(False, False)

        self.jogador_atual = "X"
        self.tabuleiro = [""] * 9
        self.botoes = []
        self.jogo_ativo = True

        self.label_status = tk.Label(
            root, text=f"Vez de: {self.jogador_atual}", font=("Arial", 16)
        )
        self.label_status.grid(row=0, column=0, columnspan=3, pady=10)

        frame_tabuleiro = tk.Frame(root)
        frame_tabuleiro.grid(row=1, column=0, columnspan=3)

        for i in range(9):
            botao = tk.Button(
                frame_tabuleiro,
                text="",
                font=("Arial", 24, "bold"),
                width=4,
                height=2,
                command=lambda i=i: self.jogar(i),
            )
            botao.grid(row=i // 3, column=i % 3)
            self.botoes.append(botao)

        botao_reiniciar = tk.Button(
            root, text="Reiniciar", font=("Arial", 12), command=self.reiniciar
        )
        botao_reiniciar.grid(row=2, column=0, columnspan=3, pady=10)

    def jogar(self, indice):
        if not self.jogo_ativo or self.tabuleiro[indice] != "":
            return

        self.tabuleiro[indice] = self.jogador_atual
        self.botoes[indice].config(text=self.jogador_atual)

        vencedor = self.checar_vencedor()
        if vencedor:
            self.jogo_ativo = False
            self.label_status.config(text=f"{vencedor} venceu!")
            messagebox.showinfo("Fim de jogo", f"O jogador {vencedor} venceu!")
        elif "" not in self.tabuleiro:
            self.jogo_ativo = False
            self.label_status.config(text="Empate!")
            messagebox.showinfo("Fim de jogo", "Empate!")
        else:
            self.jogador_atual = "O" if self.jogador_atual == "X" else "X"
            self.label_status.config(text=f"Vez de: {self.jogador_atual}")

    def checar_vencedor(self):
        for a, b, c in LINHAS_VITORIA:
            if self.tabuleiro[a] and self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c]:
                return self.tabuleiro[a]
        return None

    def reiniciar(self):
        self.tabuleiro = [""] * 9
        self.jogador_atual = "X"
        self.jogo_ativo = True
        self.label_status.config(text=f"Vez de: {self.jogador_atual}")
        for botao in self.botoes:
            botao.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    JogoDaVelha(root)
    root.mainloop()
