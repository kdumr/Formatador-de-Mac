import requests
import tkinter as tk
import sys
import colorama
import urllib.request
from tkinter import messagebox, filedialog, ttk
from prettytable import PrettyTable

# Cria tabela
table = PrettyTable()

# Cria um esquema de cores no CMD
colorama.init(autoreset=True)
colorTexto = colorama.Fore
colorStyle = colorama.Style
root = tk.Tk()
root.withdraw()
def conectar(urlVersao, urlDownload, version, nome_do_programa):
    try:
            # Realizar a solicitação HTTP
            response = requests.get(urlVersao)
            # Verificar o código de status da resposta
            if response.status_code == 200:
                # Se a resposta foi bem-sucedida, obter o conteúdo da resposta
                content = response.json()

                # Obter a versão mais recente do conteúdo
                latest_version = version

                # Comparar a versão mais recente com a versão atualmente instalada
                if latest_version < content:
                    result = messagebox.askyesno(f"Versão atual: {version}", f"Uma nova versão está disponível: {content} \nDeseja instalar?")

                    # Verificar o resultado
                    if result:
                        print("Selecione o local que deseja instalar a nova versão...")
                        def choose_directory():
                            root = tk.Tk() 
                            root.withdraw()
                            return filedialog.askdirectory()

                        def download_file(url, file_name, progress_bar):
                            try:
                                def show_progress(block_num, block_size, total_size):
                                    percent = int((block_num * block_size * 100) / total_size)
                                    progress_bar['value'] = percent
                                    progress_bar.update()

                                urllib.request.urlretrieve(url, file_name, show_progress)
                                return True
                            except urllib.error.URLError:
                                print("Não foi possível estabelecer conexão com a URL fornecida.")
                                return False

                        def show_download_progress(url, file_name):
                            install_dir = choose_directory()
                            if install_dir == "":
                                tk.messagebox.showerror("Erro!", f"A instalação foi cancelada.")
                                sys.exit()

                            progress_window = tk.Toplevel()
                            progress_window.title("Baixando...")
                            progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
                            progress_bar.pack(padx=20, pady=20)
                            # Obtém as dimensões da tela
                            screen_width = progress_window.winfo_screenwidth()
                            screen_height = progress_window.winfo_screenheight()
                            # Calcula a posição x e y da janela de loading
                            x = int((screen_width / 2) - 150)
                            y = int((screen_height / 2) - 50)
                            progress_window.geometry(f"+{x}+{y}")
                            download_success = download_file(url, f"{install_dir}/{file_name}", progress_bar)
                            progress_window.destroy()
                            if download_success:
                                tk.messagebox.showinfo("Download Concluído", f"O arquivo {file_name} foi baixado com sucesso.")
                            else:
                                tk.messagebox.showerror("Erro de Download", "Não foi possível baixar o arquivo.")
                            sys.exit()

                        url = urlDownload
                        file_name = f'{nome_do_programa} {content}.exe'
                        show_download_progress(url, file_name)
                    else:
                        table.field_names = [colorTexto.RED + "ATENÇÃO!" + colorTexto.RESET]
                        table.add_row([f"{colorTexto.RED}Você está usando uma versão antiga do aplicativo!{colorTexto.RESET}\nNova versão disponível: {colorTexto.RED}{version}{colorTexto.RESET} -> {colorTexto.GREEN}{content}{colorTexto.RESET}" + colorTexto.RESET])
                        print(table)
                else:
                    print(colorTexto.GREEN + f'-> Você está usando a versão mais recente: {version}')
            else:
                print('Erro ao verificar a versão mais recente:', response.status_code)
    except requests.exceptions.ConnectionError:
        print(colorTexto.RED + "-> Não foi possível verificar novas versões do aplicativo, parece que você está sem conexão.")