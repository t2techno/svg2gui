# svg2gui
<p>Command line program - takes an svg file and outputs a cpp file containing a map with the id's and the relative x,y positions and width/heights</p>
<h2>Required args:</h2>
  <p><ol>
    <li>fileName: The name/relative path of the SVG to open.</li>
    <li>IDKey: Should be prepended to the ID's of elements you want info on (key is not included in output file).</li>
   </ol></p>
<h2>Optional arg:</h2>
  <p><ul>
    <li>--l, -layer: Layer to find gui images. Empty defaults to last/top layer. 0 indexed</li>
  </ul></p>
 <br>
<h2>Example use:</h2> <p><ul><li>> svg2gui.exe path/to/fileName.svg find_</li>
  <ul>
    <li>Looks through all images in the last/top layer of fileName.svg</li>
    <li>Finds all images with an id of the form "find_VARNAME"</li>
    <li>outputs {VARNAME,{x,y,width,height}}</li>
    <li>Say find_KNOB_ONE is a 25x25 image at position (50,50) in an svg of total size (100,100)</li>
    <li>The cpp output in the map would be: {KNOB_ONE, {0.5, 0.5, 0.25, 0.25}}</li>
  </ul>
</p>

<p>May expand to multiple layers or other element types later. Keeping limited for speed at the moment</p>
