"""Batalha Naval (Battleship) com interface gráfica em Tkinter."""
import random
import tkinter as tk
from tkinter import messagebox

TAMANHO_TABULEIRO = 8
TAMANHOS_NAVIOS = [4, 3, 3, 2, 2]


class BatalhaNaval:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalha Naval")
        self.root.resizable(False, False)

        self.label_status = tk.Label(root, text="", font=("Arial", 12))
        self.label_status.grid(row=0, column=0, columnspan=TAMANHO_TABULEIRO, pady=10)

        self.frame_tabuleiro = tk.Frame(root)
        self.frame_tabuleiro.grid(row=1, column=0, columnspan=TAMANHO_TABULEIRO)

        botao_reiniciar = tk.Button(
            root, text="Novo Jogo", font=("Arial", 10), command=self.reiniciar
        )
        botao_reiniciar.grid(row=2, column=0, columnspan=TAMANHO_TABULEIRO, pady=10)

        self.botoes = {}
        self.reiniciar()

    def reiniciar(self):
        for botao in self.botoes.values():
            botao.destroy()
        self.botoes = {}

        self.navios = set()
        self.atingidos = set()
        self.tentativas = set()
        self.jogo_ativo = True
        self.posicionar_navios()
        self.label_status.config(text="Encontre todos os navios inimigos!")

        for linha in range(TAMANHO_TABULEIRO):
            for coluna in range(TAMANHO_TABULEIRO):
                botao = tk.Button(
                    self.frame_tabuleiro,
                    text="",
                    font=("Arial", 10, "bold"),
                    width=3,
                    height=1,
                    bg="lightblue",
                    command=lambda l=linha, c=coluna: self.atacar(l, c),
                )
                botao.grid(row=linha, column=coluna)
                self.botoes[(linha, coluna)] = botao

    def posicionar_navios(self):
        self.navios = set()
        for tamanho in TAMANHOS_NAVIOS:
            while True:
                horizontal = random.choice([True, False])
                if horizontal:
                    linha = random.randint(0, TAMANHO_TABULEIRO - 1)
                    coluna = random.randint(0, TAMANHO_TABULEIRO - tamanho)
                    celulas = {(linha, coluna + i) for i in range(tamanho)}
                else:
                    linha = random.randint(0, TAMANHO_TABULEIRO - tamanho)
                    coluna = random.randint(0, TAMANHO_TABULEIRO - 1)
                    celulas = {(linha + i, coluna) for i in range(tamanho)}

                if not self._colide_ou_encosta(celulas):
                    self.navios.update(celulas)
                    break

    def _colide_ou_encosta(self, celulas):
        for (linha, coluna) in celulas:
            for dl in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if (linha + dl, coluna + dc) in self.navios:
                        return True
        return False

    def atacar(self, linha, coluna):
        if not self.jogo_ativo or (linha, coluna) in self.tentativas:
            return

        self.tentativas.add((linha, coluna))
        botao = self.botoes[(linha, coluna)]

        if (linha, coluna) in self.navios:
            self.atingidos.add((linha, coluna))
            botao.config(text="X", bg="red", state="disabled", disabledforeground="white")
            if self.navios.issubset(self.atingidos):
                self.jogo_ativo = False
                self.label_status.config(text="Você venceu!")
                messagebox.showinfo("Fim de jogo", "Você afundou toda a frota inimiga!")
            else:
                restantes = len(self.navios) - len(self.atingidos)
                self.label_status.config(text=f"Acertou! Células de navio restantes: {restantes}")
        else:
            botao.config(text="•", bg="darkblue", state="disabled", disabledforeground="white")
            self.label_status.config(text="Água...")


if __name__ == "__main__":
    root = tk.Tk()
    BatalhaNaval(root)
    root.mainloop()
