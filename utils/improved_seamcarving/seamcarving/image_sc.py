from numpy import concatenate, size, ones, zeros
import numpy as np
import maxflow
import cv2


class image_seam_carving(object):
    #
    # X: input image
    # width_change  : Number of columns to be deleted
    # height_change  : Number of rows to be deleted
    #
    def __init__(self, X, width_change, height_change, use_integers=True):
        self.X = X
        self.width_change = width_change
        self.height_change = height_change
        self.use_integers = use_integers
        self.seams = np.empty((abs(width_change), X.shape[0]))

    def initD(self, Simg):
        return zeros((size(Simg, 0), size(Simg, 1) - 1))

    def find_neighborhood(self, image, node):
        index = np.unravel_index((node), image.shape)
        unraveled = ((index[0] + 1, index[1] - 1), (index[0] +
                                                    1, index[1]), (index[0] + 1, index[1] + 1))
        return unraveled

    def find_node(self, index, image):
        if index[0] < 0 or index[0] >= image.shape[0] or index[1] >= image.shape[1] or index[1] < 0:
            return None
        else:
            return np.ravel_multi_index(index, image.shape)

    def generate_graph(self, I):
        g = maxflow.Graph[float]()
        i_inf = np.inf
        i_mult = 1

        if self.use_integers:
            g = maxflow.Graph[int]()
            i_inf = 10000000
            i_mult = 10000

        nodeids = g.add_grid_nodes(I.shape)
        links = zeros((I.shape[0], I.shape[1], 4))

        # SU
        # LR I(i,j+1)- I(i,j-1) (SU)
        links[:, 1:-1, 0] = np.abs(I[:, 2:] - I[:, 0:-2])

        links[:, -2, 0] = i_inf
        links[:, 0, 0] = i_inf

        # -LU I(i+1,j)- I(i,j-1) (DESTRA)
        links[0:-1, 1:, 1] = np.abs(I[1:, 1:] - I[0:-1, 0:-1])

        # LU (SINISTRA)
        # I(i-1,j)-I(i,j-1)
        links[1:, 1:, 2] = np.abs(I[0:-1, 1:] - I[1:, 0:-1])

        # GIU
        links[:, :, 3] = i_inf

        links = links * i_mult

        structure = np.array([[i_inf, 0, 0],
                              [i_inf, 0, 0],
                              [i_inf, 0, 0]
                              ])
        g.add_grid_edges(nodeids, structure=structure, symmetric=False)

        # From Left to Right
        weights = links[:, :, 0]
        structure = np.zeros((3, 3))
        structure[1, 2] = 1
        g.add_grid_edges(nodeids, structure=structure,
                         weights=weights, symmetric=False)

        # GIU = destra
        weights = links[:, :, 1]
        structure = np.zeros((3, 3))
        structure[2, 1] = 1
        g.add_grid_edges(nodeids, structure=structure,
                         weights=weights, symmetric=False)

        # SU = sinistra
        weights = links[:, :, 2]
        structure = np.zeros((3, 3))
        structure[0, 1] = 1
        g.add_grid_edges(nodeids, structure=structure,
                         weights=weights, symmetric=False)

        left_most = concatenate((np.arange(I.shape[0]).reshape(
            1, I.shape[0]), zeros((1, I.shape[0])))).astype(np.uint64)
        left_most = np.ravel_multi_index(left_most, I.shape)
        g.add_grid_tedges(left_most, i_inf, 0)

        right_most = concatenate((np.arange(I.shape[0]).reshape(1, I.shape[0]), ones(
            (1, I.shape[0])) * (size(I, 1) - 1))).astype(np.uint64)
        right_most = np.ravel_multi_index(right_most, I.shape)
        g.add_grid_tedges(right_most, 0, i_inf)
        return g, nodeids

    def graph_cut(self, I):
        g, nodeids = self.generate_graph(I)
        g.maxflow()
        I = g.get_grid_segments(nodeids)
        I = (I == False).sum(1) - 1
        I = I.reshape(I.shape[0], 1)
        return I

    def apply_seam_carving_reduce(self, I, Simg, Z):
        reduced_size_1, reduced_size_2 = size(Simg, 0), size(Simg, 1) - 1

        # Deletion:
        # Generating a deletion mask n x m. It's a binary matrix that contains True if the pixel should be keeped, False if they should be deleted.
        # The total number of Falses and Trues at each like should be the same.
        # Applying that matrix to a standard numpy array, it efficiently generates a clone matrix with the deleted values
        mask = np.arange(size(Z, 1)) != np.vstack(I)
        SimgCopy = Simg[mask].reshape(reduced_size_1, reduced_size_2)
        ZCopy = Z[mask].reshape(reduced_size_1, reduced_size_2, Z.shape[2])
        return SimgCopy, ZCopy

# for enlarge
    def insert_indices(self, A, B, C, index_map):
        return np.insert(A.ravel(), index_map, B[xrange(B.shape[0]), C]).reshape(A.shape[0], A.shape[1] + 1)

    # Given A, B, C, transforms indices from 3d to flattern forms for A and B, given C
    def find_indices3(self, A, B, C):
        mi = np.ravel_multi_index([np.arange(A.shape[0]), C], A.shape[:2])
        mi2 = np.ravel_multi_index([np.arange(B.shape[0]), C], B.shape[:2])
        return mi, mi2

    # Given A, B, C, and multi-indexes, inserts elements from B in A according to the indexes
    def insert_indices3(self, A, B, mi, mi2):
        bvals = np.take(B.reshape(-1, B.shape[-1]), mi2, axis=0)
        return np.insert(A.reshape(-1, A.shape[2]), mi + 1, bvals, axis=0).reshape(A.shape[0], -1, A.shape[2])

    def apply_seam_carving_enlarge(self, I, Simg, Z):
        I = I.astype(np.uint64)
        index_map = np.ravel_multi_index(
            (xrange(Simg.shape[0]), I), Simg.shape) + 1
        SimgCopy = self.insert_indices(Simg, Simg, I, index_map)
        mi, m2 = self.find_indices3(Z, Z, I)
        ZCopy = self.insert_indices3(Z, Z, mi, m2)

        return SimgCopy, ZCopy
		
    def generate(self):
        X = self.X
        S = cv2.cvtColor(X, cv2.COLOR_BGR2GRAY).astype(np.float64)
        Z = np.copy(X)

        # Cloning S [To be fixed]
        Simg = np.copy(S)

        # For each seam I want to merge
        num_seams = abs(self.width_change) # + self.height_change
        for i in xrange(num_seams):
            print str(i + 1) + ' of ' + str(num_seams)
            # pathmap is a matrix that, for each position, specifies the best direction
            # to be taken to minimize the cost.
            pix = self.graph_cut(Simg)

            I = pix.transpose()[0]
            self.seams[i] = I
            if self.width_change < 0:
                Simg, Z = self.apply_seam_carving_reduce(I, Simg, Z)
            else:
                Simg, Z = self.apply_seam_carving_enlarge(I, Simg, Z)

        return Z
