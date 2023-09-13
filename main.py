import sys
import timeit
import cv2
import numpy as np

####################################################

INPUT_IMAGE =  'a01 - Original.bmp'
COLORED_IMG = True
JANELA = 3 ##Uso no codigo apenas a quantidade para somar para a esquerda e para a direta, se o valor aqui estiver igual a 3 então a janela é de tamanho 7 (2*JANELA + 1)

#################################################################
def filtro_media_separavel(img, heigth, width):
    img_out = img.copy()
    for y in range(0, heigth):
        primeiro = True
        soma = 0
        for x in range(JANELA, width - JANELA):
            if primeiro:
                for w in range(x - JANELA, x + JANELA + 1):
                    soma += img[y][w]
                primeiro = False
            else:
                soma = soma - img[y][x - JANELA-1] + img[y][x + JANELA]
            img_out[y][x] = soma / (JANELA*2+1)

    img_out2 = img_out.copy()
    for x in range(0 + JANELA, width - JANELA):
        for y in range(0 + JANELA, heigth - JANELA):
            soma = 0
            for h in range(y - JANELA, y + JANELA + 1):
                soma += img_out[h][x]
            img_out2[y][x] = soma / ((JANELA*2+1))

    return img_out2

#################################################################

def calcula_imagem_integral(img, heigth, width):
    img_out = np.zeros((heigth, width), dtype=float)
    # Preencha a primeira coluna da imagem de saída
    img_out[:, 0] = np.cumsum(img[:, 0])
    # Preencha a primeira linha da imagem de saída
    img_out[0, :] = np.cumsum(img[0, :])
    for y in range(1, heigth):
        for x in range(1, width):
            valor_saida = img[y, x] + img_out[y - 1, x] + img_out[y, x - 1] - img_out[y - 1, x - 1]
            img_out[y][x] = valor_saida

    return img_out

def filtro_media_integral(img, heigth, width):
    img_integral = calcula_imagem_integral(img, heigth, width)
    img_out = img.copy()
    for y in range(0, heigth):
        for x in range(0, width):
            esquerda = x - JANELA if x - JANELA - 1 >= 0 else 1
            direita = x + JANELA  if x + JANELA < width else width - 1
            cima = y - JANELA  if y - JANELA - 1 >= 0 else 1
            baixo = y + JANELA if y + JANELA < heigth else heigth - 1

            soma = img_integral[baixo][direita] - img_integral[cima - 1][direita] - img_integral[baixo][esquerda - 1] + img_integral[cima - 1][esquerda - 1]
            img_out[y][x] = soma / ((baixo - cima + 1) * (direita-esquerda+1))

    return img_out

#################################################################
def filtro_media_ingenuo(img, heigth, width):
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
    heigth = img.shape[0]
    width = img.shape[1]
    for canal in canais:
        #cv2.imshow('Canal', canal)
        #cv2.waitKey(0)
        canal = canal.reshape((canal.shape[0], canal.shape[1], 1))
        canal = canal.astype(np.float32) / 255
        #img_canais.append(filtro_media_ingenuo(canal, heigth, width)*255)
        #img_canais.append(filtro_media_integral(canal, heigth, width)*255)
        img_canais.append(filtro_media_separavel(canal, heigth, width) * 255)

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