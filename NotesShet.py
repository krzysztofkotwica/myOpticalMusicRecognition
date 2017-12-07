import numpy
import cv2
import math


#i_picture - obraz wejsciowy (macierz 2d)
def countBlackPixels(i_picture):
    height, width = i_picture.shape
    rowsBlackPixelCount = numpy.zeros(shape=(height,1),dtype=numpy.int16)
    columnsBlacPixelsCount = numpy.zeros(shape=(width,1),dtype=numpy.int16)
    
    for iRow in range(0,height):
        for iCol in range(0, width):
            if (i_picture[iRow,iCol]<=127):
                rowsBlackPixelCount[iRow]=rowsBlackPixelCount[iRow]+1
                    
    for iCol in range(0,width):
        for iRow in range(0,height):
            if (i_picture[iRow,iCol]<=127):
                columnsBlacPixelsCount[iCol]=columnsBlacPixelsCount[iCol]+1
                
    return [rowsBlackPixelCount, columnsBlacPixelsCount]
                
    

class Note:
    #image
    #sound
    #countRows
    #countColumns
    #ratioLeft
    #ratioRight
    #ratioLR
    #type
    
    def calculateRatios(self):
        stemBegin = 0
        stemEnd = 0
        tmpMaxBlackCount = max(self.countColumns)
#        for i in range(1,self.width):
#            if self.countColumns[i]>tmpMaxBlackCount/2:
#                if stemBegin==0:
#                    stemBegin = i
#                else:
#                    stemEnd = i
        for i in range(1,self.width):
            if self.countColumns[i]==tmpMaxBlackCount:
                stemBegin = i-1
                stemEnd = i+1
        stemWidth = stemEnd - stemBegin
        stemSize = sum(self.countColumns[stemBegin:stemEnd])
        if stemSize>0:
            self.ratioLeft = sum(self.countColumns[1:stemBegin])/stemSize
            self.ratioRight = sum(self.countColumns[stemEnd:self.width])/stemSize
            if stemEnd < self.width:
              self.ratioLR= sum(self.countColumns[1:stemBegin])/sum(self.countColumns[stemEnd:self.width])
            else:
              self.ratioLR = -1
        else:
            self.type = -1
            
    def __init__(self, i_picture):
        self.image = i_picture
        self.height, self.width = i_picture.shape
        self.countRows, self.countColumns = countBlackPixels(self.image)
        self.sound=0
        self.ratioLeft=0
        self.ratioRight=0
        self.ratioLR=0
        self.type=0
        self.calculateRatios()
        
        

        
        
class Line:
    #image
    
    
    def __init__(self, i_picture):
        self.note = []
        self.image = i_picture
        height, width = i_picture.shape
        rowsBlackPixelCount, columnsBlacPixelsCount = countBlackPixels(self.image)
        
        notesLocations = []
        begin = 0
        pixelVal = math.ceil(numpy.percentile(columnsBlacPixelsCount,25)) #math.ceil(numpy.mean(columnsBlacPixelsCount)) +1
    
        tmp=[0,0]
        noteBeg=0
        noteEnd=0

        for iCol in range(1,width):
            if((columnsBlacPixelsCount[iCol]>pixelVal) and (columnsBlacPixelsCount[iCol-1]<=pixelVal)):
                #tmp[0]=iCol
                notesLocations.append(iCol)
                #noteEnd=iCol
            if((columnsBlacPixelsCount[iCol-1]>pixelVal) and (columnsBlacPixelsCount[iCol]<=pixelVal)):
                #tmp[1]=iCol
                notesLocations.append(iCol)
                #noteBeg=iCol

            if noteBeg>0 and noteEnd>0:
                tmp=self.image[0:height,(noteEnd-1):(noteEnd+1)]
                self.note.append(Note(tmp))
                noteBeg=0
                noteEnd=0

        for iNote in range(0,len(notesLocations),2):
            tmp=self.image[0:height,(notesLocations[iNote]-1):(notesLocations[iNote+1]+1)]
            self.note.append(Note(tmp))

class Accolade:
    #image
    
    
    def __init__(self, i_pictureWhole, i_pictureTreble, i_pictureBass):
        self.line = []
        self.image = i_pictureWhole
        self.line.append(Line(i_pictureTreble))
        self.line.append(Line(i_pictureBass))        
        self.trebleLine = self.line[0]
        self.bassLine = self.line[1]
        
    
class NotesShet:
    #image
    
    
    def __init__(self, i_picture):
        self.accolade = []
        self.image = i_picture
        height, width = i_picture.shape
        rowsBlackPixelCount, columnsBlacPixelsCount = countBlackPixels(self.image)
        
        linesLocation = []
        black = 0
        for iRow in range(0,height):
            if(rowsBlackPixelCount[iRow]>(width*0.5)):
                if(black==0):
                    linesLocation.append(iRow)
                    black=1
            else:
                black=0
    
        lineSpaces = linesLocation[1]-linesLocation[0]
        #lineSpaces = 0
    
        
        for iAccolade in range(0,len(linesLocation),10):
            pictureWhole=self.image[(linesLocation[iAccolade+0]-2*lineSpaces):(linesLocation[iAccolade+9]+2*lineSpaces),0:width]
            pictureTreble=self.image[(linesLocation[iAccolade+0]-2*lineSpaces):(linesLocation[iAccolade+4]+2*lineSpaces),0:width]
            pictureBass = self.image[(linesLocation[iAccolade+5]-2*lineSpaces):(linesLocation[iAccolade+9]+2*lineSpaces),0:width]
            self.accolade.append(Accolade(pictureWhole,pictureTreble,pictureBass))
        
        