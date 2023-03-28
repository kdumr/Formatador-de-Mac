import requests
import tkinter as tk
import sys
import colorama
import urllib.request
import urllib.request
from tkinter import messagebox, filedialog, ttk, ttk
from prettytable import PrettyTable

# Cria tabela
table = PrettyTable()

# Cria um esquema de cores no CMD
colorama.init(autoreset=True)
colorTexto = colorama.Fore
colorStyle = colorama.Style

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

                        r = requests.get(urlDownload)

                        file_path = filedialog.askdirectory()

                        if file_path == "":
                            tk.messagebox.showerror("Erro", f"A instalação da nova versão foi cancelada!")
                            sys.exit()
                        open(file_path + f'/{nome_do_programa} {content}.exe', 'wb').write(r.content)

                        # Realizar a solicitação HTTP
                        response = requests.get(urlDownload)

                        # Verificar o código de status da resposta
                        if response.status_code == 200:
                            # Se a resposta foi bem sucedida, obter o conteúdo da resposta
                            content = response.content

                            tk.messagebox.showinfo("Sucesso!!!", "Uma nova versão do aplicativo foi instalada com sucesso!")
                            sys.exit()

                        else:
                            print('Erro ao baixar o arquivo:', response.status_code)
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
