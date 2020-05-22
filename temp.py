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
        (0.0, hex_to_rgb('#D34FB9', 0), hex_to_rgb('#D34FB9', 0)),
        (0.25, hex_to_rgb('#458ADC', 0), hex_to_rgb('#458ADC', 0)),
        (0.5, hex_to_rgb('#06C2F8', 0), hex_to_rgb('#06C2F8', 0)),
        (0.75, hex_to_rgb('#87004A', 0), hex_to_rgb('#87004A', 0)),
        (1.0, hex_to_rgb('#FF9E00', 0), hex_to_rgb('#FF9E00', 0)),
    ],
    'green': [
        (0.0, hex_to_rgb('#D34FB9', 1), hex_to_rgb('#D34FB9', 1)),
        (0.25, hex_to_rgb('#458ADC', 1), hex_to_rgb('#458ADC', 1)),
        (0.5, hex_to_rgb('#06C2F8', 1), hex_to_rgb('#06C2F8', 1)),
        (0.75, hex_to_rgb('#87004A', 1), hex_to_rgb('#87004A', 1)),
        (1.0, hex_to_rgb('#FF9E00', 1), hex_to_rgb('#FF9E00', 1)),
    ],
    'blue': [
        (0.0, hex_to_rgb('#D34FB9', 2), hex_to_rgb('#D34FB9', 2)),
        (0.25, hex_to_rgb('#458ADC', 2), hex_to_rgb('#458ADC', 2)),
        (0.5, hex_to_rgb('#06C2F8', 2), hex_to_rgb('#06C2F8', 2)),
        (0.75, hex_to_rgb('#87004A', 2), hex_to_rgb('#87004A', 2)),
        (1.0, hex_to_rgb('#FF9E00', 2), hex_to_rgb('#FF9E00', 2)),
    ],
}



# cdict = {
#     'red': [
#         (0.0, hex_to_rgb('#FFFF00', 0), hex_to_rgb('#FFFF00', 0)),
#         (0.25, hex_to_rgb('#FF00FF', 0), hex_to_rgb('#FF00FF', 0)),
#         (0.5, hex_to_rgb('#FFF6E1', 0), hex_to_rgb('#FFF6E1', 0)),
#         (0.75, hex_to_rgb('#EEB7F4', 0), hex_to_rgb('#EEB7F4', 0)),
#         (1.0, hex_to_rgb('#00FFFF', 0), hex_to_rgb('#00FFFF', 0)),
#     ],
#     'green': [
#         (0.0, hex_to_rgb('#FFFF00', 1), hex_to_rgb('#FFFF00', 1)),
#         (0.25, hex_to_rgb('#FF00FF', 1), hex_to_rgb('#FF00FF', 1)),
#         (0.5, hex_to_rgb('#FFF6E1', 1), hex_to_rgb('#FFF6E1', 1)),
#         (0.75, hex_to_rgb('#EEB7F4', 1), hex_to_rgb('#EEB7F4', 1)),
#         (1.0, hex_to_rgb('#00FFFF', 1), hex_to_rgb('#00FFFF', 1)),
#     ],
#     'blue': [
#         (0.0, hex_to_rgb('#FFFF00', 2), hex_to_rgb('#FFFF00', 2)),
#         (0.25, hex_to_rgb('#FF00FF', 2), hex_to_rgb('#FF00FF', 2)),
#         (0.5, hex_to_rgb('#FFF6E1', 2), hex_to_rgb('#FFF6E1', 2)),
#         (0.75, hex_to_rgb('#EEB7F4', 2), hex_to_rgb('#EEB7F4', 2)),
#         (1.0, hex_to_rgb('#00FFFF', 2), hex_to_rgb('#00FFFF', 2)),
#     ],
# }

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
oldimage = Image.open('raw-images\juan.jpg')
oldimage = oldimage.convert("RGB")
newimage = quantizetopalette(oldimage, palimage, dither=False)
newimage.save('raw-images\me.png')

