"""Quiz de perguntas e respostas com interface gráfica em Tkinter."""
import tkinter as tk
from tkinter import messagebox

PERGUNTAS = [
    {
        "pergunta": "Qual linguagem estamos usando para criar estes jogos?",
        "opcoes": ["Java", "Python", "C++", "JavaScript"],
        "resposta": "Python",
    },
    {
        "pergunta": "Qual biblioteca padrão do Python foi usada para a interface gráfica?",
        "opcoes": ["Pygame", "Tkinter", "Qt", "Kivy"],
        "resposta": "Tkinter",
    },
    {
        "pergunta": "Qual é o continente mais populoso do mundo?",
        "opcoes": ["África", "Europa", "Ásia", "América do Sul"],
        "resposta": "Ásia",
    },
    {
        "pergunta": "Quanto é 7 x 8?",
        "opcoes": ["54", "56", "64", "48"],
        "resposta": "56",
    },
    {
        "pergunta": "Qual planeta é conhecido como Planeta Vermelho?",
        "opcoes": ["Vênus", "Júpiter", "Marte", "Saturno"],
        "resposta": "Marte",
    },
]


class Quiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz")
        self.root.resizable(False, False)

        self.indice_atual = 0
        self.pontuacao = 0
        self.resposta_selecionada = tk.StringVar()

        self.label_progresso = tk.Label(root, text="", font=("Arial", 10))
        self.label_progresso.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.label_pergunta = tk.Label(
            root, text="", font=("Arial", 14, "bold"), wraplength=350, justify="left"
        )
        self.label_pergunta.grid(row=1, column=0, padx=20, pady=10)

        self.frame_opcoes = tk.Frame(root)
        self.frame_opcoes.grid(row=2, column=0, padx=20)

        self.radios = []
        for i in range(4):
            radio = tk.Radiobutton(
                self.frame_opcoes,
                text="",
                variable=self.resposta_selecionada,
                value="",
                font=("Arial", 12),
                anchor="w",
                justify="left",
            )
            radio.grid(row=i, column=0, sticky="w", pady=3)
            self.radios.append(radio)

        self.botao_confirmar = tk.Button(
            root, text="Confirmar", font=("Arial", 12), command=self.confirmar_resposta
        )
        self.botao_confirmar.grid(row=3, column=0, pady=15)

        self.carregar_pergunta()

    def carregar_pergunta(self):
        pergunta = PERGUNTAS[self.indice_atual]
        self.resposta_selecionada.set("")
        self.label_progresso.config(
            text=f"Pergunta {self.indice_atual + 1} de {len(PERGUNTAS)}  |  Pontos: {self.pontuacao}"
        )
        self.label_pergunta.config(text=pergunta["pergunta"])

        for radio, opcao in zip(self.radios, pergunta["opcoes"]):
            radio.config(text=opcao, value=opcao)

    def confirmar_resposta(self):
        escolha = self.resposta_selecionada.get()
        if not escolha:
            messagebox.showwarning("Atenção", "Selecione uma opção antes de confirmar.")
            return

        pergunta = PERGUNTAS[self.indice_atual]
        if escolha == pergunta["resposta"]:
            self.pontuacao += 1

        self.indice_atual += 1
        if self.indice_atual < len(PERGUNTAS):
            self.carregar_pergunta()
        else:
            self.finalizar_quiz()

    def finalizar_quiz(self):
        messagebox.showinfo(
            "Quiz concluído",
            f"Você acertou {self.pontuacao} de {len(PERGUNTAS)} perguntas!",
        )
        self.reiniciar()

    def reiniciar(self):
        self.indice_atual = 0
        self.pontuacao = 0
        self.carregar_pergunta()


if __name__ == "__main__":
    root = tk.Tk()
    Quiz(root)
    root.mainloop()
