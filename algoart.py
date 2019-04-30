import cv2
import numpy as np
from color_matching import ColorMatch
from algo_masks import pointSinusoidal, pointDamped, pointParabolic


def main():
    img = cv2.imread('raw-images/dog-face.png')

    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]

    # Setup Manipulations Channels
    b_manip = np.ones(b.shape, dtype=np.float)
    g_manip = np.ones(g.shape, dtype=np.float)
    r_manip = np.ones(r.shape, dtype=np.float)

    # Manipulate
    x = np.linspace(0, 499, 500)
    y = np.linspace(0, 499, 500)
    xx, yy = np.meshgrid(x, y)
    z1 = np.sin(xx / 10) + np.cos(yy / 10)
    z1 = np.abs(z1 / 2)
    z2 = np.sin(xx / 30) + np.cos(yy / 10)
    z2 = np.abs(z2 / 2)
    z3 = np.sin(xx / 10) + np.cos(yy / 60)
    z3 = np.abs(z3 / 2)

    b_manip = b_manip * b * z1
    r_manip = r_manip * r * z2
    g_manip = g_manip * g * z3




    # Prepare for combining
    b_manip = np.round(b_manip, 0)
    g_manip = np.round(g_manip, 0)
    r_manip = np.round(r_manip, 0)

    manip = np.stack((b_manip.astype(dtype=np.uint8),
                      g_manip.astype(dtype=np.uint8),
                      r_manip.astype(dtype=np.uint8)), axis=2)

    cv2.imshow('image', manip)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # cv2.imwrite('manipulated/dog-manip.png', manip)


def color_match(img_fn, color_model_fn):

    bgr_img_orig = cv2.imread(img_fn)
    img_orig = cv2.cvtColor(bgr_img_orig, cv2.COLOR_BGR2HSV)
    cm = ColorMatch()
    cm.load_model(color_model_fn)

    # Get list of colors
    print "Getting set of colors"

    unq_col = np.asarray(img_orig).reshape((img_orig.shape[0]*img_orig.shape[1], 3))

    print type(unq_col)
    print unq_col.shape
    print

    print "Begin"
    col_index, color_array = cm.match_color(unq_col)

    print type(col_index)
    print col_index.shape
    print type(color_array)
    print color_array.shape
    recolored_array = color_array[col_index[:]]
    print type(recolored_array)
    print recolored_array.shape

    recolored = recolored_array.reshape(img_orig.shape[0], img_orig.shape[1], img_orig.shape[2])

    print recolored.shape
    recolored = cv2.cvtColor(recolored, cv2.COLOR_HSV2BGR)

    mask = pointParabolic(img_orig.shape, 650, 600, 350, 200).matrix
    # mask = pointSinusoidal(img_orig.shape, 650, 600, 250, 150).matrix
    # mask = pointDamped(img_orig.shape, 650, 600, 450, 150, 50, .5).matrix
    stacked_mask = np.stack([mask,mask,mask]).transpose((1,2,0))

    combine = np.multiply(stacked_mask, recolored) + np.multiply(1 - stacked_mask, bgr_img_orig)

    cv2.imwrite('recolored.png', combine)
    # cv2.imshow('image', recolored)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    print "Finish"





if __name__ == '__main__':
    color_match('raw-images/melb.jpeg', 'color_model_hsv.npy')
