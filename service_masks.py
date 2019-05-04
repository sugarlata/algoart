import numpy as np
import scipy.ndimage as ndimage
from scipy import ndimage
import cv2


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


class Common:

    def get_matrix(self):
        print self.matrix.shape
        return cv2.cvtColor(self.matrix, cv2.COLOR_GRAY2BGR)


class squarePattern(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.a = 0
        self.o = 0
        self.f = 20
        self.s = 20
        self.mode = None
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': True,
            'a': True,
            'f': True,
            'o': True,
            's': True,
            'x': False,
            'y': False,
            'r': False,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Square Pattern'

    def recalc(self):

        if self.mode is None:
            self.mode = 'wrap'

        matrix = np.zeros(self.shape, dtype=np.float32)

        for i in range(self.o, self.shape[1], self.f):
            for j in range(0, self.s):
                try:
                    matrix[:, i+j] = 1
                except:
                    pass

        if self.a != 0:
            self.matrix = None
            self.matrix = ndimage.rotate(matrix, self.a, reshape=False, mode=self.mode)

        else:
            self.matrix = None
            self.matrix = matrix

    def get_matrix(self):
        return self.matrix


class sinusoidalPattern(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.a = 0
        self.o = 20
        self.f = 20
        self.mode = None
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': True,
            'a': True,
            'f': True,
            'o': True,
            's': False,
            'x': False,
            'y': False,
            'r': False,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Sinusoidal Pattern'

    def recalc(self):

        if self.mode is None:
            self.mode = 'wrap'

        x = np.linspace(0, self.shape[1], self.shape[1])
        y = np.linspace(0, self.shape[0], self.shape[0])

        xx, yy = np.meshgrid(x, y)
        sub = np.radians(xx * self.f + self.o)
        z = np.sin(sub)

        matrix = z.astype(dtype=np.float32)

        mask_matrix = np.less(matrix, 0)
        matrix = np.where(mask_matrix, 0, matrix)

        if self.a != 0:
            self.matrix = ndimage.rotate(matrix, self.a, reshape=False, mode=self.mode)

        else:
            self.matrix = matrix


class paraboloidPattern(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.a = 0
        self.o = 20
        self.f = 20
        self.mode = None
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': True,
            'a': True,
            'f': True,
            'o': True,
            's': False,
            'x': False,
            'y': False,
            'r': False,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Paraboloid Pattern'

    def recalc(self):

        if self.mode is None:
            self.mode = 'wrap'

        matrix = np.zeros(self.shape, dtype=np.float32)

        for i in range(self.o, self.shape[1], self.f):
            for j in range(0, self.f):
                try:
                    matrix[:, i + j] = j / float(self.f)
                except:
                    pass

        matrix = 1 - 4 * matrix + 4 * matrix ** 2

        if self.a != 0:
            self.matrix = ndimage.rotate(matrix, self.a, reshape=False, mode=self.mode)

        else:
            self.matrix = matrix

    def get_matrix(self):
        return self.matrix


class reverseParaboloidPattern(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.a = 0
        self.o = 20
        self.f = 20
        self.mode = None
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': True,
            'a': True,
            'f': True,
            'o': True,
            's': False,
            'x': False,
            'y': False,
            'r': False,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Reverse Paraboloid Pattern'

    def recalc(self):

        if self.mode is None:
            self.mode = 'wrap'

        matrix = np.zeros(self.shape, dtype=np.float32)

        for i in range(self.o, self.shape[1], self.f):
            for j in range(0, self.f):
                try:
                    matrix[:, i + j] = j / float(self.f)
                except:
                    pass

        matrix = 1 - (1 - 4 * matrix + 4 * matrix ** 2)

        if self.a != 0:
            self.matrix = ndimage.rotate(matrix, self.a, reshape=False, mode=self.mode)

        else:
            self.matrix = matrix

    def get_matrix(self):
        return self.matrix


class pointParabolic(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.x = 0
        self.y = 0
        self.r = 20
        self.f = 20
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': False,
            'a': False,
            'f': True,
            'o': False,
            's': False,
            'x': True,
            'y': True,
            'r': True,
            'cut_before': False,
            'add-mult': False,
        }
        self.str_text = 'Parabolic Point'

    def recalc(self):

        circle_matrix, _ = create_circular_mask(self.shape[0], self.shape[1], (self.x, self.y), self.r)
        linear_donut_matrix, _ = create_donut_mask(self.shape[0], self.shape[1], self.f, (self.x, self.y), self.r)
        parabolic_donut_matrix = linear_donut_matrix ** 2
        self.matrix = circle_matrix + parabolic_donut_matrix


class pointReverseParabolic(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.x = 0
        self.y = 0
        self.r = 20
        self.f = 20
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': False,
            'a': False,
            'f': True,
            'o': False,
            's': False,
            'x': True,
            'y': True,
            'r': True,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Reverse Parabolic Point'

    def recalc(self):

        circle_matrix, _ = create_circular_mask(self.shape[0], self.shape[1], (self.x, self.y), self.r)
        linear_donut_matrix, _ = create_donut_mask(self.shape[0], self.shape[1], self.f, (self.x, self.y), self.r)
        parabolic_donut_matrix = -1 * linear_donut_matrix ** 2 + 2 * linear_donut_matrix
        self.matrix = circle_matrix + parabolic_donut_matrix


class pointLinear(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.x = 0
        self.y = 0
        self.r = 20
        self.f = 20
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': False,
            'a': False,
            'f': True,
            'o': False,
            's': False,
            'x': True,
            'y': True,
            'r': True,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Linear Point'

    def recalc(self):
        circle_matrix, _ = create_circular_mask(self.shape[0], self.shape[1], (self.x, self.y), self.r)
        linear_donut_matrix, _ = create_donut_mask(self.shape[0], self.shape[1], self.f, (self.x, self.y), self.r)
        self.matrix = circle_matrix + linear_donut_matrix


class pointSinusoidal(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.x = 0
        self.y = 0
        self.r = 20
        self.f = 20
        self.a = 1
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': False,
            'a': True,
            'f': True,
            'o': False,
            's': False,
            'x': True,
            'y': True,
            'r': True,
            'cut_before': False,
            'add-mult': False,
        }

        self.str_text = 'Sinusoidal Point'

    def recalc(self):

        circle_matrix, _ = create_circular_mask(self.shape[0], self.shape[1], (self.x, self.y), self.r)
        linear_donut_matrix, _ = create_donut_mask(self.shape[0], self.shape[1], self.f, (self.x, self.y), self.r)
        sinusoidal_donut_matrix = np.sin(self.a * linear_donut_matrix * np.pi / 2)

        matrix = circle_matrix + sinusoidal_donut_matrix

        mask_matrix = np.less(matrix, 0)
        matrix = np.where(mask_matrix, 0, matrix)

        self.matrix = matrix


class pointDamped(Common):

    def __init__(self):

        self.shape = (100, 100)
        self.x = 0
        self.y = 0
        self.r = 20
        self.s = 20
        self.f = 0.2
        self.o = 0
        self.cut_before = False
        self.matrix = None

        self.vars_allowed = {
            'shape': True,
            'mode': False,
            'a': False,
            'f': True,
            'o': True,
            's': True,
            'x': True,
            'y': True,
            'r': True,
            'cut_before': True,
            'add-mult': False,
        }

        self.str_text = 'Damped Point'

    def recalc(self):

        circle_matrix, circle_mask = create_circular_mask(self.shape[0], self.shape[1], (self.x, self.y), self.r)
        linear_donut_matrix, donut_mask = create_donut_mask(self.shape[0], self.shape[1], self.s, (self.x, self.y), self.r)

        sinusoidal_donut_matrix = self.o * np.cos((self.f * (1 - linear_donut_matrix) * np.pi / 2)) - (self.o - 1)


        if self.cut_before:

            below_mask = np.less(sinusoidal_donut_matrix, 0)
            # Apply Below Mask
            below_matrix = np.where(below_mask, 0, sinusoidal_donut_matrix)
            # Apply Donut Mask
            donut_matrix = np.where(donut_mask, below_matrix, 0)

            self.matrix = np.multiply(donut_matrix, linear_donut_matrix) + circle_matrix


        else:

            # Dampen Matrix
            matrix = np.multiply(sinusoidal_donut_matrix, linear_donut_matrix)

            # Apply Donut Mask
            dp_matrix = np.where(donut_mask, matrix, 0)

            # Apply Below Mask
            below_mask = np.less(dp_matrix, 0)
            donut_matrix = np.where(below_mask, 0, dp_matrix)

            self.matrix = donut_matrix + circle_matrix


if __name__ == '__main__':
    import cv2
    mat = squarePattern()
    mat.shape = (500, 500)
    mat.a = 0
    mat.f = 50
    mat.s = 5
    mat.o = 0

    mat.recalc()
    # mat = sinusoidalPattern((500, 500), 45, 0, 2, mode='mirror')
    # mat = paraboloidPattern((500, 500), 35, 0, 50)
    # mat = reverseParaboloidPattern((500, 500), 35, 0, 50)
    # mat2 = pointParabolic((500,500), 250, 250, 100, 100)
    # mat = pointLinear((500,500), 250, 250, 100, 100)
    # mat = pointSinusoidal((500,500), 250, 250, 100, 100)
    # mat1 = pointReverseParabolic((500,500), 250, 250, 100, 100)
    # mat1 = pointDamped((500,500), 250, 250, 100, 100, 50, 0.5)
    # mat1 = pointDamped((500,500), 150, 250, 100, 100, 20, 0.5)
    # mat2 = pointDamped((500,500), 350, 250, 100, 100, 20, 0.5)

    # img_mat = cv2.cvtColor(mat.matrix, cv2.COLOR_GRAY2BGR)
    # img_mat2 = cv2.cvtColor(mat2.matrix, cv2.COLOR_GRAY2BGR)

    cv2.imshow('image', mat.matrix)
    cv2.moveWindow('image', 0, 0)
    # cv2.imshow('image2', img_mat2)

    cv2.waitKey(0)

    cv2.destroyAllWindows()












