import os

def listar_diretorios_usuario():
    # Obter o diretório home do usuário
    home_directory = os.path.expanduser("~")
    diretorio_home=home_directory.replace("\\","/")+str("/")
    # print(diretorio_home)

    # Listar todos os diretórios presentes no diretório home
    diretorios = [diretorio for diretorio in os.listdir(home_directory) if os.path.isdir(os.path.join(home_directory, diretorio))]

    # Diretórios que deseja excluir da lista
    diretorios_excluir = ["SendTo", "Links", "Recent", "Modelos", "Saved Games",".vscode",
                          "3D Objects","Ambiente de Impressão","Ambiente de Rede",
                          "Dados de Aplicativos","Cookies","Configurações Locais",
                          "AppData","Searches","Menu Iniciar"]

    # Filtrar os diretórios a serem excluídos da lista
    diretorios_filtrados = [diretorio for diretorio in diretorios if diretorio not in diretorios_excluir]
    dir_absoluto = []
    # dir_absoluto = [os.path.join(home_directory, diretorio_nome) for diretorio_nome in dir]
    for DIR in diretorios_filtrados:
        abs=os.path.join(diretorio_home,DIR)
        dir_absoluto.append(abs)
        

    return dir_absoluto

def tamanho_total_em_mb(lista_diretorios):
    tamanho_total_bytes = 0

    for diretorio in lista_diretorios:
        for dirpath, _, filenames in os.walk(diretorio):
            for filename in filenames:
                arquivo_path = os.path.join(dirpath, filename)
                tamanho_total_bytes += os.path.getsize(arquivo_path)

    tamanho_total_mb = tamanho_total_bytes / (1024 * 1024)
    return round(tamanho_total_mb, 2)

# user=listar_diretorios_usuario()
# print(user)