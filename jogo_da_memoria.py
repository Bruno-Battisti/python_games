"""Jogo da Memória com interface gráfica em Tkinter."""
import random
import tkinter as tk
from tkinter import messagebox

EMOJIS = ["🍎", "🍌", "🍇", "🍉", "🍓", "🍒", "🍍", "🥝"]
COSTAS = "❓"


class JogoDaMemoria:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")
        self.root.resizable(False, False)

        self.cartas = EMOJIS + EMOJIS
        random.shuffle(self.cartas)

        self.viradas = []          # índices atualmente virados (no máximo 2)
        self.combinadas = set()    # índices já combinados
        self.aguardando = False    # trava cliques durante a checagem
        self.pares_encontrados = 0

        self.label_status = tk.Label(root, text="Encontre os pares!", font=("Arial", 14))
        self.label_status.grid(row=0, column=0, columnspan=4, pady=10)

        self.botoes = []
        for i in range(16):
            botao = tk.Button(
                root,
                text=COSTAS,
                font=("Arial", 20),
                width=4,
                height=2,
                command=lambda i=i: self.virar(i),
            )
            botao.grid(row=1 + i // 4, column=i % 4)
            self.botoes.append(botao)

        botao_reiniciar = tk.Button(
            root, text="Reiniciar", font=("Arial", 12), command=self.reiniciar
        )
        botao_reiniciar.grid(row=5, column=0, columnspan=4, pady=10)

    def virar(self, indice):
        if self.aguardando or indice in self.combinadas or indice in self.viradas:
            return

        self.botoes[indice].config(text=self.cartas[indice])
        self.viradas.append(indice)

        if len(self.viradas) == 2:
            self.aguardando = True
            self.root.after(600, self.checar_par)

    def checar_par(self):
        i1, i2 = self.viradas
        if self.cartas[i1] == self.cartas[i2]:
            self.combinadas.add(i1)
            self.combinadas.add(i2)
            self.pares_encontrados += 1
            self.label_status.config(text=f"Pares encontrados: {self.pares_encontrados}/8")
        else:
            self.botoes[i1].config(text=COSTAS)
            self.botoes[i2].config(text=COSTAS)

        self.viradas = []
        self.aguardando = False

        if self.pares_encontrados == 8:
            self.label_status.config(text="Você encontrou todos os pares!")
            messagebox.showinfo("Fim de jogo", "Parabéns, você venceu!")

    def reiniciar(self):
        self.cartas = EMOJIS + EMOJIS
        random.shuffle(self.cartas)
        self.viradas = []
        self.combinadas = set()
        self.aguardando = False
        self.pares_encontrados = 0
        self.label_status.config(text="Encontre os pares!")
        for botao in self.botoes:
            botao.config(text=COSTAS)


if __name__ == "__main__":
    root = tk.Tk()
    JogoDaMemoria(root)
    root.mainloop()
