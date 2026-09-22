"""Campo Minado (Minesweeper) com interface gráfica em Tkinter."""
import random
import tkinter as tk
from tkinter import messagebox

LINHAS = 9
COLUNAS = 9
NUM_MINAS = 10

CORES_NUMEROS = {
    1: "blue", 2: "green", 3: "red", 4: "purple",
    5: "maroon", 6: "cyan", 7: "black", 8: "gray",
}


class CampoMinado:
    def __init__(self, root):
        self.root = root
        self.root.title("Campo Minado")
        self.root.resizable(False, False)

        self.label_status = tk.Label(root, text="", font=("Arial", 12))
        self.label_status.grid(row=0, column=0, columnspan=COLUNAS, pady=10)

        self.frame_tabuleiro = tk.Frame(root)
        self.frame_tabuleiro.grid(row=1, column=0, columnspan=COLUNAS)

        botao_reiniciar = tk.Button(
            root, text="Novo Jogo", font=("Arial", 10), command=self.reiniciar
        )
        botao_reiniciar.grid(row=2, column=0, columnspan=COLUNAS, pady=10)

        self.botoes = {}
        self.reiniciar()

    def reiniciar(self):
        for botao in self.botoes.values():
            botao.destroy()
        self.botoes = {}

        self.minas = set()
        self.reveladas = set()
        self.marcadas = set()
        self.jogo_ativo = True
        self.primeiro_clique = True
        self.label_status.config(text=f"Minas: {NUM_MINAS}")

        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                botao = tk.Button(
                    self.frame_tabuleiro,
                    text="",
                    font=("Arial", 10, "bold"),
                    width=2,
                    height=1,
                )
                botao.grid(row=linha, column=coluna)
                botao.bind("<Button-1>", lambda e, l=linha, c=coluna: self.revelar(l, c))
                botao.bind("<Button-3>", lambda e, l=linha, c=coluna: self.marcar(l, c))
                self.botoes[(linha, coluna)] = botao

    def posicionar_minas(self, linha_segura, coluna_segura):
        celulas_seguras = {
            (l, c)
            for l in range(linha_segura - 1, linha_segura + 2)
            for c in range(coluna_segura - 1, coluna_segura + 2)
        }
        candidatas = [
            (l, c)
            for l in range(LINHAS)
            for c in range(COLUNAS)
            if (l, c) not in celulas_seguras
        ]
        self.minas = set(random.sample(candidatas, NUM_MINAS))

    def contar_minas_vizinhas(self, linha, coluna):
        return sum(
            (l, c) in self.minas
            for l in range(linha - 1, linha + 2)
            for c in range(coluna - 1, coluna + 2)
            if (l, c) != (linha, coluna)
        )

    def revelar(self, linha, coluna):
        if not self.jogo_ativo or (linha, coluna) in self.marcadas:
            return
        if (linha, coluna) in self.reveladas:
            return

        if self.primeiro_clique:
            self.posicionar_minas(linha, coluna)
            self.primeiro_clique = False

        if (linha, coluna) in self.minas:
            self.jogo_ativo = False
            self.revelar_minas()
            self.label_status.config(text="Você perdeu!")
            messagebox.showinfo("Fim de jogo", "Você clicou em uma mina!")
            return

        self._revelar_em_cascata(linha, coluna)
        self.checar_vitoria()

    def _revelar_em_cascata(self, linha, coluna):
        if (linha, coluna) in self.reveladas:
            return
        if not (0 <= linha < LINHAS and 0 <= coluna < COLUNAS):
            return

        self.reveladas.add((linha, coluna))
        num_minas = self.contar_minas_vizinhas(linha, coluna)
        botao = self.botoes[(linha, coluna)]
        botao.config(relief="sunken", state="disabled", disabledforeground=CORES_NUMEROS.get(num_minas, "black"))

        if num_minas > 0:
            botao.config(text=str(num_minas))
        else:
            botao.config(text="")
            for l in range(linha - 1, linha + 2):
                for c in range(coluna - 1, coluna + 2):
                    if (l, c) != (linha, coluna):
                        self._revelar_em_cascata(l, c)

    def marcar(self, linha, coluna):
        if not self.jogo_ativo or (linha, coluna) in self.reveladas:
            return

        botao = self.botoes[(linha, coluna)]
        if (linha, coluna) in self.marcadas:
            self.marcadas.remove((linha, coluna))
            botao.config(text="")
        else:
            self.marcadas.add((linha, coluna))
            botao.config(text="🚩")

    def revelar_minas(self):
        for (linha, coluna) in self.minas:
            self.botoes[(linha, coluna)].config(text="💣", background="red")

    def checar_vitoria(self):
        total_celulas = LINHAS * COLUNAS
        if len(self.reveladas) == total_celulas - NUM_MINAS:
            self.jogo_ativo = False
            self.label_status.config(text="Você venceu!")
            messagebox.showinfo("Fim de jogo", "Parabéns, você desarmou o campo!")


if __name__ == "__main__":
    root = tk.Tk()
    CampoMinado(root)
    root.mainloop()
