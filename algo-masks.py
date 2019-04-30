import numpy as np
import scipy.ndimage as ndimage


def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return np.where(mask, np.ones((h, w), dtype=np.float32), np.zeros((h, w), dtype=np.float32))


class squarePattern:

    def __init__(self, shape, a, o, f, s):

        self.matrix = np.zeros(shape, dtype=np.float32)

        for i in range(o, shape[1], f):
            for j in range(0, s):
                try:
                    self.matrix[:,i+j] = 1
                except:
                    pass


class sinusoidalPattern:

    def __init__(self, shape, a, o, f):

        x = np.linspace(0, shape[0], shape[0])
        y = np.linspace(0, shape[1], shape[1])

        xx, yy = np.meshgrid(x, y)
        sub = np.radians(xx * f + o)
        z = np.sin(sub)

        self.matrix = z.astype(dtype=np.float32)


class paraboloidPattern:

    def __init__(self, shape, a, o, f):

        self.matrix = np.zeros(shape, dtype=np.float32)

        for i in range(o, shape[1], f):
            for j in range(0, f):
                try:
                    self.matrix[:,i+j] = j / float(f)
                except:
                    pass

        self.matrix = 1 - 4 * self.matrix + 4 * self.matrix ** 2


class reverseParaboloidPattern:

    def __init__(self, shape, a, o, f):

        self.matrix = np.zeros(shape, dtype=np.float32)

        for i in range(o, shape[1], f):
            for j in range(0, f):
                try:
                    self.matrix[:, i + j] = j / float(f)
                except:
                    pass

        self.matrix = 1 - (1 - 4 * self.matrix + 4 * self.matrix ** 2)


class pointParabolic:

    def __init__(self, shape, x, y, d, f):

        self.matrix = create_circular_mask(shape[1], shape[0], (x, y), d / 2)



if __name__ == '__main__':
    import cv2
    # mat = squarePattern((500, 500), 0, 0, 50, 1)
    # mat = sinusoidalPattern((500, 500), 0, 0, 2)
    # mat = paraboloidPattern((500, 500), 0, 0, 50)
    # mat = reverseParaboloidPattern((500, 500), 0, 0, 50)
    mat = pointParabolic((500,500), 250, 250, 30, 2)

    print mat.matrix

    img_mat = cv2.cvtColor(mat.matrix, cv2.COLOR_GRAY2BGR)

    cv2.imshow('image', img_mat)
    cv2.waitKey(0)

    cv2.destroyAllWindows()












