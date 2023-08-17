from tkinter import *

def barra():
    global progress_width, values_index

    if values_index < len(valores):
        value = valores[values_index]
        values_index += 1
        progress_width = value
        canvas.coords(progress_bar, 0, 0, progress_width, 20)
        root.after(1000, barra)

root = Tk()
root.title("Barra de Progresso")
root.geometry("300x200")

canvas = Canvas(root, width=300, height=20, background="white")
canvas.place(x=0, y=150)

progress_width = 0
values_index = 0
valores = [10, 20, 40, 50, 60, 80, 90, 100, 120, 150, 200, 250, 300]

progress_bar = canvas.create_rectangle(0, 0, 0, 20, fill="green")

btn_barra = Button(root, text="Iniciar Barra", command=barra)
btn_barra.place(x=50, y=10)

root.mainloop()
