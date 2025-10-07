import pyautogui
print('Mova o mouse para a posição desejada. Pressione Ctrl-C para parar o script.')
try:
    while True:
        # Pega a posição atual do mouse
        x, y = pyautogui.position()
        # Formata a string para visualização (o '\r' atualiza a mesma linha do terminal)
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='\r')
        pyautogui.sleep(0.1) # Pausa curta para não sobrecarregar
except KeyboardInterrupt:
    print('\nCoordenadas Capturadas.')