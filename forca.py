"""Jogo da Forca (Hangman) com interface gráfica em Tkinter."""
import random
import string
import tkinter as tk
from tkinter import messagebox

PALAVRAS = [
    "python", "tkinter", "programacao", "computador", "teclado",
    "internet", "algoritmo", "variavel", "funcao", "biblioteca",
]

MAX_ERROS = 6


class JogoDaForca:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=200, height=220, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=7, pady=10)

        self.label_palavra = tk.Label(root, text="", font=("Courier", 24, "bold"))
        self.label_palavra.grid(row=1, column=0, columnspan=7, pady=10)

        self.label_status = tk.Label(root, text="", font=("Arial", 12))
        self.label_status.grid(row=2, column=0, columnspan=7)

        self.botoes_letras = {}
        self.criar_teclado()

        botao_reiniciar = tk.Button(
            root, text="Nova Palavra", font=("Arial", 12), command=self.reiniciar
        )
        botao_reiniciar.grid(row=5, column=0, columnspan=7, pady=10)

        self.reiniciar()

    def criar_teclado(self):
        letras = string.ascii_lowercase
        for i, letra in enumerate(letras):
            linha = 3 + i // 13
            coluna = i % 13
            botao = tk.Button(
                self.root,
                text=letra,
                font=("Arial", 10),
                width=3,
                command=lambda letra=letra: self.chutar(letra),
            )
            botao.grid(row=linha, column=coluna)
            self.botoes_letras[letra] = botao

    def desenhar_forca(self):
        self.canvas.delete("all")
        # base e poste
        self.canvas.create_line(20, 200, 120, 200)
        self.canvas.create_line(40, 200, 40, 20)
        self.canvas.create_line(40, 20, 130, 20)
        self.canvas.create_line(130, 20, 130, 50)

        partes = [
            lambda: self.canvas.create_oval(110, 50, 150, 90),  # cabeça
            lambda: self.canvas.create_line(130, 90, 130, 140),  # tronco
            lambda: self.canvas.create_line(130, 100, 105, 120),  # braço esq
            lambda: self.canvas.create_line(130, 100, 155, 120),  # braço dir
            lambda: self.canvas.create_line(130, 140, 105, 175),  # perna esq
            lambda: self.canvas.create_line(130, 140, 155, 175),  # perna dir
        ]

        for i in range(self.erros):
            partes[i]()

    def atualizar_label_palavra(self):
        exibicao = " ".join(
            letra if letra in self.letras_chutadas else "_" for letra in self.palavra
        )
        self.label_palavra.config(text=exibicao)

    def chutar(self, letra):
        if not self.jogo_ativo or letra in self.letras_chutadas:
            return

        self.letras_chutadas.add(letra)
        self.botoes_letras[letra].config(state="disabled")

        if letra not in self.palavra:
            self.erros += 1
            self.desenhar_forca()

        self.atualizar_label_palavra()

        if all(letra in self.letras_chutadas for letra in self.palavra):
            self.jogo_ativo = False
            self.label_status.config(text="Você venceu!")
            messagebox.showinfo("Fim de jogo", "Parabéns, você venceu!")
        elif self.erros >= MAX_ERROS:
            self.jogo_ativo = False
            self.label_palavra.config(text=self.palavra)
            self.label_status.config(text="Você perdeu!")
            messagebox.showinfo("Fim de jogo", f"Você perdeu! A palavra era: {self.palavra}")

    def reiniciar(self):
        self.palavra = random.choice(PALAVRAS)
        self.letras_chutadas = set()
        self.erros = 0
        self.jogo_ativo = True
        self.label_status.config(text="")
        self.canvas.delete("all")
        self.desenhar_forca()
        self.atualizar_label_palavra()
        for botao in self.botoes_letras.values():
            botao.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    JogoDaForca(root)
    root.mainloop()
