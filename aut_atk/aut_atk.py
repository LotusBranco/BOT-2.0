import tkinter as tk
import threading
import time
import keyboard

# Variável global para controlar o loop de automação
is_running = False

def start_automation(status_label, start_button, stop_button):
    """Função para iniciar a automação em uma thread separada."""
    global is_running
    if not is_running:
        is_running = True
        status_label.config(text="Status: Ativo!", fg="green")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        automation_thread = threading.Thread(target=automation_loop)
        automation_thread.start()

def stop_automation(status_label, start_button, stop_button):
    """Função para parar a automação."""
    global is_running
    if is_running:
        is_running = False
        status_label.config(text="Status: Inativo", fg="red")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def automation_loop():
    """Loop que pressiona as teclas F1 e F2 simultaneamente com o menor intervalo possível."""
    global is_running
    while is_running:
        keyboard.press('f1')
        keyboard.press('f2')
        
        time.sleep(1.1)
        
        keyboard.release('f1')
        keyboard.release('f2')
        
        time.sleep(0.01)
        
        if not is_running:
            break

def create_automation_frame(parent, show_frame_func, menu_frame):
    """Cria e retorna o frame de automação de ataque."""
    automation_frame = tk.Frame(parent)
    
    automation_content_frame = tk.Frame(automation_frame)
    automation_content_frame.pack(expand=True)

    automation_label = tk.Label(automation_content_frame, text="Controle de Ataque", font=("Helvetica", 14, "bold"))
    automation_label.pack(pady=5)

    status_label = tk.Label(automation_content_frame, text="Status: Inativo", fg="red", font=("Helvetica", 12))
    status_label.pack(pady=5)

    start_button = tk.Button(automation_content_frame, text="Iniciar", width=20, bg="lightgreen",
                             command=lambda: start_automation(status_label, start_button, stop_button))
    start_button.pack(pady=2)

    stop_button = tk.Button(automation_content_frame, text="Parar", width=20, bg="lightcoral", state=tk.DISABLED,
                            command=lambda: stop_automation(status_label, start_button, stop_button))
    stop_button.pack(pady=2)

    # Botão de Voltar para o menu principal (agora usando show_frame_func)
    back_button = tk.Button(automation_content_frame, text="Voltar", command=lambda: show_frame_func(menu_frame))
    back_button.pack(pady=10)
    
    return automation_frame