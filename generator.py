from itertools import chain
import math, time, sys, random, numpy as np, copy
import numpy as np, json, plotly.graph_objs as go, networkx as nx
from plotly import tools
from plotly.offline import plot

class Generator:
    def __init__(self, N, m, r):
        self.G = nx.Graph(N=N)
        self.m = m
        self.r = r
        #initialize nodes
        for i in range(N):
            self.G.add_node(i, vector=np.random.random_sample((5,)),
                            rating=np.random.randint(1, 6), pop_sim = np.random.uniform())

        self.rand_edge = random.Random()
        self.rand_edge.seed('edges')

        self.plot_data = []

    def restart(self):
        self.G.remove_edges_from(self.G.edges)
        self.plot_data = []

    def get_probs(self, graph, u, eps):
        res = []
        sum_mods = sum([abs(graph.degree(u) - graph.degree(v)) for v in graph.nodes])
        sum_deg = sum([graph.degree(v) for v in graph.nodes])
        for n in graph.nodes():  # список узлов всегда упорядочен
            if n == u:
                res.append(0)
            else:
                res.append(self._edge_prob(graph, u, n, sum_mods, sum_deg, eps))
        return res

    def _edge_prob(graph, u, v, sum_mods, sum_deg, eps):
        this_k = graph.degree(u)  # this node degree
        k = graph.degree(v)  # target node degree

        sim_p = (1 - abs(this_k - k) / sum_mods) / (len(graph) - 1)

        # check if the resulting probability is in [0;1]
        if sim_p < 0 or sim_p > 1:
            raise NameError('Prob Sim is not in range. P=' + str(sim_p))

        pop_p = k / sum_deg

        if pop_p < 0 or pop_p > 1:
            raise NameError('Prob Pop is not in range. P=' + str(pop_p))
        return (eps * sim_p + (1 - eps) * pop_p)



    def step(self):
        for i in range(0, self.N):
            print(i)
            for j in range(self.m):
                probs = self.get_probs(self.G, i, self.G.nodes[i]['pop_sim'])

                s = sum(probs)

                r = self.rand_edge.uniform(0, s)
                k = 0
                while r >= 0:

                    r -= probs[k]
                    k += 1

                self.G.add_edge(i, k)

            for i in range(0, self.N):
                if self.G.degree(i) > 0:

           #plot_data.append(plot_graph(G, pos))
            #pos = nx.spring_layout(G, pos=pos)
        #return G, #plot_data

