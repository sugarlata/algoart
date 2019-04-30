import os
import cv2
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

class ColorMatch:

    def __init__(self):
        self.model_path = 'model-images/'


    def create_model(self):

        fn = os.path.join(self.model_path, 'elg746dlqfkz.png')

        # Open Image
        img = cv2.imread(fn)
        print 'Points:', img.shape[0] * img.shape[1]

        # Only get unique points
        unq_col_set = set(tuple(v) for m2d in img for v in m2d)
        print 'Colors:', len(unq_col_set)
        unq_col = np.asarray(list(unq_col_set))
        # Plot

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        print unq_col[:,0].shape
        ax.scatter(unq_col[:,0], unq_col[:,1], unq_col[:,2])

        plt.show()



        # Cluster


    def save_model(self):
        pass

    def load_model(self):
        pass

    def match_color(self):
        pass



if __name__ == '__main__':
    cm = ColorMatch()
    cm.create_model()