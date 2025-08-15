import tkinter as tk
import threading
import time
import keyboard
import pyautogui

# Variável global para controlar os loops de ambas as automações
is_running_all = False

def start_all_automation(status_label, start_button, stop_button):
    """Inicia ambas as automações em threads separadas."""
    global is_running_all
    if not is_running_all:
        is_running_all = True
        status_label.config(text="Status: Ativo!", fg="green")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        # Inicia a automação de ataque/cura em uma nova thread
        atk_thread = threading.Thread(target=atk_automation_loop)
        atk_thread.start()

        # Inicia a automação de troca em outra nova thread
        troca_thread = threading.Thread(target=troca_automation_loop)
        troca_thread.start()

def stop_all_automation(status_label, start_button, stop_button):
    """Para ambas as automações."""
    global is_running_all
    if is_running_all:
        is_running_all = False
        status_label.config(text="Status: Inativo", fg="red")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def atk_automation_loop():
    """Loop que pressiona as teclas F1 e F2."""
    global is_running_all
    while is_running_all:
        keyboard.press('f1')
        keyboard.press('f2')
        time.sleep(1.1)
        keyboard.release('f1')
        keyboard.release('f2')
        time.sleep(0.01)
        
        if not is_running_all:
            break

def troca_automation_loop():
    """Executa a sequência de 6 cliques."""
    global is_running_all
    coordinates = [
        (29, 210), (78, 203), (130, 203),
        (183, 209), (228, 209), (267, 212)
    ]
    while is_running_all:
        for x, y in coordinates:
            pyautogui.click(x, y)
            time.sleep(4)
            if not is_running_all:
                break
        time.sleep(0.01)
        if not is_running_all:
            break

def create_all_frame(parent, show_frame_func, menu_frame):
    """Cria e retorna o frame para ambas as automações."""
    all_frame = tk.Frame(parent)
    
    all_content_frame = tk.Frame(all_frame)
    all_content_frame.pack(expand=True)

    all_label = tk.Label(all_content_frame, text="Controle Total", font=("Helvetica", 14, "bold"))
    all_label.pack(pady=5)

    status_label = tk.Label(all_content_frame, text="Status: Inativo", fg="red", font=("Helvetica", 12))
    status_label.pack(pady=5)

    start_button = tk.Button(all_content_frame, text="Iniciar Todos", width=20, bg="lightgreen",
                             command=lambda: start_all_automation(status_label, start_button, stop_button))
    start_button.pack(pady=2)

    stop_button = tk.Button(all_content_frame, text="Parar Todos", width=20, bg="lightcoral", state=tk.DISABLED,
                            command=lambda: stop_all_automation(status_label, start_button, stop_button))
    stop_button.pack(pady=2)

    back_button = tk.Button(all_content_frame, text="Voltar", command=lambda: show_frame_func(menu_frame))
    back_button.pack(pady=10)
    
    return all_frame