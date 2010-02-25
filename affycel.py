
import csv, os, glob
import sys
import numpy

class affycel:
    def _int_(self, filename, version, header, intensityCells, intensity, maskscells, masks, outlierCells, outliers, modifiedCells, modified):
        self.filename = filename
        self.version = version
        self.header = {}
        self.intensityCells = intensityCells
        self.intensity = intensity
        self.masksCells = maskscells
        self.masks = masks
        self.outliersCells = outlierCells
        self.outliers = outliers
        self.modifiedCells = modifiedCells
        self.modfied = modified
        self.custom = {}
        
    def read_cel(self, filename):
        reader = csv.reader(open(filename, "U"),delimiter='\t')
        self.filename = os.path.split(filename)[1]
        # continu past these def to the next step

        def Rcel(row, areader):
            if '[CEL]' in row: #row passed in should contain '[CEL]'
                for row in areader: #Skips '[CEL]' row that was passed in
                    if row: # skips blank rows
                        print 'cell', row
                        if not any(("[HEADER]" in row, "[INTENSITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                            self.version = int(row[0].partition('=')[2])
                            print self.version
                            #self.version = row
                        else: 
                            rsel[row[0]](row, areader) # Go to correct section
                    
        def Rheader(row, areader):
            if '[HEADER]' in row: #row passed in should contain '[HEADER]'
                self.header = {} #self.header is a dictionary
                for row in reader: # skips the section heading row
                    if row: #skips blank rows
                        if not any(("[CEL]" in row, "[INTENSITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                            self.header[str(row[0].partition('=')[0])] = str(row[0].partition('=')[2])
                        else:
                            rsel[row[0]](row, areader) # Go to correct section
                
        def Rintensity(row, areader):
            print 'start intencity', row 
            data = []
            if "[INTENSITY]" in row: #row passed in should contain '[INTENSITY]'
                row = areader.next() # moves to the row after "[INTENSITY]"
                self.intensityCells = int(row[0].partition('=')[2]) #gets the number of intensities
                areader.next() #skips the colmn headings
                print 'cont', row
                for row in reader:
                    if row: 
                        if not any(("[CEL]" in row, "[HEADER]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                            #row = [(int(x[0]), int(x[1]), numpy.float64(x[2]), numpy.float64(x[3]), int(x[4])) for x in row]
                            data.append(tuple(row))
                            #print data[len(data)-1]
                        else:
                            #self.data = data
                            self.intensity = numpy.array(data, [('x',int),('y',int),('mean',numpy.float64),('stdv',numpy.float64),('npixcels',int)])
                            rsel[row[0]](row, areader)
            
        def Rmasks(row, areader):
            data = []
            maskstype = [('x', int), ('y', int)]
            if "[MASKS]" in row:
                            row = areader.next() # moves to the row after "[INTENSITY]"
                            self.masksCells = int(row[0].partition('=')[2]) #gets the number of intensities
                            areader.next() #skips the colmn headings
            for row in reader:
                if row:
                    if not any(("[CEL]" in row, "[HEADER]" in row, "[INTESITY]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                        
                        data.append(row)
                    else:
                        self.masks = numpy.array(data, dtype = int)
                        rsel[row[0]](row, areader)
            
        def Routliers(row, areader):
            data = []
            outlierstype = [('x', int), ('y', int)]
            if "[OUTLIERS]" in row:
                            row = areader.next() # moves to the row after "[INTENSITY]"
                            self.outliersCells = int(row[0].partition('=')[2]) #gets the number of intensities
                            areader.next() #skips the colmn headings
            for row in reader:
                if row:
                    if not any(("[CEL]" in row, "[HEADER]" in row, "[INTESITY]" in row, "[MASKS]" in row, "[MODIFIED]" in row)):
                        data.append(row)
                    else:
                        self.outliers = numpy.array(data, dtype = int)
                        rsel[row[0]](row, areader)
            
        def Rmodified(row, areader):
            data = []
            modifiedtype = [('x', int), ('y', int), ('ORIGMEAN', float)]
            if "[MODIFIED]" in row:
                            row = areader.next() # moves to the row after "[INTENSITY]"
                            self.modifiedCells = int(row[0].partition('=')[2]) #gets the number of intensities
                            areader.next() #skips the colmn headings
            for row in reader:
                if row:
                    if not any(("[CEL]" in row, "[HEADER]" in row, "[INTESITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row)):
                        data.append(row)
                    else:
                        self.modified[masks] = numpy.array(data, dtype=float64)
                        #rsel[row[0]](row, areader)
            
        rsel = {}
        rsel['[CEL]'] = Rcel
        rsel['[HEADER]']= Rheader
        rsel['[INTENSITY]']= Rintensity
        rsel['[MASKS]']= Rmasks
        rsel['[OUTLIERS]']= Routliers
        rsel['[MODIFIED]']= Rmodified        
        
        def read_selector(areader):
            for row in areader:
                print 's1', row
                if row:
                    if any(("[CEL]" in row, "[HEADER]" in row, "[INTENSITY]" in row, "[MASKS]" in row, "[OUTLIERS]" in row, "[MODIFIED]" in row)):
                        print 's2',row
                        rsel[row[0]](row, areader)
                    else: print '*****something went wrong*******'
        read_selector(reader)

        
a = affycel()
a.read_cel("/Users/vmd/Dropbox/dna/data/1g_A9AF-1.CEL")