# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import timeit
import cv2
import numpy as np

####################################################

INPUT_IMAGE =  'b01 - Original.bmp'
COLORED_IMG = True
JANELA = 3

#################################################################
def filtro_media_separavel(img):
    return

#################################################################

def filtro_media_integral(img):
    return

#################################################################
def filtro_media_ingenuo(img):
    heigth = img.shape[0]
    width = img.shape[1]
    img_out = img.copy()
    for y in range(0 + JANELA, heigth - JANELA):
        for x in range(0 + JANELA, width - JANELA):
            soma = 0
            for h in range(y - JANELA, y + JANELA + 1):
                for w in range(x - JANELA, x + JANELA + 1):
                    soma += img[h][w]
            total_janela = (((2*JANELA) + 1)**2)
            valor_saida = soma/float(total_janela)
            img_out[y][x] = valor_saida
    return img_out

def main():
    img = None
    canais = None
    if COLORED_IMG:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    canais = cv2.split(img)
    img_canais = []
    for canal in canais:
        #cv2.imshow('Canal', canal)
        #cv2.waitKey(0)
        canal = canal.reshape((canal.shape[0], canal.shape[1], 1))
        canal = canal.astype(np.float32) / 255
        img_canais.append(filtro_media_ingenuo(canal)*255)

    if COLORED_IMG:
        img_out = cv2.merge(img_canais)
    else:
        img_out = img_canais[0]

    #cv2.imshow('Canal', img_out)
    #cv2.waitKey(0)

    cv2.imwrite('01 - imagem_filtrada.png', img_out)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
