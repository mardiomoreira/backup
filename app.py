# Bibliotecas da Janela
from tkinter import messagebox, ttk, PhotoImage
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from tkinter import ttk
from barra import lst_valores_BARRA
# Funções Rclone
from rclone import *
#Biblioteca para naõ travar a tela
import threading
#Biblioteca para data
from datetime import date
#IMportando o script usuario
from usuario import *

class Aplicacao():
    def __init__(self) -> None:
        self.jconfig = None
        self.jprincipal = None
        self.Principal()
        
    def Principal(self):
        self.jprincipal = Tk()
        self.jprincipal.iconbitmap(bitmap="IMG\\backup.ico")
        self.jprincipal.attributes('-topmost', 1)
        self.Altura_p = 400
        self.largura_p = 400
        self.tela_largura_p = self.jprincipal.winfo_screenwidth()
        self.tela_altura_p = self.jprincipal.winfo_screenheight()
        self.x_principal = (self.tela_largura_p - self.largura_p) // 2
        self.y_principal = (self.tela_altura_p - self.Altura_p) // 2
        self.jprincipal.geometry(f"{self.largura_p}x{self.Altura_p}+{self.x_principal}+{self.y_principal}")
        img_config=PhotoImage(file="IMG\config-64.png")
        self.jprincipal.protocol("WM_DELETE_WINDOW", self.FecharJanelas)  # Tratamento para o evento de fechamento
        img_instalar=PhotoImage(file="IMG\installer-64.png")
        self.btn_instalacao=Button(self.jprincipal,text="Instalar",image=img_instalar,compound="top")
        self.btn_instalacao.grid(row=0,column=1,padx=10)
        self.btn_configuracao = Button(self.jprincipal, text="Configurar", command=self.Configuracao,image=img_config,compound="top")
        self.btn_configuracao.grid(row=0,column=0,padx=10)
        img_select_dir=PhotoImage(file="IMG\select-64.png")
        self.btn_select_dir=Button(self.jprincipal,text="Selecionar DIR",image=img_select_dir,compound="top",command=self.selecionar_diretorio)
        self.btn_select_dir.grid(row=0,column=2,padx=10)
        img_dir_USER=PhotoImage(file="IMG\\Diretorios_USER.png")
        self.btn_dir_USER=Button(self.jprincipal,text="Dir User",image=img_dir_USER,compound="top",command=self.preencher_treeview)
        self.btn_dir_USER.grid(row=0,column=3,padx=10)
        self.scrollbar = Scrollbar(self.jprincipal)
        self.tree=Treeview(self.jprincipal,yscrollcommand=self.scrollbar.set)
        self.tree.heading("#0", text="Diretório", anchor="center")
        self.tree.column("#0", anchor="center")
        self.tree.heading("#0", text="Diretório", anchor="center")
        self.tree.column("#0", anchor="center")
        self.scrollbar.config(command=self.tree.yview)
        self.tree.place(x=10,y=100,width=self.largura_p-30,height=self.Altura_p-180)
        self.scrollbar.place(x=self.largura_p-20,y=100,height=self.Altura_p-180)
        self.btn_BKP=Button(self.jprincipal,text="Backup",command=self.executar_backup)
        self.btn_BKP.place(x=90,y=372)
        self.btn_excluir=Button(self.jprincipal,text="Excluir Linha",command=self.Excluir_linha_tree)
        self.btn_excluir.place(x=175,y=372)
        self.btn_limpar_tree=Button(self.jprincipal,text="Limpar",command=self.limpar_tree)
        self.btn_limpar_tree.place(x=262,y=372)
        self.canvas = Canvas(self.jprincipal, width=400, height=20, background="white")
        self.canvas.place(x=0,y=330)
        self.progress_width = 0
        self.progress_bar = self.canvas.create_rectangle(0, 0, 0, 20, fill="green")
        self.jprincipal.mainloop()
        
    def preencher_treeview(self):
        # Substitua esta lista com os seus dados
        usuario_diretorio = listar_diretorios_usuario()

        for item in usuario_diretorio:
            self.tree.insert("", "end", text=item)
    
    def limpar_tree(self):
        self.tree.delete(*self.tree.get_children())
        
    def Excluir_linha_tree(self):
        sel=self.tree.selection()
        if len(sel) == 0:
            messagebox.showinfo(parent=self.jprincipal,title="Seleção",message="Nenhuma linha selecionada para exclusão")
        else:
            self.tree.delete(sel)
    def barra(self, valor):
        self.progress_width += valor
        self.canvas.coords(self.progress_bar, 0, 0, self.progress_width, 20)

    def Backup_tree(self):
        data_atual = date.today()
        data_atual=data_atual.strftime("%d_%m_%Y")
        FOLDER=f"BACKUP/{data_atual}/"
        diretorios=self.pegar_treeview_linhas()
        if (diretorios) == None:
            pass
        else:
            tamanho_Backup=tamanho_total_em_mb(lista_diretorios=diretorios)
            tamanho_Backup=int(tamanho_Backup)
            FREE_remoto=Rclone_about(remote_name="mega:")
            espaco_Livre=FREE_remoto[2].replace(" GiB","").replace("Free:    ","")
            espaco_Livre=float(espaco_Livre)
            free_megabytes = espaco_Livre * 1024
            espaco_Livre = int(free_megabytes)
            # print(f"Espaço Livre Nuvem:{espaco_Livre}")
            # print("Tamanho Backup: ",tamanho_Backup)
            if espaco_Livre < tamanho_Backup:
                print("Não pode fazer backup")
            else:
                self.btn_BKP.config(state='disabled')
                self.btn_excluir.config(state='disabled')
                self.btn_limpar_tree.config(state='disabled')
            ############################################################
                tamanho=len(diretorios)
                valores=lst_valores_BARRA(t_lst=tamanho)
                # print(valores)
                valor_por_diretorio = int(400 // tamanho)  # 25% do tamanho total da barra (400)
                # print(valor_por_diretorio)
                for diretorio in diretorios:
                    nome_da_pasta = os.path.basename(diretorio)
                    Rclone_copy(arquivo_Local=diretorio,diretorio_destino=FOLDER+nome_da_pasta)
                    print(diretorio)
                    self.barra(valor_por_diretorio)  # Atualiza a barra de progresso após cada diretório
                self.canvas.destroy()
                lbl_AVISO=Label(self.jprincipal,text="Backup realizado com sucesso!!!",justify='center',anchor='center',font=("Arial",11,"bold italic"),background="green",foreground="white")
                lbl_AVISO.place(x=0,y=320,relwidth=1)
                self.jprincipal.update_idletasks()
                self.limpar_tree()
                self.btn_BKP.config(state='normal')
                self.btn_excluir.config(state='normal')
                self.btn_limpar_tree.config(state='normal')
            ############################################################
            
    def executar_backup(self):
        try:
            threading.Thread(target=self.Backup_tree).start()
        except Exception as e:
            messagebox.showerror(parent=self.jprincipal,title="ERRO",message=f"Erro: {e}")

    def pegar_treeview_linhas(self):
        listDiretorios=[]
        indices=self.tree.get_children()
        if len(indices) == 0:
            messagebox.showinfo(parent=self.jprincipal,title="Tabela Vazia",message="Favor inserir Diretório na tabela")
            return None
        else:
            for linhas in indices:
                dir=self.tree.item(linhas,"text")
                listDiretorios.append(dir)
            return listDiretorios
            
    def selecionar_diretorio(self):
        diretorio=askdirectory()
        if len(diretorio) == 0:
            pass
        else:
            self.tree.insert("", "end", text=diretorio)
            
    def Configuracao(self):
        self.jconfig = Toplevel(self.jprincipal)  # Usar Toplevel para criar janela de configuração
        self.Altura_c = 200
        self.largura_c = 300
        self.tela_largura_c = self.jconfig.winfo_screenwidth()
        self.tela_altura_c = self.jconfig.winfo_screenheight()
        self.x_configuracao = (self.tela_largura_c - self.largura_c) // 2
        self.y_configuracao = (self.tela_altura_c - self.Altura_c) // 2
        self.jconfig.geometry(f"{self.largura_c}x{self.Altura_c}+{self.x_configuracao}+{self.y_configuracao}")
        
        # Use o método lift para colocar a janela à frente de todas as outras
        self.jconfig.lift()
        self.jconfig.protocol("WM_DELETE_WINDOW", self.FecharJanelaConfiguracao)  # Tratamento para o evento de fechamento
        self.lbl_titulo_c=Label(self.jconfig,text="Configuração Acesso Remoto",font=("Arial",12,"bold italic"),justify='center',anchor='center')
        self.lbl_titulo_c.place(x=0,y=0,relwidth=1)
        self.lbl_username=Label(self.jconfig,text="Username:")
        self.lbl_username.place(x=15,y=50)
        self.lbl_senha=Label(self.jconfig,text="Senha:")
        self.lbl_senha.place(x=15,y=80)
        self.ent_username=Entry(self.jconfig,justify='center',width=35)
        self.ent_username.place(x=77,y=50)
        self.ent_senha=Entry(self.jconfig,justify='center', show="*",width=35)
        self.ent_senha.place(x=77,y=80)
        self.btn_gravar=Button(self.jconfig,text="Gravar",command=self.executar_sessao_jconfig)
        self.btn_gravar.place(x=70,y=120)
        self.btn_limpar_c=Button(self.jconfig,text="Limpar",command=self.limpar_jconfig)
        self.btn_limpar_c.place(x=150,y=120)
        self.jconfig.mainloop()
        
    def limpar_jconfig(self):
        self.ent_username.delete(0,END)
        self.ent_senha.delete(0,END)
        
    def sessao_jconfig(self):
        try:
            pass
            senha=self.ent_senha.get()
            nome=self.ent_username.get()
            if nome and senha:  # Verificar se ambos os campos estão preenchidos
                # print("Não Vazio")
                Rclone_config(remote_name="mega",username=nome,password=senha)
            else:
                # print("Vazio")
                messagebox.showinfo(parent=self.jconfig,title="Campos Vazios",message="Todos os Campos são obrigatórios")
            messagebox.showinfo(parent=self.jconfig,title="Sucesso",message="Acesso Remoto Configurado com Sucesso!!!")
            self.limpar_jconfig()
        except Exception as e:
            messagebox.showerror(parent=self.jconfig,title="Erro",message=f"Erro: {e}")
            
    def executar_sessao_jconfig(self):
        threading.Thread(target=self.sessao_jconfig).start()
        
    def FecharJanelas(self):
        if self.jconfig is not None:
            self.jconfig.destroy()
        self.jprincipal.destroy()
        
    def FecharJanelaConfiguracao(self):
        self.jconfig.destroy()
        


# Crie uma instância da sua classe
app = Aplicacao()
