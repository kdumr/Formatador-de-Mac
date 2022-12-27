# NÃO LÊ O CÓDIGO >(
import pyautogui
import pyperclip
import time
import os
import sys
import requests
import tkinter as tk
import ctypes
import datetime
import traceback
from prettytable import PrettyTable
from tkinter import messagebox, filedialog
from pynput.keyboard import Key, Listener

version = 2.3
nome_do_programa = "mac"

# URL da página que contém informações sobre a versão mais recente
urlVersao = 'https://raw.githubusercontent.com/kdumr/Formatador-de-Mac/main/versionapp.json'

# URL do arquivo a ser baixado
urlDownload = 'https://raw.githubusercontent.com/kdumr/Formatador-de-Mac/main/dist/mac.exe'

# Criar a janela principal
root = tk.Tk()
root.withdraw()


table = PrettyTable()

# Modifica o nome do CMD
ctypes.windll.kernel32.SetConsoleTitleW("Formatador de MAC")

# Verificar versão
class Main:
    def main():        
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

                        open(file_path + f'/{nome_do_programa} {version}.exe', 'wb').write(r.content)

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
                        table.field_names = ["ATENÇÃO!"]
                        table.add_row(["Você está usando uma versão antiga do aplicativo!"])
                        print(table)
                else:
                    print('-> Você está usando a versão mais recente:', version)
            else:
                print('Erro ao verificar a versão mais recente:', response.status_code)
        except requests.exceptions.ConnectionError:
            print("-> Não foi possível verificar novas versões do aplicativo, parece que você está sem conexão.")

        lista = []
        continuar = True

        def inicio():
            print("============================================")
            print("Use a tecla DELETE para parar o programa")
            print("Use a tecla END para colar o mac no Flashman")
            print("============================================\n")

        def show(key):
            if key == Key.end:
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                    time.sleep(1)
                print('OS MACS FORAM COLADOS')
                return False
            if key == Key.delete:
                return False

        inicio()
        while continuar:
            print("Digite '0' para ir para a próxima etapa:")
            print("Digite '1' para APAGAR os macs:")
            print("Digite '2' para APAGAR o último mac:")
            print(f"MACS Registrados: {len(lista)}")
            numIn = input("Digite o mac:\n-> ")
            if numIn == "0":
                os.system('cls') or None
                print("===================================================")
                print("Use a tecla END para colar o mac no Flashman")
                print("")
                print("Use a tecla DELETE para continuar digitando os macs")
                print("===================================================\n")
                with Listener(on_press=show) as listener:
                    listener.join()
            elif numIn == "1":
                os.system('cls') or None
                print("================================")
                print("OS MACS FORAM APAGADOS DA LISTA")
                print("================================")
                inicio()
                lista.clear()
            elif numIn == "2":
                if lista == []:
                    print("====================================")
                    print("ERRO: NÃO EXISTE NENHUM MAC NA LISTA")
                    print("====================================")
                else:
                    os.system('cls') or None
                    print("================================")
                    print("O ÚLTIMO MAC FOI APAGADO DA LISTA")
                    print("================================")
                    inicio()
                    lista.pop()
            elif numIn == "":
                print("=================================")
                print("ERRO: VOCÊ PRECISA DIGITAR UM MAC")
                print("=================================")
                inicio()
            else:
                mac = '{}:{}:{}:{}:{}:{}'.format(numIn[:2], numIn[2:4], numIn[4:6], numIn[6:8], numIn[8:10], numIn[10:])
                print(f"MAC: {mac}\n")
                lista.append(mac)

if __name__ == "__main__":
    try:
        # Executa o código
        Main.main()
    except Exception as e:
        # Cria um arquivo .txt e salva o erro do aplicativo
        with open('FMac log_crash.txt', 'a') as f:
            errorText = traceback.format_exc()
            tk.messagebox.showerror("Crash", f"Ocorreu um erro na execução do aplicativo:\n{errorText}")
            f.write("\n[{}] {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(e)))
            f.write(traceback.format_exc())
            sys.exit()