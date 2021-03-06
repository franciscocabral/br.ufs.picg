# -*- coding: utf-8 -*-
#1 Crie uma bibliotca em python para armazenar suas funcoes.

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math

def imsave(img):
	mpimg.imsave("tmp.png", img)

#2 Crie uma funcao chamada imread que recebe um nome de arquivo e retorna a imagem lida.
def imread(image_file):
	return mpimg.imread(image_file)


#3 Abra e exiba uma imagem colorida.
def ex3():
	img = imread("./images/test20.png")
	plt.imshow(img, origin='image')
	plt.show()
               

#4 Crie uma funcao chamada nchannels que retorna o numero de canais da imagem de entrada.
def nchannels(img):
	dim = np.ndim(img)
	if dim == 3:
		return 3
	else:
		return 1


#5 Crie uma funcao chamada size que retorna um vetor onde a primeira posicao
# e a largura e a segunda e a altura em pixels da imagem.
def size(img):
	shape = np.shape(img)
	width = shape[1]
	height = shape[0]
	return np.array([width,height])

#6 Crie uma funcao chamada rgb2gray que recebe uma imagem RGB e a converte para
# escala de cinza. Para converter um pixel de RGB para escala de cinza, faca a
# media ponderada dos valores (R, G, B) com os pesos (0.299, 0.587, 0.144)
# respectivamente.
# ATENÇÃO: verifique se a imagem de entrada permanece inalterada apo s o termino
# da execucao.
# a) Crie uma funcao chamada imreadgray que recebe um nome de arquivo e retorna a
# imagem lida em escala de cinza. Deve funcionar com imagens de entrada RGB e
# escala de cinza.
def rgb2gray(img):
	return np.dot(img[:,:,:3],[.299,.587,.144]).astype('float')

#7 Crie uma função chamada imshow que recebe uma imagem como parametro e a exibe.
# Se a imagem for em escala de cinza, exiba com colormap gray. Caso a imagem seja
# pequena, usar interpolação nearest.
def imshow(img):
	isRgb = nchannels(img) == 3
	minW = 50
	minH = 50
	
	if(isRgb):
		plt.imshow(img, interpolation='nearest')
	else:
		plt.imshow(img, cmap = plt.cm.gray, interpolation='nearest' )
			
	plt.show()
	return True


#8  Crie uma funcao chama thresh que recebe uma imagem e um valor de limiar.
# Retorna uma imagem onde cada pixel tem intensidade maxima onde o pixel
# correspondemte da imagem de entrada tiver intensidade maior ou igual ao
# limiar, e intensidade minima caso contrario.
def thresh(img, l):
    return (img > l).astype(np.uint8) * 255

#9 Crie uma funcao que recebe uma imagem e retorna sua negativa.
def neg(img):
    return 255-img

#13 Crie uma funcao chamada contrast que recebe um real r e um real m.
# Seja f a entrada e g a saída, g= r(f - m) + m
def contrast(img, r, m):
    return r*(img - m) + m

#14 - crie uma funcao chamada histeq que calcula a equalizacao do histograma da imagem de
# entrada e retorna a imagem resultante. Deve funcionar para imagens em escala de cinza.
def histeq(img):
    nk = hist(img, 255).astype('float')
    n = sum(nk)
    pr = nk/n
    tr = np.array(range(0,255)).astype('float')
    tr[0] = pr[0]
    for k in range(1,255):
        tr[k] = pr[k]+tr[k-1]
    t255 = (tr * 255).astype(np.uint8)

    width,height = size(img)
    img2 = np.copy(img)
    img2 = t255[img]
    #for x in range(0,width):
    #    for y in range(0,height):
    #        img2[x][y] = t255[img[x][y]]
    plt.clf()
    return img2

#15 - Crie uma funcao chamada convolve, que recebe uma imagem de entrada e uma
#mascara com valores reais. Retorna a convolucao da imagem de entrada pela mascara.
def convolve(img, mask):
    maskW, maskH = size(mask)
    mW = maskW % 2
    mH = maskH % 2
    width,height = size(img)
    img2 = np.copy(img)
    for x in range(0,height):
        for y in range(0,width):
            tot = 0
            for mx in range(-mH,mH):
                for my in range(-mW,mW):
                    if(x < mH):
                        val = img[x][y]
                    elif(y < mW):
                        val = img[x][y]
                    else:
                        val = img[x+mx][y+my]
                    tot = tot + (mask[mx+mH][my+mW]*val)
                   
            img2[x][y] = tot
    return img2

def dft(img):
    iW, iH = size(img)
    x = [[k for k in range(iW)] for l in range(iH)]
    y = [[l for k in range(iW)] for l in range(iH)]
    fimg = np.array([[0 for k in range(iW)] for l in range(iH)], dtype=complex)

    for u in range(iW):
        for v in range(iH):
            pis = 2*np.pi
            
            ux = np.dot(x,u)
            M = iW
            
            vy = np.dot(y,v)
            N = iH

            div1 = np.divide(ux,M)
            div2 = np.divide(vy,N)
            sum1 = np.add(div1, div2)

            rad = np.dot(pis, sum1)

            cos = np.cos(rad)
            sin = np.dot(-1j,np.sin(rad))
            f = img
            
            res = np.dot(f, np.add(cos,  sin))
            
            fimg[u][v] = np.sum(res)
    return np.dot(1.0/(iW*iH), fimg)

