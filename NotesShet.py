
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
            
    def __init__(self, i_picture):
        self.image = picture
        height, width = i_picture.shape
        self.countRows, self.countColumns = countBlackPixels(self.image)
        self.sound=0
        self.ratioLeft=0
        self.ratioRight=0
        self.ratioLR=0
        self.type=0
        
class Line:
    #image
    note = []
    
    def __init__(self, i_picture):
        self.image = i_picture
        height, width = i_picture.shape
        rowsBlackPixelCount, columnsBlacPixelsCount = countBlackPixels(self.image)
        
        notesLocations = []
        begin = 0
        pixelVal = math.ceil(numpy.percentile(columnsBlacPixelsCount,25)) #math.ceil(numpy.mean(columnsBlacPixelsCount)) +1
    
        tmp=[0,0]
    
        for iCol in range(1,width):
            if((columnsBlacPixelsCount[iCol]>pixelVal) and (columnsBlacPixelsCount[iCol-1]<=pixelVal)):
                #tmp[0]=iCol
                notesLocations.append(iCol)
            if((columnsBlacPixelsCount[iCol-1]>pixelVal) and (columnsBlacPixelsCount[iCol]<=pixelVal)):
                #tmp[1]=iCol
                notesLocations.append(iCol)
                
        for iNote in range(0,len(notesLocations),2):
            tmp=self.image[0:height,(notesLocations[iNote]-1):(notesLocations[iNote+1]+1)]
            self.note.append(tmp)

class Accolade:
    #image
    line = []
    
    def __init__(self, i_pictureWhole, i_pictureTreble, i_pictureBass):

        self.image = i_pictureWhole
        self.line.append(Line(i_pictureTreble))
        self.line.append(Line(i_pictureBass))        
        self.trebleLine = self.line[0]
        self.bassLine = self.line[1]
        
    
class NotesShet:
    #image
    accolade = []
    
    def __init__(self, i_picture):
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
        
        