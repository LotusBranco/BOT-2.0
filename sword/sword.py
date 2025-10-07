import tkinter as tk
import threading
import time
import pyautogui
import keyboard

# Variável global para controlar o loop de automação da GUI
is_running_sword = False

# Variável global para controlar o estado da tecla F1
is_hotkey_pressed = False

# Caminho para a imagem do monstro (Gatilho)
MONSTER_SWORD_PATH = 'sword/image/tm-sword.png'

# Coordenadas da Área de Interesse (ROI) para otimização
# (X superior esquerdo, Y superior esquerdo, Largura, Altura)
# X1=1174, Y1=121, X2=1193, Y2=178
# Largura = 1193 - 1174 = 19
# Altura = 178 - 121 = 57
MONITOR_REGION = (1174, 121, 19, 57)

# O comando de ataque
ATTACK_HOTKEY = 'f1'

def start_sword_automation(status_label, start_button, stop_button):
    """Inicia a automação 'sword' em uma thread separada."""
    global is_running_sword
    if not is_running_sword:
        is_running_sword = True
        status_label.config(text="Status: Ativo!", fg="green")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        
        sword_thread = threading.Thread(target=sword_automation_loop)
        sword_thread.start()

def stop_sword_automation(status_label, start_button, stop_button):
    """Para a automação 'sword'."""
    global is_running_sword, is_hotkey_pressed
    if is_running_sword:
        is_running_sword = False
        status_label.config(text="Status: Inativo", fg="red")
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        
        # Garante que a tecla F1 seja solta ao parar a automação
        if is_hotkey_pressed:
            keyboard.release(ATTACK_HOTKEY)
            is_hotkey_pressed = False


def sword_automation_loop():
    """Monitora a área, pressiona F1 quando o monstro aparece e solta quando ele sai."""
    global is_running_sword, is_hotkey_pressed
    
    while is_running_sword:
        try:
            # PROCURA OTIMIZADA: Procura o monstro APENAS na região definida
            monster_location = pyautogui.locateOnScreen(
                MONSTER_SWORD_PATH, 
                confidence=0.7,
                region=MONITOR_REGION
            )

            if monster_location:
                # Monstro ENCONTRADO
                if not is_hotkey_pressed:
                    # A tecla não está pressionada, então vamos pressionar.
                    keyboard.press(ATTACK_HOTKEY)
                    is_hotkey_pressed = True
                    # print(f"Monstro detectado! Tecla {ATTACK_HOTKEY} pressionada.")
                # Se já estiver pressionada, o loop continua e mantém o F1 ativo.
            
            else:
                # Monstro NÃO ENCONTRADO
                if is_hotkey_pressed:
                    # A tecla está pressionada, mas o monstro sumiu. Hora de soltar.
                    keyboard.release(ATTACK_HOTKEY)
                    is_hotkey_pressed = False
                    # print(f"Monstro saiu da área. Tecla {ATTACK_HOTKEY} liberada.")
            
        except pyautogui.PyAutoGUIException as e:
            # Captura erro se, por exemplo, a imagem não for encontrada por algum motivo de caminho
            print(f"Erro ao procurar a imagem: {e}")
            
        # Pausa muito curta para loops ultrarrápidos (Verifica 10 vezes por segundo)
        time.sleep(0.1)
        
        if not is_running_sword:
            break
        
def create_sword_frame(parent, show_frame_func, menu_frame):
    """Cria e retorna o frame de automação de 'sword'."""
    sword_frame = tk.Frame(parent)
    
    sword_content_frame = tk.Frame(sword_frame)
    sword_content_frame.pack(expand=True)

    sword_label = tk.Label(sword_content_frame, text="Controle de Sword", font=("Helvetica", 14, "bold"))
    sword_label.pack(pady=5)

    status_label = tk.Label(sword_content_frame, text="Status: Inativo", fg="red", font=("Helvetica", 12))
    status_label.pack(pady=5)

    start_button = tk.Button(sword_content_frame, text="Iniciar", width=20, bg="lightgreen",
                             command=lambda: start_sword_automation(status_label, start_button, stop_button))
    start_button.pack(pady=2)

    stop_button = tk.Button(sword_content_frame, text="Parar", width=20, bg="lightcoral", state=tk.DISABLED,
                            command=lambda: stop_sword_automation(status_label, start_button, stop_button))
    stop_button.pack(pady=2)

    back_button = tk.Button(sword_content_frame, text="Voltar", command=lambda: show_frame_func(menu_frame))
    back_button.pack(pady=10)
    
    return sword_frame