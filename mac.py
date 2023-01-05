# NÃO LÊ O CÓDIGO >(
import pyautogui
import pyperclip
import time
import os
import sys
import tkinter as tk
import ctypes
import datetime
import traceback
import colorama
import json
from prettytable import PrettyTable
from pynput.keyboard import Key, Listener
from conection import *

titulo = """
 ____        _       _
/ ___|  ___ | |_   _| |_ ___  ___ 
\___ \ / _ \| | | | | __/ _ \/ __|
 ___) | (_) | | |_| | ||  __/ (__ 
|____/ \___/|_|\__,_|\__\___|\___|
"""
version = 2.6
nome_do_programa = "mac"

colorama.init(autoreset=True)
colorTexto = colorama.Fore
colorStyle = colorama.Style

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

class Main:
    def main():
        # Verifica a versão do aplciativo
        conectar(urlVersao, urlDownload, version, nome_do_programa)

        lista = []
        continuar = True

        def show(key):
            if key == Key.end:
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                    time.sleep(0.5)
                os.system('cls') or None
                print(titulo)
                print(colorTexto.LIGHTGREEN_EX + "=====================")
                print(colorTexto.LIGHTGREEN_EX + "OS MACS FORAM COLADOS")
                print(colorTexto.LIGHTGREEN_EX + "=====================" + colorTexto.RESET)
                print("")
                return False
            if key == Key.delete:
                return False

        print(titulo)
        while continuar:
            print(f"Digite '{colorStyle.BRIGHT}0{colorStyle.NORMAL}' para {colorTexto.GREEN}SEGUIR{colorTexto.RESET} para a próxima etapa:")
            print(f"Digite '{colorStyle.BRIGHT}1{colorStyle.NORMAL}' para {colorTexto.RED}DELETAR{colorTexto.RESET} os macs:")
            print(f"Digite '{colorStyle.BRIGHT}2{colorStyle.NORMAL}' para {colorTexto.LIGHTRED_EX}APAGAR{colorTexto.RESET} o último mac:")
            print(f"MACS Registrados: {colorTexto.CYAN}{len(lista)}{colorTexto.RESET}")
            numIn = input("Digite o mac:\n-> ")
            if numIn == "0":
                os.system('cls') or None
                print(titulo)
                print("===================================================")
                print("Use a tecla END para colar o mac no Flashman")
                print("")
                print("Use a tecla DELETE para continuar digitando os macs")
                print("===================================================\n")
                with Listener(on_press=show) as listener:
                    listener.join()
            elif numIn == "1":
                os.system('cls') or None
                print(titulo)
                print("================================")
                print(f"OS MACS FORAM {colorTexto.RED}DELETADOS{colorTexto.RESET} DA LISTA")
                print("================================")
                lista.clear()
            elif numIn == "2":
                if lista == []:
                    print("====================================")
                    print(f"{colorTexto.RED}ERRO:{colorTexto.RESET} NÃO EXISTE NENHUM MAC NA LISTA")
                    print("====================================")
                else:
                    print("")
                    print("=================================")
                    print(f"O ÚLTIMO MAC FOI {colorTexto.LIGHTRED_EX}APAGADO{colorTexto.RESET} DA LISTA")
                    print("=================================")
                    lista.pop()
            elif numIn == "":
                print(colorTexto.RED + "=================================")
                print(colorTexto.RED + "ERRO: VOCÊ PRECISA DIGITAR UM MAC")
                print(colorTexto.RED + "=================================")
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
