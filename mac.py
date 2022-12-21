#NÃO LÊ O CÓDIGO >(
import pyautogui
import pyperclip
import time
import os
from tkinter import messagebox
from pynput.keyboard import Key, Listener, Controller


def inicio():
    print("============================================")
    print("Use a tecla DELETE para parar o programa")
    print("Use a tecla END para colar o mac no Flashman")
    print("============================================\n")

lista = []
continuar = True
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
        print("============================================")
        print("Use a tecla END para colar o mac no Flashman")
        print("")
        print("Use a tecla DELETE para continuar digitando os macs")
        print("============================================\n")
        with Listener(on_press = show) as listener:
            listener.join()
    elif numIn == "1":
        os.system('cls') or None
        print("================================")
        print("OS MACS FORAM APAGADOS DA LISTA")
        print("================================")
        inicio()
        lista.clear()
    elif numIn == "2":
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
    


