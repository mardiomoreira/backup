from tkinter import * 
from tkinter.ttk import *
import time
import threading
def Progresso(self):
    pass
    root = Tk() 
    largura=110
    altura=39
    root.overrideredirect(True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Calcular as coordenadas para centralizar a janela
    x = (screen_width - largura) // 2
    y = (screen_height - altura) // 2
    # Definir a posição da janela
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    progress = Progressbar(root, orient = HORIZONTAL, 
                length = 100, mode = 'determinate') 
    def bar(): 
        import time 
        progress['value'] = 20
        root.update_idletasks() 
        time.sleep(2) 
    
        progress['value'] = 40
        root.update_idletasks() 
        time.sleep(3) 
    
        progress['value'] = 50
        root.update_idletasks() 
        time.sleep(4) 
    
        progress['value'] = 60
        root.update_idletasks() 
        time.sleep(5) 
    
        progress['value'] = 80
        root.update_idletasks() 
        time.sleep(2) 
        progress['value'] = 100
        time.sleep(10)
        root.destroy()
    
    progress.pack(pady = 10) 
    # Button(root, text = 'Start', command = bar).pack(pady = 10) 
    threading.Thread(target=bar).start()
    root.mainloop()
Progresso()