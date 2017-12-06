
import numpy
import cv2
import math
from matplotlib import pyplot as plt
from NotesShet import NotesShet


# Load an color image in grayscale
img_l = cv2.imread('notes001.jpg')
img_t = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
tmp, img = cv2.threshold(img_t,200,255,cv2.THRESH_BINARY)

ns = NotesShet(img)
fignumber = 0
print(len(ns.accolade[1].line[1].note))

''' for Acc in ns.accolade:
    plt.rcParams["figure.figsize"] = [2, 3]
    plt.imshow(Acc.image,cmap='gray' )
    plt.savefig('./figs/'+str(fignumber) + '.png')
    fignumber = fignumber +1
    for Ln in Acc.line:
        plt.rcParams["figure.figsize"] = [2, 3]
        plt.imshow(Ln.image,cmap='gray' )
        plt.savefig('./figs/'+str(fignumber) + '.png')
        fignumber = fignumber +1
        for Nt in Ln.note:
            plt.rcParams["figure.figsize"] = [2, 3]
            plt.imshow(Nt.image,cmap='gray' )
            plt.savefig('./figs/'+str(fignumber) + '.png')
            fignumber = fignumber +1
            s = 'ratioLeft = ' + str(Nt.ratioLeft) + '; ratioRight = ' +str(Nt.ratioRight) + '; ratioLR = ' +str(Nt.ratioLR) + '; type = '+str(Nt.type)
            print(s)
             '''
print('end')