import numpy as np
import time as time
from images import *
import matplotlib.pyplot as plt
import math


def blocking(image, x, y, size=16, dx=0, dy=0, delta=0):
    """
    Fonction qui retourne un bloc de premier pixel (x,y) de size * size d'une image 
    """
    nblock = image[x*size+dx+delta:(x+1)*size+dx +
                   delta, y*size+dy+delta:(y+1)*size+dy+delta]
    return nblock


def sad(block1, block2):
    """
    Fonction qui retourne la SAD entre 2 blocks de même taille
    """
    result = 0
    for i in range(len(block1)):
        for j in range(len(block1)):
            result += abs(block1[i][j] - block2[i][j])
    return result


def motionEstimation(window, block):
    """
    Fonction qui retourne le meilleur vecteur mouvement entre un bloc et la fenetre de recherche
    """
    sad_result = 0
    vector = (0, 0)
    blockSize = 16
    previous = np.inf
    height = len(window)
    width = len(window[0])
    for i in range(height-blockSize):
        for j in range(width-blockSize):
            blocImage = window[i:i+16, j:j+16]
            sad_result = sad(blocImage, block)
            if (previous > sad_result):
                vector = (i-16, j-16)
                previous = sad_result
            if sad_result == 0:
                return vector
    return vector


def movementCompensation(image, me_array):
    """
    Fonction qui reconstruit l'image courante grâce a une image de référence et un champ de vecteur mouvement
    """
    predictImage = np.empty((288, 352))
    for i in range(18):
        for j in range(22):
            dx, dy = me_array[22*i+j]
            nblock = image[i*16+dx+16:(i+1)*16+dx+16,
                           j*16+dy+16:(j+1)*16+dy+16]
            predictImage[i*16:(i+1)*16, j*16:(j+1)*16] = nblock

    return predictImage


def imageX4(image):
    """
    Fonction qui retourne une image 4 fois plus grande
    """
    height = len(image)
    width = len(image[0])
    heightX4 = height * 4
    widthX4 = width * 4
    newIm = np.zeros((heightX4, widthX4))
    for i in range(height):
        for j in range(width):
            newIm[i*4][j*4] = image[i][j]
    return newIm


def quarterPixelImage(image):
    """
    Fonction qui retourne une image 4 fois plus grande 
    """
    height = len(image)
    width = len(image[0])
    for i in range(height-4):
        if (i % 4 == 0):
            pass
        for j in range(width-4):
            if (i % 4 == 0 and j % 4 == 0):
                block = image[i:i+5, j:j+5]
                image[i:i + 5, j:j + 5] = weightedMean(block)
    return image


def getDistance(point1, point2):
    """
    Fonction qui retroune la distance en entre 2 points dans un bloc
    """
    return math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)


def weightedMean(block):
    """
    Fonction qui retourne un bloc remplit avec des pixel qui sont basés sur les pixels réels
    """
    height = len(block)
    width = len(block[0])
    p1 = block[0][0]
    p2 = block[0][4]
    p3 = block[4][0]
    p4 = block[4][4]
    for i in range(height):
        for j in range(width):
            if i % 4 == 0 and j % 4 == 0:
                pass
            else:
                coeff1 = getDistance((0, 0), (i, j))
                coeff2 = getDistance((0, 4), (i, j))
                coeff3 = getDistance((4, 0), (i, j))
                coeff4 = getDistance((4, 4), (i, j))
                sumCoeff = 1/coeff1 + 1/coeff2 + 1/coeff3 + 1/coeff4
                w1 = (1/coeff1)/sumCoeff
                w2 = (1/coeff2)/sumCoeff
                w3 = (1/coeff3)/sumCoeff
                w4 = (1/coeff4)/sumCoeff
                block[i][j] = w1 * p1 + w2 * p2 + w3 * p3 + w4 * p4
    return block


def blockMatching(image1, image2):
    "Fonction qui retourne le champ de vecteur mouvement "
    height = len(image1)
    width = len(image1[0])
    blockSize = 16
    me_array = []
    nbBlocksH = height // blockSize
    nbBlocksW = width // blockSize
    image1_2 = np.zeros((height+2*(blockSize-1), width+2*(blockSize-1)))
    image1_2[blockSize: height + blockSize,
             blockSize: width + blockSize] = image1

    for i in range(nbBlocksH):  # nbBlocksH
        for j in range(nbBlocksW):  # nbBlocksW
            nblock = blocking(image2, i, j)
            window = image1_2[i*blockSize: (i+3)*blockSize,
                              j*blockSize: (j+3)*blockSize]
            me = motionEstimation(window, nblock)
            me_array.append(me)
    predictImage = movementCompensation(image1_2, me_array)
    predictImage_yuv = np.uint8(np.reshape(predictImage, 352*288))
    saveImage(predictImage_yuv, 'result')


YUV1 = './images/FOOTBALL_352x288_30.yuv'
YUV2 = './images/vautours_CIF.yuv'
YUV3 = './images/zebres_CIF_long.yuv'

image1_yuv = readImage(YUV1, 1)
image1 = formatImage(image1_yuv)

image2_yuv = readImage(YUV1, 3)
image2 = formatImage(image2_yuv)

""" On lance l'algorithme de block Matching entre l'image 1 et 3 de la vidéo football
On enregistre l'image avec compensation de mouvement dans le dossier image sous le nom result.yuv
"""
t1 = time.time()
blockMatching(image1, image2)
t2 = time.time()
print('Temps : ', t2-t1)
