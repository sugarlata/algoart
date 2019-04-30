import os
import cv2
from time import sleep
from scipy import spatial as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


def do_kdtree(combined_x_y_arrays,points):
    mytree = sp.cKDTree(combined_x_y_arrays)
    dist, indexes = mytree.query(points)
    return indexes


class ColorMatch:

    def __init__(self):
        self.model_path = 'model-images/'
        self.color_array = None


    def create_model(self):

        fn = os.path.join(self.model_path, '9uvmn7doasi01.jpg')

        # Open Image
        m_img = cv2.imread(fn)

        img = cv2.cvtColor(m_img, cv2.COLOR_BGR2HSV)

        print 'Points:', img.shape[0] * img.shape[1]

        # Only get unique points
        img_array = np.asarray(img).reshape((img.shape[0] * img.shape[1], 3))

        unq_col, count_ind = np.unique(img_array, axis=0, return_counts=True)

        print unq_col.shape

        for i in range(len(count_ind)):

            if count_ind[i] < 100:
                # print "Too small pixels:", unq_col[i]
                unq_col[i] = np.nan

        unq_col = np.unique(unq_col, axis=0)
        print unq_col.shape

        # Plot

        self.color_array = unq_col

        # Cluster???

    def save_model(self, model_fn):

        np.save(model_fn, self.color_array)

    def load_model(self, model_fn):

        c_array = np.load(model_fn)
        self.color_array = c_array

    def plot_model(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.color_array[:,0], self.color_array[:,1], self.color_array[:,2])

        plt.show()

    def match_color(self, color_list):

        results = do_kdtree(self.color_array, color_list)
        return results, self.color_array





if __name__ == '__main__':
    cm = ColorMatch()
    cm.create_model()
    cm.save_model('color_model_hsv.npy')
    # cm.load_model('color_model.npy')
    # cm.plot_model()
    # cm.match_color(np.asarray([[0, 155, 45], [234, 64, 186]]))






