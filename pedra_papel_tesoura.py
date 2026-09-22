"""Pedra, Papel e Tesoura com interface gráfica em Tkinter."""
import random
import tkinter as tk

OPCOES = ["Pedra", "Papel", "Tesoura"]
EMOJIS = {"Pedra": "✊", "Papel": "✋", "Tesoura": "✌"}

VENCE_DE = {
    "Pedra": "Tesoura",
    "Papel": "Pedra",
    "Tesoura": "Papel",
}


class PedraPapelTesoura:
    def __init__(self, root):
        self.root = root
        self.root.title("Pedra, Papel e Tesoura")
        self.root.resizable(False, False)

        self.pontos_jogador = 0
        self.pontos_computador = 0

        self.label_placar = tk.Label(
            root, text="Você: 0  x  0 :Computador", font=("Arial", 14, "bold")
        )
        self.label_placar.grid(row=0, column=0, columnspan=3, pady=10)

        self.label_jogadas = tk.Label(root, text="Escolha sua jogada", font=("Arial", 16))
        self.label_jogadas.grid(row=1, column=0, columnspan=3, pady=10)

        self.label_resultado = tk.Label(root, text="", font=("Arial", 14))
        self.label_resultado.grid(row=2, column=0, columnspan=3, pady=10)

        for i, opcao in enumerate(OPCOES):
            botao = tk.Button(
                root,
                text=f"{EMOJIS[opcao]}\n{opcao}",
                font=("Arial", 14),
                width=8,
                height=3,
                command=lambda opcao=opcao: self.jogar(opcao),
            )
            botao.grid(row=3, column=i, padx=5, pady=10)

        botao_reiniciar = tk.Button(
            root, text="Zerar Placar", font=("Arial", 10), command=self.zerar_placar
        )
        botao_reiniciar.grid(row=4, column=0, columnspan=3, pady=10)

    def jogar(self, jogada_jogador):
        jogada_computador = random.choice(OPCOES)
        resultado = self.determinar_resultado(jogada_jogador, jogada_computador)

        texto = (
            f"Você: {EMOJIS[jogada_jogador]} {jogada_jogador}   "
            f"Computador: {EMOJIS[jogada_computador]} {jogada_computador}\n{resultado}"
        )
        self.label_resultado.config(text=texto)
        self.atualizar_placar()

    def determinar_resultado(self, jogador, computador):
        if jogador == computador:
            return "Empate!"
        if VENCE_DE[jogador] == computador:
            self.pontos_jogador += 1
            return "Você venceu!"
        self.pontos_computador += 1
        return "Computador venceu!"

    def atualizar_placar(self):
        self.label_placar.config(
            text=f"Você: {self.pontos_jogador}  x  {self.pontos_computador} :Computador"
        )

    def zerar_placar(self):
        self.pontos_jogador = 0
        self.pontos_computador = 0
        self.atualizar_placar()
        self.label_resultado.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    PedraPapelTesoura(root)
    root.mainloop()
