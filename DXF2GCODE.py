# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 11:32:02 2016

@author: ammar
"""
j = 1
skipCount = 0



print("DXF to G-code converter. Written by Ammar Aldaoud 18-09-16.")
print("Intended for use with Klayout. Interprets rectangles and lines.")
print("To use:")
print("Save Klayout file as DXF\nSet to 'no compression' and 'Decompose into SOLID entities'.")

fileDestination = input("Enter full path to file including file name:")
layerNameRectangles = input("Enter the layer name under which rectangles were created (eg. L1D0):")
layerNameLines = input("Enter the layer name under which lines were created (eg. L2D0):")

with open(fileDestination) as f:
    content = f.readlines()
sizeFile = len(content)

Rectangles = []
Lines = []
RectanglesString = []
LinesString = []
for i in range(0,sizeFile):
    if content[i] == layerNameRectangles+"\n":
        Rectangles.append(content[i+2])
        Rectangles.append(content[i+4])
        Rectangles.append(content[i+14])
        Rectangles.append(content[i+16])

del Rectangles[0:4]
numberOfRectangles = int(len(Rectangles)/4)

for i in range(0,sizeFile):
    if content[i] == layerNameLines+"\n":
        skipCount = skipCount + 1
        if ((skipCount != 1) and (skipCount-2)%3 != 0):
            Lines.append(content[i+2])
            Lines.append(content[i+4])

numberOfLines = int(len(Lines)/4)

Rectangles = [float(x)/1000 for x in Rectangles]
Lines = [float(x)/1000 for x in Lines]


for i in range(0,numberOfRectangles):
    RectanglesString.append("$rectangleBLX["+str(i)+"]="+str(Rectangles[4*i])+"\n")
    RectanglesString.append("$rectangleBLY["+str(i)+"]="+str(Rectangles[4*i+1])+"\n")
    RectanglesString.append("$rectangleTRX["+str(i)+"]="+str(Rectangles[4*i+2])+"\n")
    RectanglesString.append("$rectangleTRY["+str(i)+"]="+str(Rectangles[4*i+3])+"\n\n")


for i in range(0,numberOfLines):
    LinesString.append("$lineX1["+str(i)+"]="+str(Lines[4*i])+"\n")
    LinesString.append("$lineY1["+str(i)+"]="+str(Lines[4*i+1])+"\n")
    LinesString.append("$lineX2["+str(i)+"]="+str(Lines[4*i+2])+"\n")
    LinesString.append("$lineY2["+str(i)+"]="+str(Lines[4*i+3])+"\n\n")
    
LinesString = ''.join(LinesString)
RectanglesString = ''.join(RectanglesString)
    
numberOfRectanglesString = "$numberOfRectangles="+str(numberOfRectangles)+"\n"
numberOfLinesString = "$numberOfLines="+str(numberOfLines)+"\n"
  

"Directory to MillerCodeTemplate placed here:"
with open("/PLACE_DIRECTORY_TO_MILLER_CODE_HERE/MillerCodeTemplate.pgm") as g:
    contentTemplate = g.readlines()

for i in range(0, len(contentTemplate)):
    if contentTemplate[i] == ";appendRectangles\n":
        contentTemplate.insert(i+1,numberOfRectanglesString)
        contentTemplate.insert(i+2,RectanglesString)

for i in range(0, len(contentTemplate)):
    if contentTemplate[i] == ";appendLines\n":
        contentTemplate.insert(i+1,numberOfLinesString)
        contentTemplate.insert(i+2,LinesString)
        
GCodeFileName = input("Enter a name for the G-Code file:")

f = open("/home/ammar/Desktop/PythonLearning/"+GCodeFileName+".pgm","w") #opens file with name of "test.txt"

for item in contentTemplate:
  f.write("%s" % item)
f.close()

print("File "+GCodeFileName+".pgm sucessfully created in PythonLearning folder.")