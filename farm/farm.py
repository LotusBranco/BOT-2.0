import tkinter as tk
import threading
import time
import pyautogui
import keyboard

# Variável global para controlar o loop de automação
is_running_farm = False

# Caminho para a imagem do personagem caído
DEAD_CHARACTER_PATH = 'farm/image/croagunk_dead.png'

def start_farm_automation(status_label, start_button, stop_button):
    """Inicia a automação de farm em uma thread separada."""
    global is_running_farm
    if not is_running_farm:
        is_running_farm = True
        status_label.config(text="Status: Ativo!", fg="green")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        farm_thread = threading.Thread(target=farm_automation_loop)
        farm_thread.start()

def stop_farm_automation(status_label, start_button, stop_button):
    """Para a automação de farm."""
    global is_running_farm
    if is_running_farm:
        is_running_farm = False
        status_label.config(text="Status: Inativo", fg="red")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def farm_automation_loop():
    """Procura pelo personagem caído e executa a cascata de comandos."""
    global is_running_farm
    
    while is_running_farm:
        try:
            # Procura pela imagem do personagem caído na tela com menor confiança
            character_location = pyautogui.locateOnScreen(DEAD_CHARACTER_PATH, confidence=0.6)

            if character_location:
                print("Personagem caído detectado! Iniciando a cascata...")

                # Ação 1: Pressiona a tecla de atalho para a poção (F6)
                keyboard.press_and_release('E')
                
                # Ação 2: Clica no centro da imagem do personagem
                center_x, center_y = pyautogui.center(character_location)
                pyautogui.click(center_x, center_y)
                
                print(f"Comandos executados com sucesso em: X={center_x}, Y={center_y}")
                # Pausa para evitar cliques repetidos muito rápidos
                time.sleep(2) 
            
            else:
                print("Personagem não caído. Aguardando...")
            
        except pyautogui.PyAutoGUIException as e:
            print(f"Erro ao procurar a imagem: {e}")
            
        # Pequena pausa para não sobrecarregar a CPU
        time.sleep(1)
        
        if not is_running_farm:
            break
        
def create_farm_frame(parent, show_frame_func, menu_frame):
    """Cria e retorna o frame de automação de 'farm'."""
    farm_frame = tk.Frame(parent)
    
    farm_content_frame = tk.Frame(farm_frame)
    farm_content_frame.pack(expand=True)

    farm_label = tk.Label(farm_content_frame, text="Controle de Farm", font=("Helvetica", 14, "bold"))
    farm_label.pack(pady=5)

    status_label = tk.Label(farm_content_frame, text="Status: Inativo", fg="red", font=("Helvetica", 12))
    status_label.pack(pady=5)

    start_button = tk.Button(farm_content_frame, text="Iniciar", width=20, bg="lightgreen",
                             command=lambda: start_farm_automation(status_label, start_button, stop_button))
    start_button.pack(pady=2)

    stop_button = tk.Button(farm_content_frame, text="Parar", width=20, bg="lightcoral", state=tk.DISABLED,
                            command=lambda: stop_farm_automation(status_label, start_button, stop_button))
    stop_button.pack(pady=2)

    back_button = tk.Button(farm_content_frame, text="Voltar", command=lambda: show_frame_func(menu_frame))
    back_button.pack(pady=10)
    
    return farm_frame