from re import sub
from svgelements import SVG, Image

# the length of the html elements in svgs are super long, and unnecessary for my purposes
# returns the name of the stripped file that was saved to be parsed with svgElements as well as the stripped svg object
def stripSvgHtmlElement(originalSvg):
    name = originalSvg[:len(originalSvg)-4]
    strippedName = name+"Stripped.svg"
    strippedCopy = open(name+"Stripped.svg", 'w')
    f = open(originalSvg)
    strippedTxt = sub("href=\".*\"", "href=\"...\"", f.read())
    f.close()
    strippedCopy.write(strippedTxt)
    strippedCopy.close()
    svgOut = SVG.parse(strippedName)
    return strippedName, svgOut

# layer ids don't seem to be in optimized or plain svgs...recommend using full inkscape file
# assume the guiElement layer is last eg. topMost
# elements should have a identifier in front of all id's: oscOne -> tt_oscOne
def findGUIElements(idKey, svg, layerNum=-1):
    return [el for el in svg[layerNum] if idKey in el.id]

#matrix transform
#x' = a*x + c*y + e 
#y' = b*x + d*y + f
def findGUIElPositions(svgName, idKey, layerNum=-1):
    svg = SVG.parse(svgName)
    width = svg.width
    height = svg.height
    guiElements = findGUIElements(idKey, svg, layerNum)
    output = {}
    for el in guiElements:
        if type(el) == Image:
            x = el.x * el.transform[0] + el.y*el.transform[2] + el.transform[4]
            y = el.x * el.transform[1] + el.y*el.transform[3] + el.transform[5]
            
            output[sub("tt_", "", el.id)] = (x/svg.width,y/svg.height,el.width/width, el.height/height)
    
    #sorted alphabetically
    return dict(sorted(output.items(), key=lambda item: item[0]))

def writeGUIFile(guiElementPositions):
    # Output strings
    outString = "/*\n  ==============================================================================\n\n" + \
              "\tFile generated with svg2gui\n" + \
              "\tContains the name, x/y position and width/height for each gui element from a single layer in the source SVG\n"+ \
              "\tAll values are relative to total gui width/height(in range 0 <= ... <= 1)\n" + \
              "\tVAR_NAME should be defined and imported from somewhere as a string constant. eg. #include \"../Constants.h\"\n"+ \
              "\tDeclare guiPositions in the same file as the string constants\n\n" + \
              "  ==============================================================================\n*/\n\n"


    #imports
    outString += "#include <map>;\n#include <array>;\n#include <string>;\n\n"

    #comments
    outString += "//  VAR_NAME should be useable everywhere (keep your naming consistent)"
    outString += "// {VAR_NAME: [x_position, y_position, width, height]}\n"

    #variable dec
    outString += "const std::map<std::string, std::array<float,4>> guiPositions = {\n"
    for key,vals in guiElementPositions.items():
        outString += "\t{"+ "{0},".format(key) + \
                     "{" + "{0},{1},{2},{3}".format(vals[0],vals[1],vals[2],vals[3]) + "}},\n"

    outString += "};"

    guiElCpp = open("./GuiElementsPosition.cpp","w")
    guiElCpp.write(outString)
    guiElCpp.close()