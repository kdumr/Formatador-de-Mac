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
from prettytable import PrettyTable
from pynput.keyboard import Key, Listener
from conection import *
from threading import Thread

# Cria variável para cores
colorama.init(autoreset=True)
colorTexto = colorama.Fore
colorStyle = colorama.Style

titulo = f"""{colorTexto.YELLOW}
 ____        _       _
/ ___|  ___ | |_   _| |_ ___  ___ 
\___ \ / _ \| | | | | __/ _ \/ __|
 ___) | (_) | | |_| | ||  __/ (__ 
|____/ \___/|_|\__,_|\__\___|\___|
{colorTexto.RESET}
"""
version = 2.7
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

class Main:
    def main():
        tempoAtual = time.time()
        # Verifica a versão do aplciativo
        conectar(urlVersao, urlDownload, version, nome_do_programa)

        lista = []
        continuar = True

        def caixaTexto(texto, cor = colorTexto.WHITE, tipoLinha = "-"):
            linhas = texto.splitlines()
            tamanho = max([len(linha) for linha in linhas])
            linha_superior = tipoLinha * (tamanho + 4)
            print(cor + linha_superior)
            for linha in linhas:
                print(cor + "| " + linha.ljust(tamanho) + " |")
            print(cor + linha_superior + colorTexto.RESET)

        def show(key):
            if key == Key.end:
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                os.system('cls') or None
                print(titulo)
                caixaTexto((" " * 10 + "OS MACS FORAM COLADOS" + " " * 10), colorTexto.GREEN)
                print("")
                return False
            if key == Key.delete:
                return False

        print(titulo)
        while continuar:
            print(f"|Digite [{colorStyle.BRIGHT}0{colorStyle.NORMAL}] para {colorTexto.GREEN}SEGUIR{colorTexto.RESET} para a próxima etapa:")
            print(f"|Digite [{colorStyle.BRIGHT}1{colorStyle.NORMAL}] para {colorTexto.RED}DELETAR{colorTexto.RESET} os mac's:")
            print(f"|Digite [{colorStyle.BRIGHT}2{colorStyle.NORMAL}] para {colorTexto.LIGHTRED_EX}APAGAR{colorTexto.RESET} o último mac:")
            print(f"|Digite [{colorStyle.BRIGHT}3{colorStyle.NORMAL}] para {colorTexto.MAGENTA}LISTAR{colorTexto.RESET} os mac's copiados:")
            print(f"|MACS Registrados: {colorTexto.CYAN}{len(lista)}{colorTexto.RESET}")
            numIn = input("|Digite o mac:\n-> ")
            if numIn == "":
                caixaTexto("ERRO: Você precisa digitar um MAC.", colorTexto.RED, "=")
            elif numIn == "0":
                os.system('cls') or None
                print(titulo)
                caixaTexto("Use a tecla [END] para colar o mac no Flashman\n\nUse a tecla [DELETE] para continuar digitando os macs")
                with Listener(on_press=show) as listener:
                    listener.join()
            elif numIn == "1":
                os.system('cls') or None
                print(titulo)
                caixaTexto("OS MACS FORAM DELETADOS DA LISTA", colorTexto.RED, "=")
                lista.clear()
            elif numIn == "2":
                if lista == []:
                    caixaTexto("ERRO: NÃO EXISTE NENHUM MAC NA LISTA", colorTexto.RED, "=")
                else:
                    caixaTexto("O ÚLTIMO MAC FOI APAGADO DA LISTA", colorTexto.LIGHTRED_EX, "=")
                    lista.pop()
            elif numIn == "3":
                if lista == []:
                    caixaTexto("ERRO: NÃO EXISTE NENHUM MAC NA LISTA", colorTexto.RED, "=")
                else:
                    os.system('cls') or None
                    print(titulo)
                    caixaTexto((" " * 10 + "LISTA DE MAC'S COPIADOS" + " " * 10), colorTexto.MAGENTA)
                    for item in lista:
                        print(colorTexto.MAGENTA + item + "\n")
            elif numIn == "info":
                os.system('cls') or None
                print("Informações do aplicativo:")
                print("\n")
                print(f"Versão: {version}")
                print("\n")
            else:
                mac = '{}:{}:{}:{}:{}:{}'.format(numIn[:2], numIn[2:4], numIn[4:6], numIn[6:8], numIn[8:10], numIn[10:])
                caixaTexto(f"MAC: {mac}")
                print("")
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