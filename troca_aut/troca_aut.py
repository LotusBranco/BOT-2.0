import tkinter as tk
import threading
import time
import pyautogui

# Variável global para controlar o loop de automação
is_running_troca = False

def start_troca_automation(status_label, start_button, stop_button):
    """Inicia a automação de troca em uma thread separada."""
    global is_running_troca
    if not is_running_troca:
        is_running_troca = True
        status_label.config(text="Status: Ativo!", fg="green")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        troca_thread = threading.Thread(target=troca_automation_loop)
        troca_thread.start()

def stop_troca_automation(status_label, start_button, stop_button):
    """Para a automação de troca."""
    global is_running_troca
    if is_running_troca:
        is_running_troca = False
        status_label.config(text="Status: Inativo", fg="red")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def troca_automation_loop():
    """Executa a sequência de 6 cliques."""
    global is_running_troca
    
    # As coordenadas que você me forneceu
    coordinates = [
        (29, 210),
        (78, 203),
        (130, 203),
        (183, 209),
        (228, 209),
        (267, 212)
    ]

    while is_running_troca:
        for x, y in coordinates:
            pyautogui.click(x, y)
            time.sleep(4)  # Intervalo de 4 segundos entre os cliques

            if not is_running_troca:
                break
        
        time.sleep(0.01)
        if not is_running_troca:
            break

def create_troca_frame(parent, show_frame_func, menu_frame):
    """Cria e retorna o frame de automação de troca."""
    troca_frame = tk.Frame(parent)
    
    troca_content_frame = tk.Frame(troca_frame)
    troca_content_frame.pack(expand=True)

    troca_label = tk.Label(troca_content_frame, text="Controle de Troca", font=("Helvetica", 14, "bold"))
    troca_label.pack(pady=5)

    status_label = tk.Label(troca_content_frame, text="Status: Inativo", fg="red", font=("Helvetica", 12))
    status_label.pack(pady=5)

    start_button = tk.Button(troca_content_frame, text="Iniciar", width=20, bg="lightgreen",
                             command=lambda: start_troca_automation(status_label, start_button, stop_button))
    start_button.pack(pady=2)

    stop_button = tk.Button(troca_content_frame, text="Parar", width=20, bg="lightcoral", state=tk.DISABLED,
                            command=lambda: stop_troca_automation(status_label, start_button, stop_button))
    stop_button.pack(pady=2)

    # Botão de Voltar (agora usando show_frame_func)
    back_button = tk.Button(troca_content_frame, text="Voltar", command=lambda: show_frame_func(menu_frame))
    back_button.pack(pady=10)
    
    return troca_frame