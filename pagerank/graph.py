'''
Graph - Models a graph with an implementation of the PageRank algorithm.
Copyright (C) 2020  Hugo Fonseca Diaz
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import numpy as np
np.seterr(divide = "ignore", invalid = "ignore")

class Graph:
    def __init__(self, edges):
        # PageRank values
        self.PR = { }
        # Adjacency Matrix
        self.M = self.__get_M__(edges)

    def page_rank(self, damping = 0.85, limit = 1.0e-8):
        M = self.__stochastic__(self.M) # Stochastic matrix
        N = M.shape[1] # Number of nodes
        v = np.full((1, N), (1 / N)) 
        v = v / np.linalg.norm(v, 1)
        R = (1 - damping) / N + damping * M
        while True: # While the result is over the limit
            prev_v = v
            v = np.dot(v, R)
            if np.linalg.norm(v - prev_v, 2) <= limit: 
                break
        # Dictionary with the PR values
        # key = node, value = PR(node)
        pos = 0
        for n in self.PR.keys():
            self.PR[n] = v[0, pos]
            pos += 1
        return self.PR

    def __get_M__(self, edges):
        # Returns the adjacency matrix
        # Get the unique nodes from the edges tuples
        aux = set(e[0] for e in edges)
        unique_nodes = aux.union(set(e[1] for e in edges))

        # Dictionary: key = node, value = position
        nodes = { }
        pos = 00
        for n in sorted(list(unique_nodes)):
            self.PR[n] = 0 # PageRank values dictionary
            nodes[n] = pos
            pos += 1

        # The matrix is created
        num_nodes = len(nodes)
        M = np.zeros((num_nodes, num_nodes))
        for e in edges:
            row = nodes[e[0]]
            col = nodes[e[1]]
            M[row][col] = 1
        return M

    def __stochastic__(self, matrix):
        # The matrix is normalized
        row_sums = matrix.sum(axis=1)
        normalized = matrix / row_sums[:, np.newaxis]
        normalized[np.isnan(normalized)] = 0
        # Stochastic matrix
        z = np.where(~normalized.any(axis=1))[0]
        for row in z:
            normalized[row] = (1 / matrix.shape[1])
        return normalized

