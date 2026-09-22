"""Jogo Adivinhe o Número com interface gráfica em Tkinter."""
import random
import tkinter as tk
from tkinter import messagebox

NUMERO_MINIMO = 1
NUMERO_MAXIMO = 100


class AdivinheONumero:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivinhe o Número")
        self.root.resizable(False, False)

        self.numero_secreto = None
        self.tentativas = 0

        self.label_instrucao = tk.Label(
            root,
            text=f"Pensei em um número entre {NUMERO_MINIMO} e {NUMERO_MAXIMO}.\nTente adivinhar!",
            font=("Arial", 12),
            justify="center",
        )
        self.label_instrucao.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.entrada = tk.Entry(root, font=("Arial", 14), justify="center")
        self.entrada.grid(row=1, column=0, columnspan=2, padx=20, pady=5)
        self.entrada.bind("<Return>", lambda evento: self.chutar())

        botao_chutar = tk.Button(root, text="Chutar", font=("Arial", 12), command=self.chutar)
        botao_chutar.grid(row=2, column=0, columnspan=2, pady=5)

        self.label_dica = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.label_dica.grid(row=3, column=0, columnspan=2, pady=10)

        self.label_tentativas = tk.Label(root, text="Tentativas: 0", font=("Arial", 10))
        self.label_tentativas.grid(row=4, column=0, columnspan=2)

        botao_reiniciar = tk.Button(
            root, text="Novo Jogo", font=("Arial", 10), command=self.reiniciar
        )
        botao_reiniciar.grid(row=5, column=0, columnspan=2, pady=10)

        self.reiniciar()

    def chutar(self):
        texto = self.entrada.get().strip()
        if not texto.isdigit():
            self.label_dica.config(text="Digite um número válido!")
            return

        chute = int(texto)
        self.tentativas += 1
        self.label_tentativas.config(text=f"Tentativas: {self.tentativas}")

        if chute < self.numero_secreto:
            self.label_dica.config(text="Mais alto! ⬆")
        elif chute > self.numero_secreto:
            self.label_dica.config(text="Mais baixo! ⬇")
        else:
            self.label_dica.config(text="Acertou! 🎉")
            messagebox.showinfo(
                "Parabéns!", f"Você acertou em {self.tentativas} tentativa(s)!"
            )

        self.entrada.delete(0, tk.END)

    def reiniciar(self):
        self.numero_secreto = random.randint(NUMERO_MINIMO, NUMERO_MAXIMO)
        self.tentativas = 0
        self.label_dica.config(text="")
        self.label_tentativas.config(text="Tentativas: 0")
        self.entrada.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    AdivinheONumero(root)
    root.mainloop()
