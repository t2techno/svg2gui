import argparse
import svgUtils

# read in command line arguments 
# Initialize parser
parser = argparse.ArgumentParser()

# Adding required arguments
parser.add_argument("fileName",
                    help="The name/relative path of the SVG to open.")
parser.add_argument("IDKey",
                    help="Should be prepended to the ID's of elements you want info on (key is not included in output file)")
parser.add_argument("-l", "--layer", help="Layer to find gui elements. Empty defaults to last/top layer", 
                    default=-1, type=int)

# Read arguments from command line
args = parser.parse_args()
    
# Get gui positions and create file
guiElementPositions = svgUtils.findGUIElPositions(args.fileName, args.IDKey, args.layer)
svgUtils.writeGUIFile(guiElementPositions)