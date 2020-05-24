import PIL
from PIL import Image
import pdb
import matplotlib

def hex_to_rgb(value, index):
    value = value.replace('#', '')
    # pdb.set_trace()
    return ([int(value[i:i+2], 16) for i in (0, 2, 4)][index]) / 255.


# list_colors = [
#     '#D34FB9',
#     '#458ADC',
#     '#06C2F8',
#     '#87004A',
#     '#FF9E00'
# ]

# list_colors = [
#     '#D34FB9',
#     '#458ADC',
#     '#06C2F8',
#     '#87004A',
#     '#FF9E00'
# ]

# Get from color hunter
import requests
from bs4 import BeautifulSoup



palette_number = '2084768'
# palette_type = 'dull0'
palette_type = 'vibrant0'





# r = requests.get('http://www.colorhunter.com/palette/%s' % palette_number)
# soup = BeautifulSoup(r.text, 'lxml')
# raw_color_list = soup.find_all('div', {'class': 'palettecolors', 'id': palette_type})[0].find_all('div', {'class': 'color'})

# list_colors = []
# for color_line in raw_color_list:
#     list_colors.append(color_line.a['title'])


list_colors = [
    '#FF02FF',
    'FFD5FF',
    'A67EF2',
    '3D00FF',
    'EB0004',
    'FFB01A'
]


color_mapping = {
    'red': 0,
    'green': 1,
    'blue':2
}

from pprint import pprint
cdict = {k: [(float(i) / float(len(list_colors) - 1.), hex_to_rgb(list_colors[i], v), hex_to_rgb(list_colors[i], v)) for i in range(0,len(list_colors))] for k, v in color_mapping.items()}

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
oldimage = Image.open('raw-images\me.jpg')
oldimage = oldimage.convert("RGB")
newimage = quantizetopalette(oldimage, palimage, dither=False)
newimage.save('raw-images\me.png')

