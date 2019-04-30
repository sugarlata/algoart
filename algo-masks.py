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
    matrix = np.where(mask, np.ones((h, w), dtype=np.float32), np.zeros((h, w), dtype=np.float32))

    return matrix, mask


def create_donut_mask(h, w, f, center=None, radius=None):

    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    full_mask = dist_from_center <= radius + f
    inner_mask = radius <= dist_from_center
    mask = np.logical_and(full_mask, inner_mask)

    donut_dist = 1 - (dist_from_center.astype(np.float32) - radius) / f

    matrix = np.where(mask, donut_dist, np.zeros((h, w), dtype=np.float32))

    return matrix, mask


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

    def __init__(self, shape, x, y, r, f):

        circle_matrix, _ = create_circular_mask(shape[1], shape[0], (x, y), r)
        linear_donut_matrix, _ = create_donut_mask(shape[1], shape[0], f, (x, y), r)
        parabolic_donut_matrix = linear_donut_matrix ** 2
        self.matrix = circle_matrix + parabolic_donut_matrix


class pointReverseParabolic:

    def __init__(self, shape, x, y, r, f):

        circle_matrix, _ = create_circular_mask(shape[1], shape[0], (x, y), r)
        linear_donut_matrix, _ = create_donut_mask(shape[1], shape[0], f, (x, y), r)
        parabolic_donut_matrix = -1 * linear_donut_matrix ** 2 + 2 * linear_donut_matrix
        self.matrix = circle_matrix + parabolic_donut_matrix


class pointLinear:

    def __init__(self, shape, x, y, r, f):
        circle_matrix, _ = create_circular_mask(shape[1], shape[0], (x, y), r)
        linear_donut_matrix, _ = create_donut_mask(shape[1], shape[0], f, (x, y), r)
        self.matrix = circle_matrix + linear_donut_matrix


class pointSinusoidal:

    def __init__(self, shape, x, y, r, f):
        circle_matrix, _ = create_circular_mask(shape[1], shape[0], (x, y), r)
        linear_donut_matrix, _ = create_donut_mask(shape[1], shape[0], f, (x, y), r)
        sinusoidal_donut_matrix = np.sin(linear_donut_matrix * np.pi / 2)
        self.matrix = circle_matrix + sinusoidal_donut_matrix


class pointDamped:

    def __init__(self, shape, x, y, r, s, f, o):
        circle_matrix, circle_mask = create_circular_mask(shape[1], shape[0], (x, y), r)
        linear_donut_matrix, donut_mask = create_donut_mask(shape[1], shape[0], s, (x, y), r)

        sinusoidal_donut_matrix = np.where(donut_mask, np.cos((f * (1 - linear_donut_matrix) * np.pi / 2)), 0)

        self.matrix = sinusoidal_donut_matrix + circle_matrix


if __name__ == '__main__':
    import cv2
    # mat = squarePattern((500, 500), 0, 0, 50, 1)
    # mat = sinusoidalPattern((500, 500), 0, 0, 2)
    # mat = paraboloidPattern((500, 500), 0, 0, 50)
    # mat = reverseParaboloidPattern((500, 500), 0, 0, 50)
    # mat2 = pointParabolic((500,500), 250, 250, 100, 100)
    # mat = pointLinear((500,500), 250, 250, 100, 100)
    # mat = pointSinusoidal((500,500), 250, 250, 100, 100)
    # mat1 = pointReverseParabolic((500,500), 250, 250, 100, 100)
    mat1 = pointDamped((500,500), 250, 250, 100, 100, 1, 2)

    img_mat = cv2.cvtColor(mat1.matrix, cv2.COLOR_GRAY2BGR)
    # img_mat2 = cv2.cvtColor(mat2.matrix, cv2.COLOR_GRAY2BGR)

    cv2.imshow('image', img_mat)
    # cv2.imshow('image2', img_mat2)

    cv2.waitKey(0)

    cv2.destroyAllWindows()












