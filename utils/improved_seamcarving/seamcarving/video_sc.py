from numpy import size, amax, where, empty
import numpy as np
from random import random
import maxflow


class video_seam_carving(object):
    # X: An fxnxmxc matrix (f = frame, n = rows, m = columns, c = components)
    def __init__(self, X, width_change, height_change, use_integers=True):
        self.X = X
        self.width_change = width_change
        self.height_change = height_change
        self.use_integers = use_integers

    def generate_up_down_edges(self, I, nodeids, i_inf, i_mult):
        structure = np.zeros((3, 3, 3))
        structure[1, 2, 1] = 1
        links = np.zeros(I.shape)
        links[:, 0:-1, 1:] = np.abs(I[:, 0:-1, 1:] - I[:, 1:, 0:-1])
        links = links * i_mult
        return links, structure

    def generate_down_up_edges(self, I, nodeids, i_inf, i_mult):
        structure = np.zeros((3, 3, 3))
        structure[1, 0, 1] = 1
        links = np.zeros(I.shape)
        links[:, 1:, 1:] = np.abs(I[:, 1:, 1:] - I[:, 0:-1, 0:-1])
        links = links * i_mult
        return links, structure

    def generate_left_right_edges(self, I, nodeids, i_inf, i_mult):
        structure = np.zeros((3, 3, 3))
        structure[1, 1, 2] = 1
        links = np.zeros(I.shape)
        links[:, :, 1:-1] = np.abs(I[:, :, 2:] - I[:, :, 0:-2])
        links = links * i_mult
        links[:, :, -2] = i_inf
        links[:, :, 0] = i_inf
        return links, structure

    def generate_backward_forward_edges(self, I, nodeids, i_inf, i_mult):
        structure = np.zeros((3, 3, 3))
        structure[2, 1, 1] = 1
        links = np.zeros(I.shape)
        links[0:-1, :, 1:] = np.abs(I[0:-1, :, 1:] - I[1:, :, 0:-1])
        links = links * i_mult
        return links, structure

    def generate_forward_backward_edges(self, I, nodeids, i_inf, i_mult):
        structure = np.zeros((3, 3, 3))
        structure[0, 1, 1] = 1
        links = np.zeros(I.shape)
        links[1:, :, 0:-1] = np.abs(I[0:-1, :, 0:-1] - I[1:, :, 1:])
        links = links * i_mult
        return links, structure

    def generate_graph(self, I):
        g = maxflow.Graph[float]()
        i_inf = np.inf
        i_mult = 1

        if self.use_integers:
            g = maxflow.Graph[int]()
            i_inf = 10000000
            i_mult = 10000

        nodeids = g.add_grid_nodes(I.shape)

        links, structure = self.generate_left_right_edges(
            I, nodeids, i_inf, i_mult)
        g.add_grid_edges(nodeids, structure=structure,
                         weights=links, symmetric=False)
        links, structure = self.generate_up_down_edges(
            I, nodeids, i_inf, i_mult)
        g.add_grid_edges(nodeids, structure=structure,
                         weights=links, symmetric=False)
        links, structure = self.generate_down_up_edges(
            I, nodeids, i_inf, i_mult)
        g.add_grid_edges(nodeids, structure=structure,
                         weights=links, symmetric=False)

 # Diagonali su singola immagine
        structure = np.zeros((3, 3, 3))
        structure[1, :, 0] = i_inf
        structure[2, 1, 0] = i_inf
        structure[0, 1, 0] = i_inf
        g.add_grid_edges(nodeids, structure=structure)

        links, structure = self.generate_backward_forward_edges(
            I, nodeids, i_inf, i_mult)
        g.add_grid_edges(nodeids, structure=structure,
                         weights=links, symmetric=False)
        links, structure = self.generate_forward_backward_edges(
            I, nodeids, i_inf, i_mult)
        g.add_grid_edges(nodeids, structure=structure,
                         weights=links, symmetric=False)

        g.add_grid_tedges(nodeids[:, :, 0], i_inf, 0)
        g.add_grid_tedges(nodeids[:, :, -1], 0, i_inf)
        return g, nodeids

    def graph_cut(self, I):
        g, nodeids = self.generate_graph(I)
        g.maxflow()
        pathMap = g.get_grid_segments(nodeids)
        I = (pathMap == False).sum(2) - 1
        del g
        return I, pathMap

    # This method applies the merge in two steps:
    # * Deletion: For each row, deletes a value according to I.
    # * Merge/substitution: For each row, it replaces the actual value of the seam with it's look-forwarded version, according to I
    # The only exception is Z, that is not precomputed and should be calculated in real time.

    def apply_seam_carving(self, I, mask, Simg, Z):
        reduced_size_1, reduced_size_2, reduced_size_3 = size(
            Simg, 0), size(Simg, 1), size(Simg, 2) - 1
        SimgCopy = Simg[mask].reshape(
            reduced_size_1, reduced_size_2, reduced_size_3)
        ZCopy = Z[mask].reshape(
            reduced_size_1, reduced_size_2, reduced_size_3, Z.shape[3])
        return SimgCopy, ZCopy

    def makeEdge(self, A):
        X = np.ones_like(A)
        X[:, :, 0:-1] = A[:, :, 1:]
        return np.invert(A ^ X)

    def generate(self):
        X = self.X
        S = X.astype(np.float64).sum(axis=3) / 3

        Z = np.copy(X)

        # Cloning S
        Simg = np.copy(S)

        num_seams = abs(self.width_change + self.height_change)
        # For each seam I want to merge
        for i in xrange(num_seams):
            print str(i + 1) + ' of ' + str(num_seams)
            I, pathMap = self.graph_cut(Simg)
            mask = self.makeEdge(pathMap)
            Simg, Z = self.apply_seam_carving(I, mask, Simg, Z)

        return Z
