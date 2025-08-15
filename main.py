import tkinter as tk
from aut_atk.aut_atk import create_automation_frame
from troca_aut.troca_aut import create_troca_frame
from all.all import create_all_frame
from loot.loot import create_loot_frame

def show_frame(frame):
    """Função para mostrar um frame e esconder os outros."""
    frame.tkraise()

# --- Configuração da Janela Principal ---
root = tk.Tk()
root.title("Gerenciador de Automação")
root.attributes("-topmost", True)

container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# --- Criação dos Frames ---
menu_frame = tk.Frame(container)

# Passa a função show_frame e o menu_frame para as funções de criação
automation_frame = create_automation_frame(container, show_frame, menu_frame)
troca_frame = create_troca_frame(container, show_frame, menu_frame)
all_frame = create_all_frame(container, show_frame, menu_frame)
loot_frame = create_loot_frame(container, show_frame, menu_frame)

for frame in (menu_frame, automation_frame, troca_frame, all_frame, loot_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# --- Conteúdo do Menu Principal ---
menu_content_frame = tk.Frame(menu_frame)
menu_content_frame.pack(expand=True)

menu_label = tk.Label(menu_content_frame, text="Menu Principal", font=("Helvetica", 14, "bold"))
menu_label.pack(pady=10)

attack_button = tk.Button(menu_content_frame, text="Ataque", command=lambda: show_frame(automation_frame), width=20, height=2, bg="lightblue")
attack_button.pack(pady=10)

troca_button = tk.Button(menu_content_frame, text="Troca Aut.", command=lambda: show_frame(troca_frame), width=20, height=2, bg="lightgreen")
troca_button.pack(pady=10)

all_button = tk.Button(menu_content_frame, text="All", command=lambda: show_frame(all_frame), width=20, height=2, bg="lightpink")
all_button.pack(pady=10)

loot_button = tk.Button(menu_content_frame, text="Lootear", command=lambda: show_frame(loot_frame), width=20, height=2, bg="orange")
loot_button.pack(pady=10)

show_frame(menu_frame)

root.mainloop()