import numpy as np
import matplotlib.pyplot as plt
import math


def readImage(path, nbImage):
    "Fonction qui retourne la camposante y de la nbImage d'une video"
    NB_BYTES = 352 * 288 + 2*(176*144)  # 152_064
    Y1_SIZE = 352 * 288  # 101_376
    U1_SIZE = Y1_SIZE / 2  # 50_688
    src_yuv = open(path, 'rb')
    y = []
    for _ in range(nbImage):
        data = src_yuv.read(NB_BYTES)
        y = data[0:Y1_SIZE]
    return y


def showImage(image):
    "Fonction qui affiche une image"
    plt.imshow(image)
    plt.show()


def formatImage(image):
    "Fonction qui formate une image en ligne en 2 dimensions"
    nimage = []
    for i in range(len(image)):
        nimage.append(np.uint8(repr(image[i])))
    return np.reshape(nimage, (288, 352))


def formatImageYUV(image):
    "Fonction qui formate une image 2D en ligne afin de pouvoir la sauvegarder"
    Y1_SIZE = len(image) * len(image[0])  # 101_376
    image = np.reshape(image, (Y1_SIZE, 1))
    return image


def saveImage(image, name):
    "Fonction qui sauvegarde une image sous un nom (name) dans le fichier image"
    file = open('./images/' + name + '.yuv', 'wb')
    file.write(image)
    file.close()


def psnr(img1, img2):
    "Fonction qui retourne le PSNR entre 2 images de même taille"
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
