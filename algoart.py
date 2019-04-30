import cv2
import numpy as np


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




if __name__ == '__main__':
    main()