import subprocess
import re, os

def Rclone_about(remote_name):
    """Obtenha informações de cota do servidor remoto.

    Args:
        remote_name (string): retorna um lista com [Capacitade total da conta, espaço usado,espaço livre] em gigabytes
    """
    try:
        # Executa o comando Rclone para obter informações sobre o espaço livre
        command = ["rclone", "about", remote_name]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Analisa a saída em busca das informações de espaço livre
        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            return output_lines
    except Exception as e:
            print("Erro:", e)
            return None
        
def Rclone_version():
    """Mostra o número da versão.
    """
    try:
        # Executa o comando Rclone para obter informações sobre o espaço livre
        command = ["rclone", "version", "--check"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Analisa a saída em busca das informações de espaço livre
        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            versao=output_lines[0]
            v=re.sub(r"yours:  ","",versao)
            return v
            
    except Exception as e:
            print("Erro:", e)
            return None

def Rclone_config(remote_name, username, password):
    """Configura uma sessão interativa de configuração.

    Args:
        remote_name (_type_): _description_
        username (_type_): _description_
        password (_type_): _description_
        retorno:
        1 = Sucesso
        0 = Erro
    """
    pass
    create_command = f'rclone config create mega {remote_name} user "{username}"'
    password_command = f'rclone config password {remote_name} pass "{password}"'
    try:
        subprocess.run(create_command, shell=True, check=True)
        subprocess.run(password_command, shell=True, check=True)
        return 1
    except Exception as e:
        print(f"Erro: {e}")
        return 0
    
def Rclone_copy(arquivo_Local,diretorio_destino):
    """Copie arquivos da origem para o destino, ignorando arquivos idênticos.

    Args:
        remote_name (_type_): _description_
        arquivo_origem (_type_): _description_
        diretorio_destino (_type_): _description_
        retorno:
        1 = Sucesso
        0 = Erro
    """
    pass
    try:
        remote_name="mega:"
        comando = f"rclone copy {arquivo_Local} {remote_name}/{diretorio_destino} --create-empty-src-dirs"
        subprocess.run(comando, shell=True)
        return 1
    except Exception as e:
        print(f"Erro: {e}")
        return 0
    
def Rclone_mkdir(remote_name, diretorio_name):
    """Cria diretorio no caminho especificado se ele ainda não existir.

    Args:
        remote_name (_type_): _description_
        diretorio_name (_type_): _description_
        retorno:
        1 = Sucesso
        0 = Erro
    """
    try:
        comando = f"rclone mkdir {remote_name}/{diretorio_name}"
        subprocess.run(comando, shell=True)
        return 1
    except Exception as e:
        print(f"Erro: {e}")
        return 0

def Rclone_ls(remote_name):
    
    """Liste os objetos no caminho especificado com tamanho e caminho.

    Args:
        remote_name (_type_): retorna uma lista com todos os arquivos localizados
        retorno: lista com arquivos encontrados
    """
    try:
        # Comando a ser executado
        comando = "rclone ls mega:"

        # Cria um arquivo temporário para redirecionar a saída
        with open("saida_temp.txt", "w") as arquivo_temporario:
            subprocess.run(comando, shell=True, stdout=arquivo_temporario)

        # Lê o arquivo temporário e cria uma lista de linhas
        with open("saida_temp.txt", "r", encoding="utf-8") as arquivo_temporario:
            linhas = arquivo_temporario.read().splitlines()
            return linhas

        # # Imprime a lista de linhas
        # for linha in linhas:
        #     print(linha)
    except Exception as e:
        print(f"Erro: {e}")
        return None
