import PIL
from PIL import Image
import pdb
import matplotlib

def hex_to_rgb(value, index):
    value = value.replace('#', '')
    # pdb.set_trace()
    return ([int(value[i:i+2], 16) for i in (0, 2, 4)][index]) / 255.



cdict = {
    'red': [
        (0.0, hex_to_rgb('#060031', 0), hex_to_rgb('#060031', 0)),
        (0.25, hex_to_rgb('#18007D', 0), hex_to_rgb('#18007D', 0)),
        (0.5, hex_to_rgb('#7C0076', 0), hex_to_rgb('#7C0076', 0)),
        (0.75, hex_to_rgb('#0700FA', 0), hex_to_rgb('#0700FA', 0)),
        (1.0, hex_to_rgb('#CF00F6', 0), hex_to_rgb('#CF00F6', 0)),
    ],
    'green': [
        (0.0, hex_to_rgb('#060031', 1), hex_to_rgb('#060031', 1)),
        (0.25, hex_to_rgb('#18007D', 1), hex_to_rgb('#18007D', 1)),
        (0.5, hex_to_rgb('#7C0076', 1), hex_to_rgb('#7C0076', 1)),
        (0.75, hex_to_rgb('#0700FA', 1), hex_to_rgb('#0700FA', 1)),
        (1.0, hex_to_rgb('#CF00F6', 1), hex_to_rgb('#CF00F6', 1)),
    ],
    'blue': [
        (0.0, hex_to_rgb('#060031', 2), hex_to_rgb('#060031', 2)),
        (0.25, hex_to_rgb('#18007D', 2), hex_to_rgb('#18007D', 2)),
        (0.5, hex_to_rgb('#7C0076', 2), hex_to_rgb('#7C0076', 2)),
        (0.75, hex_to_rgb('#0700FA', 2), hex_to_rgb('#0700FA', 2)),
        (1.0, hex_to_rgb('#CF00F6', 2), hex_to_rgb('#CF00F6', 2)),
    ],
}
cmap = matplotlib.colors.LinearSegmentedColormap('cmap1', cdict, 256)

palette = []
for i in range(0,256):
    
    cmap_resp = cmap(i/255.0)
    palette = palette + list(cmap_resp[:3])

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image made below
    palette.load()
    im = silf.im.convert("P", 0, palette.im)
    # the 0 above means turn OFF dithering making solid colors
    return silf._new(im)



palettedata = [int(x*255) for x in palette]
palimage = Image.new('P', (32, 32))
palimage.putpalette(palettedata)
oldimage = Image.open('raw-images\melb.jpeg')
oldimage = oldimage.convert("RGB")
newimage = quantizetopalette(oldimage, palimage, dither=False)
newimage.save('raw-images\me.png')

