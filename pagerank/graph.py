'''
Graph - Models a graph and contains an implementation the PageRank algorithm.
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

class Graph:
    def __init__(self, edges):
        # Adjacency Matrix
        self.M = self.__get_M__(edges)

    def page_rank(self, d = 0.85, limit = 1.0e-8):
        N = self.M.shape[1]
        v = np.random.rand(N, 1)
        v = v / np.linalg.norm(v, 1)
        M_hat = (d * self.M + (1 - d) / N)
        while True:
            prev_v = v
            v = M_hat @ v # Matrix multiplication
            if np.linalg.norm(v - prev_v, 2) <= limit): break
        return v

    def __get_M__(self, edges):
        # Returns the adjacency matrix
        # Get the unique nodes from the edges tuples
        aux = set(e[0] for e in edges)
        unique_nodes = aux.union(set(e[1] for e in edges))

        # Dictionary: key = node, value = position
        nodes = { }
        pos = 00
        for n in sorted(list(unique_nodes)):
            nodes[n] = pos
            pos += 1

        # The matrix is created
        num_nodes = len(nodes)
        M = np.zeros((num_nodes, num_nodes)
        for e in edges:
            row = nodes[e[0]]
            col = nodes[e[1]]
            M[row][col] = 1
        return M



