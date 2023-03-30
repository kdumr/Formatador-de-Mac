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
import pynput
from tkinter import messagebox
from prettytable import PrettyTable
from pynput.keyboard import Key, Listener
from conection import *
from api import urlLicense, urlInfoLicense, urlCreate, urlInfo, usuario, senha

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
version = 3.7
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

        def apiError():
            print(f"Error: Houve um erro de conexão com a API\n")

        def caixaTexto(texto, cor = colorTexto.WHITE, tipoLinha = "-"):
            linhas = texto.splitlines()
            tamanho = max([len(linha) for linha in linhas])
            linha_superior = tipoLinha * (tamanho + 4)
            print(cor + linha_superior)
            for linha in linhas:
                print(cor + "| " + linha.ljust(tamanho) + " |")
            print(cor + linha_superior + colorTexto.RESET)

        def status(i):
            if i:
                print(f"\n-> Os CPE's válidos foram {colorTexto.RED}BLOQUEADOS{colorTexto.RESET}")
            else:
                print(f"\n-> Os CPE's válidos foram {colorTexto.LIGHTGREEN_EX}DESBLOQUEADOS{colorTexto.RESET}")
        
        def create():
            try:
                for i in range(len(cpeNotFound)):
                    payloadCreate = {"content": {"mac_address": cpeNotFound[i], "pppoe_user": "glnk", "pppoe_password": "gigalinkinet!", "wifi_ssid": "Gigarouter", "wifi_password": "gigarouteractivation", "wifi_channel": "auto", "wifi_band": "auto", "wifi_mode": "11g"}}
                    response = requests.put(urlCreate, auth=(usuario, senha), json=payloadCreate)
                    response.json()
            except:
                apiError()
                return None
        def license(block):
            try:
                if block == True:
                    block = "true"
                elif block == False:
                    block = "false"
                for i in range(len(lista)):
                    payloadLicense = {'ids': lista[i],'block': block}
                    response = requests.put(urlLicense, auth=(usuario, senha), json=payloadLicense)
                    saida = response.json().get("success", "Error")

                    codigo = response.status_code
                    if codigo == 500:
                        codigo = f"{colorTexto.LIGHTRED_EX}CPE não encontrado{colorTexto.RESET}"
                    elif codigo == 200:
                        codigo = f"{colorTexto.LIGHTGREEN_EX}CPE encontrado{colorTexto.RESET}"
                    if saida == True:
                        saida = f'{colorTexto.LIGHTGREEN_EX}OK{colorTexto.RESET}'
                    else:
                        saida = f'{colorTexto.RED}XX{colorTexto.RESET}'
                    print(f'CPE: {lista[i]} | {saida} | {codigo}')
            except:
                apiError()
                return None

        def cancelar(key):
            if key == Key.home:
                return False
            
        def show(key):
            if key == Key.home:
                # Bloquear Mouse
                i = 0
                while True:
                    pyperclip.copy(lista[i])
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                    i += 1
                    if i == len(lista):
                        break
                    else:
                        with Listener(on_press=cancelar) as listener:
                            listener.join()

                os.system('cls') or None
                print(titulo)
                caixaTexto((" " * 10 + "OS MACS FORAM COLADOS" + " " * 10), colorTexto.GREEN)
                print("")
                return False
                
            if key == Key.end:
                # Bloquear Mouse
                original_position = pyautogui.position()
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(-100, -100)
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey(',')
                pyautogui.hotkey('enter')
                os.system('cls') or None
                print(titulo)
                caixaTexto((" " * 10 + "OS MACS FORAM COLADOS" + " " * 10), colorTexto.GREEN)
                print("")
                # Desbloquear Mouse
                mouse_listener.stop()
                pyautogui.moveTo(original_position)
                pyautogui.FAILSAFE = True
                return False
            
            if key == Key.delete:
                return False
            
            if key == Key.page_up:
                # Bloquear Mouse
                original_position = pyautogui.position()
                pyautogui.FAILSAFE = False
                pyautogui.moveTo(-100, -100)
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                for i in range(len(lista)):
                    pyperclip.copy(lista[i])
                    time.sleep(0.5)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')
                os.system('cls') or None
                print(titulo)
                caixaTexto((" " * 10 + "OS MACS FORAM COLADOS" + " " * 10), colorTexto.GREEN)
                print("")
                # Desbloquear Mouse
                mouse_listener.stop()
                pyautogui.moveTo(original_position)
                pyautogui.FAILSAFE = True
                return False

        print(titulo)
        while continuar:
            print(f"|Digite [{colorStyle.BRIGHT}0{colorStyle.NORMAL}] para {colorTexto.GREEN}SEGUIR{colorTexto.RESET} para a próxima etapa:")
            print(f"|Digite [{colorStyle.BRIGHT}1{colorStyle.NORMAL}] para {colorTexto.RED}DELETAR{colorTexto.RESET} os mac's:")
            print(f"|Digite [{colorStyle.BRIGHT}2{colorStyle.NORMAL}] para {colorTexto.LIGHTRED_EX}APAGAR{colorTexto.RESET} o último mac:")
            print(f"|Digite [{colorStyle.BRIGHT}3{colorStyle.NORMAL}] para {colorTexto.MAGENTA}LISTAR{colorTexto.RESET} os mac's copiados:")
            print(f"|Digite [{colorStyle.BRIGHT}4{colorStyle.NORMAL}] para {colorTexto.LIGHTYELLOW_EX}ALTERAR{colorTexto.RESET} o status da licença dos CPE's")
            print(f"|MACS Registrados: {colorTexto.CYAN}{len(lista)}{colorTexto.RESET}")
            numInnoReplace = input("|Digite o mac:\n-> ")
            numIn = numInnoReplace.replace(":", "")
            if numIn == "":
                caixaTexto("ERRO: Você precisa digitar um MAC.", colorTexto.RED, "=")
            elif numIn == "0":
                os.system('cls') or None
                print(titulo)
                caixaTexto(f'Use a tecla {colorTexto.LIGHTGREEN_EX}[END]{colorTexto.RESET} para colar todos os macs em sequência\n\nUse a tecla {colorTexto.GREEN}[HOME]{colorTexto.RESET} para colar UM mac por vez\n\nUse a tecla {colorTexto.CYAN}[PAGE UP]{colorTexto.RESET} para colar os macs na vertical\n\nUse a tecla {colorTexto.LIGHTRED_EX}[DELETE]{colorTexto.RESET} para continuar digitando os macs')
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
            elif numIn == "4":
                if lista == []:
                    caixaTexto("ERRO: NÃO EXISTE NENHUM MAC NA LISTA", colorTexto.RED, "=")
                else:
                    cpeNotFound = []

                    os.system('cls') or None
                    print(titulo)
                    for i in range(len(lista)):
                        payloadLicense = {'id': "0C:80:63:D8:56:64"}
                        response = requests.get(f'{urlInfo}{lista[i]}', auth=(usuario, senha))
                        responseLicense = requests.put(urlInfoLicense, auth=(usuario, senha), json=payloadLicense)
                        saida = response.json().get("success")

                        saidaLicense = responseLicense.json().get("status", saida)
                        
                        
                        if saidaLicense == True:
                            saidaLicense = f"{colorTexto.LIGHTGREEN_EX}Desbloqueado{colorTexto.RESET}"
                        elif saidaLicense == False:
                            saidaLicense = f"{colorTexto.RED}Bloqueado{colorTexto.RESET}"
                        else:
                            while saidaLicense not in [True, False]:
                                print("Carregando...")
                                responseLicense = requests.put(urlInfoLicense, auth=(usuario, senha), json=payloadLicense)
                                saidaLicense = responseLicense.json().get("status")
                                break
                            if saidaLicense == True:
                                saidaLicense = f"{colorTexto.LIGHTGREEN_EX}Desbloqueado{colorTexto.RESET}"
                            elif saidaLicense == False:
                                saidaLicense = f"{colorTexto.RED}Bloqueado{colorTexto.RESET}"


                        codigo = response.status_code
                        if codigo == 404:
                            codigo = f"{colorTexto.LIGHTRED_EX}CPE não encontrado{colorTexto.RESET}"
                            cpeNotFound.append(lista[i])
                        elif codigo == 200:
                            codigo = f"{colorTexto.LIGHTGREEN_EX}CPE encontrado{colorTexto.RESET} | Licença: {saidaLicense}"
                        print(f'CPE: {lista[i]} | {codigo}')
                    if len(cpeNotFound) > 0:
                        print("Deseja criar um registro para os CPE's não encontrados?\n")
                        print (f"|Digite [{colorStyle.BRIGHT}0{colorStyle.NORMAL}] para {colorTexto.LIGHTGREEN_EX}SIM{colorTexto.RESET}")
                        print (f"|Digite [{colorStyle.BRIGHT}1{colorStyle.NORMAL}] para {colorTexto.RED}NÃO{colorTexto.RESET}")
                        questIn = input("->")
                        if questIn == "0":
                            create()
                            caixaTexto("Os registro para os CPE's não encontrados foram criados!", colorTexto.LIGHTGREEN_EX, "=")

                    print (f"|Digite [{colorStyle.BRIGHT}0{colorStyle.NORMAL}] para {colorTexto.WHITE}VOLTAR{colorTexto.RESET} ao menu")
                    print (f"|Digite [{colorStyle.BRIGHT}1{colorStyle.NORMAL}] para {colorTexto.GREEN}DESBLOQUEAR{colorTexto.RESET} os CPE's acima:")
                    print (f"|Digite [{colorStyle.BRIGHT}2{colorStyle.NORMAL}] para {colorTexto.RED}BLOQUEAR{colorTexto.RESET} os CPE's acima:")
                    while True:
                        inp = input("->")
                        if inp != "0" and inp != "1" and inp != "2":
                            caixaTexto("ERRO: OPÇÃO INVÁLIDA", colorTexto.RED, "=")
                        else:
                            if inp == "0":
                                os.system('cls') or None
                                print(titulo)
                                break
                            elif inp == "1":
                                license(False)
                                status(False)
                                try:
                                    input("Aperte ENTER para voltar para o menu")
                                    os.system('cls') or None
                                    print(titulo)
                                    break
                                except:
                                    apiError()
                            elif inp == "2":
                                license(True)
                                status(True)
                                try:
                                    input("Aperte ENTER para voltar para o menu")
                                    os.system('cls') or None
                                    print(titulo)
                                    break
                                except :
                                    apiError()

            elif len(numIn) < 12 or len(numIn) > 12:
                caixaTexto("ERRO: O NÚMERO DIGITADO É INVÁLIDO", colorTexto.RED, "=")
            elif numIn == "info":
                os.system('cls') or None
                print("Informações do aplicativo:")
                print("\n")
                print(f"Versão: {version}")
                print("\n")

            else:
                mac = '{}:{}:{}:{}:{}:{}'.format(numIn[:2], numIn[2:4], numIn[4:6], numIn[6:8], numIn[8:10], numIn[10:])
                if mac in lista:
                    caixaTexto("ATENÇÃO: ESTE MAC JÁ EXISTE NA LISTA", colorTexto.YELLOW, "=")
                else:
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
