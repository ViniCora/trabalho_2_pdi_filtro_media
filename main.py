# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import timeit
import cv2
import numpy as np

####################################################

INPUT_IMAGE =  'a01 - Original.bmp'
COLORED_IMG = False
JANELA = 1

####################################################

def filtro_media_ingenuo(img):
    img_out = img.copy()
    heigth = img.shape[0]
    width = img.shape[1]
    if not COLORED_IMG:
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                soma = 0
                for h in range(y - JANELA, y + JANELA):
                    for w in range(x - JANELA, x + JANELA):
                        soma += img[y][x]
                total_janela = (((2*JANELA) + 1)**2)
                img_out[y][x] = soma/float(total_janela)
    return img_out

def main():
    img = None
    if COLORED_IMG:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255
    img_out = filtro_media_ingenuo(img)
    cv2.imwrite('01 - binarizada.png', img_out*255)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
