import pyautogui
import time

print("O script vai começar em 5 segundos.")
print("Posicione seu mouse sobre a primeira área de clique.")

time.sleep(5)

for i in range(6):
    x, y = pyautogui.position()
    print(f"Coordenada {i+1}: X={x}, Y={y}")
    
    if i < 5:
        print("Mova o mouse para a próxima área...")
        time.sleep(3)