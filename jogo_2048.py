"""Jogo 2048 com interface gráfica em Tkinter."""
import random
import tkinter as tk
from tkinter import messagebox

TAMANHO = 4
OBJETIVO = 2048

CORES_FUNDO = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
    256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
}
CORES_TEXTO = {2: "#776e65", 4: "#776e65"}
COR_TEXTO_PADRAO = "#f9f6f2"

TECLAS_DIRECAO = {
    "Up": "cima", "Down": "baixo", "Left": "esquerda", "Right": "direita",
    "w": "cima", "s": "baixo", "a": "esquerda", "d": "direita",
}


class Jogo2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.resizable(False, False)

        self.label_status = tk.Label(root, text="", font=("Arial", 16))
        self.label_status.grid(row=0, column=0, pady=10)

        self.frame_tabuleiro = tk.Frame(root, bg="#bbada0")
        self.frame_tabuleiro.grid(row=1, column=0, padx=10, pady=10)

        self.celulas = []
        for linha in range(TAMANHO):
            linha_celulas = []
            for coluna in range(TAMANHO):
                label = tk.Label(
                    self.frame_tabuleiro,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    bg=CORES_FUNDO[0],
                )
                label.grid(row=linha, column=coluna, padx=5, pady=5)
                linha_celulas.append(label)
            self.celulas.append(linha_celulas)

        botao_reiniciar = tk.Button(
            root, text="Novo Jogo", font=("Arial", 12), command=self.reiniciar
        )
        botao_reiniciar.grid(row=2, column=0, pady=10)

        self.root.bind("<Key>", self.pressionar_tecla)

        self.reiniciar()

    def reiniciar(self):
        self.grade = [[0] * TAMANHO for _ in range(TAMANHO)]
        self.pontos = 0
        self.jogo_ativo = True
        self.venceu = False
        self.adicionar_tile()
        self.adicionar_tile()
        self.atualizar_status()
        self.desenhar()

    def adicionar_tile(self):
        vazias = [
            (l, c)
            for l in range(TAMANHO)
            for c in range(TAMANHO)
            if self.grade[l][c] == 0
        ]
        if not vazias:
            return
        linha, coluna = random.choice(vazias)
        self.grade[linha][coluna] = 4 if random.random() < 0.1 else 2

    def pressionar_tecla(self, evento):
        if not self.jogo_ativo:
            return
        direcao = TECLAS_DIRECAO.get(evento.keysym)
        if direcao is None:
            return

        grade_anterior = [linha[:] for linha in self.grade]
        if direcao == "esquerda":
            self.mover_esquerda()
        elif direcao == "direita":
            self.mover_direita()
        elif direcao == "cima":
            self.mover_cima()
        elif direcao == "baixo":
            self.mover_baixo()

        if self.grade != grade_anterior:
            self.adicionar_tile()
            self.atualizar_status()
            self.desenhar()
            self.checar_fim_de_jogo()

    def _comprimir_e_mesclar(self, linha):
        valores = [v for v in linha if v != 0]
        resultado = []
        i = 0
        while i < len(valores):
            if i + 1 < len(valores) and valores[i] == valores[i + 1]:
                valor_mesclado = valores[i] * 2
                resultado.append(valor_mesclado)
                self.pontos += valor_mesclado
                if valor_mesclado == OBJETIVO and not self.venceu:
                    self.venceu = True
                i += 2
            else:
                resultado.append(valores[i])
                i += 1
        resultado.extend([0] * (TAMANHO - len(resultado)))
        return resultado

    def mover_esquerda(self):
        self.grade = [self._comprimir_e_mesclar(linha) for linha in self.grade]

    def mover_direita(self):
        self.grade = [
            list(reversed(self._comprimir_e_mesclar(list(reversed(linha)))))
            for linha in self.grade
        ]

    def mover_cima(self):
        transposta = [list(coluna) for coluna in zip(*self.grade)]
        transposta = [self._comprimir_e_mesclar(linha) for linha in transposta]
        self.grade = [list(coluna) for coluna in zip(*transposta)]

    def mover_baixo(self):
        transposta = [list(coluna) for coluna in zip(*self.grade)]
        transposta = [
            list(reversed(self._comprimir_e_mesclar(list(reversed(linha)))))
            for linha in transposta
        ]
        self.grade = [list(coluna) for coluna in zip(*transposta)]

    def existe_movimento_possivel(self):
        for linha in range(TAMANHO):
            for coluna in range(TAMANHO):
                if self.grade[linha][coluna] == 0:
                    return True
                if coluna + 1 < TAMANHO and self.grade[linha][coluna] == self.grade[linha][coluna + 1]:
                    return True
                if linha + 1 < TAMANHO and self.grade[linha][coluna] == self.grade[linha + 1][coluna]:
                    return True
        return False

    def checar_fim_de_jogo(self):
        if self.venceu:
            self.venceu = False
            messagebox.showinfo("Você venceu!", "Você formou o bloco 2048!")
        if not self.existe_movimento_possivel():
            self.jogo_ativo = False
            self.label_status.config(text=f"Fim de jogo! Pontos: {self.pontos}")
            messagebox.showinfo(
                "Fim de jogo", f"Não há mais movimentos possíveis! Pontuação final: {self.pontos}"
            )

    def atualizar_status(self):
        self.label_status.config(text=f"Pontos: {self.pontos}")

    def desenhar(self):
        for linha in range(TAMANHO):
            for coluna in range(TAMANHO):
                valor = self.grade[linha][coluna]
                label = self.celulas[linha][coluna]
                label.config(
                    text=str(valor) if valor else "",
                    bg=CORES_FUNDO.get(valor, "#3c3a32"),
                    fg=CORES_TEXTO.get(valor, COR_TEXTO_PADRAO),
                )


if __name__ == "__main__":
    root = tk.Tk()
    Jogo2048(root)
    root.mainloop()
