"""A função do código é criar um programa que apresentará uma carta

com uma palavra em frânces e uma em inglês no verso e dois botões para

o usuário clicar caso ele saiba ou não a tradução. Se souber, a palavra

será retirada da lista"""

"""o código visa ler o arquivo CSV como um dicionário, por isso foi usado o pandas,

a variável data recebe o arquivo já convertido para o formato pandas que criará duas colunas

uma com as palavras em francês e outra em inglês e a variável to_learn vai receber o dicionário,

mas já convertido com a função orient= records, que modifica a orientação do dicionário e

ao invés de duas colunas, fica assim [{'french': 'partie', 'English': 'part}... o que facilita

na hora do sistema ler a key:value. O código foi inserido dentro de um try pois serão criadas

duas listas csv, uma com todas as palavras, que já vem carregada com o programa, e outra com as

palavras restantes, que ainda não foram aprendidas, se acontecer dessa segunda lista não existir,

como na primeira vez que o programa rodar, ele vai dar uma exceção"""

from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

"""a função abaixo vai escolher aleatoriamente uma carta que contém a chave "French" do dicionário,

depois o canvas.itemconfig vai configurar o botão passado como parâmetro, nesse caso, o botão

que configura o título e o da palavra atual mostrada na tela. Reparar que primeiro ela criou

o botão na parte da configuração visual com as devidas configurações e depois o guardou em uma

variável para poder utilizar esta mesma variável e modificá-la. Também reparar no current_card

que ganhou um escopo global para poder ser utilizado em vários locais do código. A função

after_cancel cancela a função do after, pois se ela não for chamada, o código vai contar

 3 segundos, mesmo, que se troque de carta e a ideia são 3 segundos a cada carta"""
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

"""essa é a função que vai modificar as configurações da tela quando o carta for virada

de francês para inglês, ela é chamada na função next_card"""
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)
"""essa função remove a palavra do dicionário to_learn quando o usuário clicar no botão

check e depois cria um novo dicionário só com as palavras restantes, ainda não decoradas.

O index como falso serve para que não sejam adicionados indices no dicionário toda vez

que o panda acrescentar uma nova palavra"""

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

"""código inicial de configuração da tela e do fundo"""
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
"""essa função (after) é uma função interna, ela funciona para chamar uma determinada função

depois de um tempo determinado em milisecundos. Quando estava fazendo o código, a professora

primeiro criou a função é só depois a guardou em uma variável para poder reutilizá-la mais

facilmente."""
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
"""dica: quando for inserir um nome de arquivo, como acima, dar preferência ao

autocomplete do Pycharm para diminuir a chance de erro de digitação"""
"""as linhas acima configuram a posição da imagem e a criação do texto do título e da

palavra a ser traduzida, lembrando que a posição é a metade ou quase a metade do

tamanho do Canvas."""
"""já o código 109 e 110 servem para configurar a imagem que ficará dentro da janela(window),

por isso foi usado o módulo canvas, """



cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

"""essas linhas aci,a criam o botão de X, primeiro cria a variável da imagem e através do método

PhotoImage que é um método do tkinter para mostrar imagens, indica-se o caminho do arquivo,

depois, cria-se o botão e o ajusta no Grid. Já o comando (command) next_card, chama uma

função"""

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)
"""esse código é igual ao do unknowm button, mas para o botão de acerto que também servirá

para retirar a palavra da lista de palavras desconhecidas"""

next_card()
""""A função já é chamada no início para que possa começar o programa com as configurações."""

window.mainloop()



