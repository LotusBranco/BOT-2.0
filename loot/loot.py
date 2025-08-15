import tkinter as tk
import threading
import time
import pyautogui

# Variável global para controlar o loop de automação
is_running_loot = False

# Lista com os caminhos para as imagens dos itens que queremos coletar
LOOT_ITEM_PATHS = [
    'loot/image/small_stones.png',
    'loot/image/water_gems.png',
    'loot/image/water_gems_2.png'  # Adicione o nome da sua nova imagem aqui
]

def start_loot_automation(status_label, start_button, stop_button):
    """Inicia a automação de 'looting' em uma thread separada."""
    global is_running_loot
    if not is_running_loot:
        is_running_loot = True
        status_label.config(text="Status: Ativo!", fg="green")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        loot_thread = threading.Thread(target=loot_automation_loop)
        loot_thread.start()

def stop_loot_automation(status_label, start_button, stop_button):
    """Para a automação de 'looting'."""
    global is_running_loot
    if is_running_loot:
        is_running_loot = False
        status_label.config(text="Status: Inativo", fg="red")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

def loot_automation_loop():
    """Procura pelos itens na tela e clica neles."""
    global is_running_loot
    
    while is_running_loot:
        item_found = False
        for item_path in LOOT_ITEM_PATHS:
            try:
                # Procura por cada item na lista
                item_location = pyautogui.locateOnScreen(item_path, confidence=0.7)

                if item_location:
                    # Se um item foi encontrado, clica nele e sai do loop interno
                    center_x, center_y = pyautogui.center(item_location)
                    pyautogui.click(center_x, center_y)
                    print(f"Item '{item_path}' encontrado e clicado em: X={center_x}, Y={center_y}")
                    item_found = True
                    break # Sai do loop 'for' para recomeçar a busca do zero
                
            except pyautogui.PyAutoGUIException as e:
                print(f"Erro ao procurar a imagem: {e}")
            
        if not item_found:
            print("Nenhum item encontrado. Procurando novamente...")
            
        # Pequena pausa para não sobrecarregar a CPU
        time.sleep(1)
        
        if not is_running_loot:
            break
        
def create_loot_frame(parent, show_frame_func, menu_frame):
    """Cria e retorna o frame de automação de 'looting'."""
    loot_frame = tk.Frame(parent)
    
    loot_content_frame = tk.Frame(loot_frame)
    loot_content_frame.pack(expand=True)

    loot_label = tk.Label(loot_content_frame, text="Controle de Loot", font=("Helvetica", 14, "bold"))
    loot_label.pack(pady=5)

    status_label = tk.Label(loot_content_frame, text="Status: Inativo", fg="red", font=("Helvetica", 12))
    status_label.pack(pady=5)

    start_button = tk.Button(loot_content_frame, text="Iniciar", width=20, bg="lightgreen",
                             command=lambda: start_loot_automation(status_label, start_button, stop_button))
    start_button.pack(pady=2)

    stop_button = tk.Button(loot_content_frame, text="Parar", width=20, bg="lightcoral", state=tk.DISABLED,
                            command=lambda: stop_loot_automation(status_label, start_button, stop_button))
    stop_button.pack(pady=2)

    back_button = tk.Button(loot_content_frame, text="Voltar", command=lambda: show_frame_func(menu_frame))
    back_button.pack(pady=10)
    
    return loot_frame