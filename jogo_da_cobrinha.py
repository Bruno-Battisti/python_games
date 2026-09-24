"""Jogo da Cobrinha (Snake) com interface gráfica em Tkinter."""
import random
import tkinter as tk
from tkinter import messagebox

COLUNAS = 20
LINHAS = 20
TAMANHO_CELULA = 20
VELOCIDADE_INICIAL = 120

DIRECOES_OPOSTAS = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
DELTAS = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}
TECLAS = {
    "Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right",
    "w": "Up", "s": "Down", "a": "Left", "d": "Right",
}


class JogoDaCobrinha:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Cobrinha")
        self.root.resizable(False, False)

        self.label_status = tk.Label(root, text="", font=("Arial", 14))
        self.label_status.grid(row=0, column=0, pady=10)

        self.canvas = tk.Canvas(
            root,
            width=COLUNAS * TAMANHO_CELULA,
            height=LINHAS * TAMANHO_CELULA,
            bg="black",
        )
        self.canvas.grid(row=1, column=0)

        botao_reiniciar = tk.Button(
            root, text="Reiniciar", font=("Arial", 12), command=self.reiniciar
        )
        botao_reiniciar.grid(row=2, column=0, pady=10)

        self.root.bind("<Key>", self.mudar_direcao)

        self.after_id = None
        self.reiniciar()

    def reiniciar(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)

        centro = (COLUNAS // 2, LINHAS // 2)
        self.cobra = [centro, (centro[0] - 1, centro[1]), (centro[0] - 2, centro[1])]
        self.direcao = "Right"
        self.proxima_direcao = "Right"
        self.pontos = 0
        self.jogo_ativo = True
        self.velocidade = VELOCIDADE_INICIAL
        self.comida = self.gerar_comida()

        self.label_status.config(text=f"Pontos: {self.pontos}")
        self.desenhar()
        self.after_id = self.root.after(self.velocidade, self.mover)

    def gerar_comida(self):
        celulas_livres = [
            (c, l)
            for c in range(COLUNAS)
            for l in range(LINHAS)
            if (c, l) not in self.cobra
        ]
        return random.choice(celulas_livres)

    def mudar_direcao(self, evento):
        nova_direcao = TECLAS.get(evento.keysym)
        if nova_direcao is None:
            return
        if nova_direcao == DIRECOES_OPOSTAS.get(self.direcao):
            return
        self.proxima_direcao = nova_direcao

    def mover(self):
        if not self.jogo_ativo:
            return

        self.direcao = self.proxima_direcao
        dx, dy = DELTAS[self.direcao]
        cabeca_x, cabeca_y = self.cobra[0]
        nova_cabeca = (cabeca_x + dx, cabeca_y + dy)

        colidiu_parede = not (0 <= nova_cabeca[0] < COLUNAS and 0 <= nova_cabeca[1] < LINHAS)
        colidiu_corpo = nova_cabeca in self.cobra

        if colidiu_parede or colidiu_corpo:
            self.jogo_ativo = False
            self.label_status.config(text=f"Fim de jogo! Pontos: {self.pontos}")
            messagebox.showinfo("Fim de jogo", f"Você perdeu! Pontuação final: {self.pontos}")
            return

        self.cobra.insert(0, nova_cabeca)
        if nova_cabeca == self.comida:
            self.pontos += 1
            self.label_status.config(text=f"Pontos: {self.pontos}")
            self.comida = self.gerar_comida()
            self.velocidade = max(60, VELOCIDADE_INICIAL - self.pontos * 4)
        else:
            self.cobra.pop()

        self.desenhar()
        self.after_id = self.root.after(self.velocidade, self.mover)

    def desenhar(self):
        self.canvas.delete("all")

        for i, (x, y) in enumerate(self.cobra):
            cor = "lime" if i == 0 else "green"
            self.canvas.create_rectangle(
                x * TAMANHO_CELULA,
                y * TAMANHO_CELULA,
                (x + 1) * TAMANHO_CELULA,
                (y + 1) * TAMANHO_CELULA,
                fill=cor,
                outline="black",
            )

        fx, fy = self.comida
        self.canvas.create_oval(
            fx * TAMANHO_CELULA,
            fy * TAMANHO_CELULA,
            (fx + 1) * TAMANHO_CELULA,
            (fy + 1) * TAMANHO_CELULA,
            fill="red",
            outline="black",
        )


if __name__ == "__main__":
    root = tk.Tk()
    JogoDaCobrinha(root)
    root.mainloop()