def idft(img):
    iW, iH = size(img)
    x = [[k for k in range(iW)] for l in range(iH)]
    y = [[l for k in range(iW)] for l in range(iH)]
    fimg = np.array([[0 for k in range(iW)] for l in range(iH)], dtype=complex)

    for u in range(iW):
        for v in range(iH):
            pis = 2*np.pi
            
            ux = np.dot(x,u)
            M = iW
            
            vy = np.dot(y,v)
            N = iH

            div1 = np.divide(ux,M)
            div2 = np.divide(vy,N)
            sum1 = np.add(div1, div2)

            rad = np.dot(pis, sum1)

            cos = np.cos(rad)
            sin = np.dot(1j,np.sin(rad))
            f = img
            
            res = np.dot(f, np.add(cos,  sin))
            
            fimg[u][v] = np.sum(res)
    return fimg

#CG
def newImage(size, color):
    width, height = size
    img = np.array([[color for k in range(width)] for l in range(height)], dtype='uint8')
    return img

def drawDot(img, a, color):
    imW, imH = size(img)
    x = np.round_(a[0])
    y = np.round_(a[1])
	
    if (x >= 0 and x < imW) and (y >= 0 and y < imH):
        img[x][y] = color
    return img

def drawLine(img, a, b, color):
    x0, y0 = a
    x1, y1 = b
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    
    if (abs(dx) > abs(dy)):
        step = abs(dx)
    else:
        step = abs(dy)
        
    if(step == 0):
        step = 1
        
    xInc = dx/step
    yInc = dy/step
    
    drawDot(img, [x,y], color)
    for i in range(np.round_(step).astype(int)):
        x += xInc
        y += yInc
        drawDot(img, [x,y], color)
    return img


def drawCircle(img, c, r, color):
    x0, y0 = c
    
    for x in range(r):
        y = np.sqrt((r*r) - (x*x))
        drawDot(img, [x0 -x,y0 -y], color)
        drawDot(img, [x0 -y,y0 -x], color)
        drawDot(img, [x0 +x,y0 -y], color)
        drawDot(img, [x0 -x,y0 +y], color)
        drawDot(img, [x0 +y,y0 -x], color)
        drawDot(img, [x0 -y,y0 +x], color)
        drawDot(img, [x0 +x,y0 +y], color)
        drawDot(img, [x0 +y,y0 +x], color)
        if(x > y): break

    return img


def drawPoly(img, dots, color):
    lastDot = dots[len(dots)-1]
    
    for i, dot in enumerate(dots):
        drawLine(img, lastDot, dot, color)
        lastDot = dot
    return img

def rotate(theta, dots):
    radian = math.radians(theta)
    for i, dot in enumerate(dots):
        dots[i] = np.dot([[np.cos(radian), -np.sin(radian)], [np.sin(radian), np.cos(radian)]], dot)
    return dots

def traslade(delta, dots):
    for i, dot in enumerate(dots):
        dots[i] = [delta[0]+dot[0],delta[1]+dot[1]]
    return dots

def rotate2(theta, delta, dots):
    return traslade(delta, rotate(theta, traslade(np.dot(delta,-1), dots)))

def imgRotate(img, theta):
    iW, iH = size(img)
    c = [np.round_(iW/2), np.round_(iH/2)]
    img2 = newImage([iW,iH],[0,0,0])
    
    for x in range(iW):
        for y in range(iH):
            newDot = rotate2(theta, c, [[x,y]])[0]
            newX = np.round_(newDot[0])
            newY = np.round_(newDot[1])
            if(newX >= 0 and newX < iW) and (newY >= 0 and newY < iH):
                drawDot(img2, [x,y], img[newX][newY]*256)
    return img2

def dot2HomoDot(dot):
    return [dot[0],dot[1],1]

def homoDot2Dot(homoDot):
    return [homoDot[0], homoDot[1]]
    
def homoTranslad(dot,delta):
    dx, dy = delta
    hDot = dot2HomoDot(dot)
    return homoDot2Dot(np.dot([[1,0,dx],[0,1,dy],[0,0,1]], hDot))

def homoScale(dot, k):
    hDot = dot2HomoDot(dot)
    return homoDot2Dot(np.dot([[k,0,0],[0,k,0],[0,0,1]], hDot))

def homoRotate(dot, theta):
    radian = math.radians(theta)
    hDot = dot2HomoDot(dot)
    return homoDot2Dot(np.dot([[np.cos(radian),-np.sin(radian),0],[np.sin(radian),np.cos(radian),0],[0,0,1]], hDot))

def homoRt(dot, theta, delta):
    return homoRotate(homoTranslad(dot, delta), theta)
    #Seguindo a matriz dada em sala, o resultado aparece errado
    #dx, dy = delta
    #radian = math.radians(theta)
    #hDot = dot2HomoDot(dot)
    #return homoDot2Dot(np.dot([[np.cos(radian),-np.sin(radian),dx],[np.sin(radian),np.cos(radian),dy],[0,0,1]], hDot))
    
def homoRotate2(dotP, theta, dotC):
    rotate = homoRt(dotP, theta, np.dot(dotC,-1))
    translad = homoTranslad(rotate, dotC)
    return translad
    
def imgHomoRotate(img, theta):
    iW, iH = size(img)
    c = [np.round_(iW/2), np.round_(iH/2)]
    img2 = newImage([iW,iH],[0,0,0])
    
    for x in range(iW):
        for y in range(iH):
            newDot = homoRotate2([x,y], theta, c)
            newX = np.round_(newDot[0])
            newY = np.round_(newDot[1])
            if(newX >= 0 and newX < iW) and (newY >= 0 and newY < iH):
                drawDot(img2, [x,y], img[newX][newY]*256)
    return img2
#Area de testes
imgLena = imread('./images/lena_std.png')
imgBlack = newImage([32,32],255)
imgWhite = newImage([32,32],[0,0,0])
imgColored = newImage([500,500],[255,0,255])

dots = [[250, 250], [350, 250], [350, 350], [300, 350], [325, 300]]

imgLena45 = imgHomoRotate(imgLena, 45)

imshow(imgLena45)
