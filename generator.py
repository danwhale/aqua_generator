from itertools import chain
import math, time, sys, random, numpy as np, copy
import json, plotly.graph_objs as go, networkx as nx
from plotly import tools
from plotly.offline import plot
from utils import *

class Generator:
    def __init__(self, N, m, r):
        self.N = N
        self.G = nx.Graph()
        self.m = m
        self.r = r
        #initialize nodes
        for i in range(N):
            self.G.add_node(i, vector=np.random.random_sample((5,)),
                            rating=np.random.randint(1, 6), pop_sim = np.random.uniform())

        self.rand_edge = random.Random()
        self.rand_edge.seed('edges')
        self.rand_remove = random.Random()
        self.rand_remove.seed('remove')

        self.plot_data = []

    def restart(self):
        self.G.remove_edges_from(self.G.edges)
        self.plot_data = []

    def get_probs(self, graph, u, eps):
        res = []
        sum_rating = sum([graph.nodes[v]['rating'] for v in graph.nodes])
        for n in graph.nodes():  # список узлов всегда упорядочен
            if n == u:
                res.append(0)
            else:
                res.append(self._edge_prob(graph, u, n, sum_rating, graph.nodes[u]['pop_sim']))
        return res

    def _edge_prob(self,graph, u, v, sum_rating, eps):
        

        sim_p = cosine_similarity(graph.nodes[u]['vector'],graph.nodes[v]['vector'])

        # check if the resulting probability is in [0;1]
        if sim_p < 0 or sim_p > 1:
            raise NameError('Prob Sim is not in range. P=' + str(sim_p))

        pop_p = graph.nodes[v]['rating'] /  sum_rating

        if pop_p < 0 or pop_p > 1:
            raise NameError('Prob Pop is not in range. P=' + str(pop_p))
        return (eps * sim_p + (1 - eps) * pop_p)



    def step(self):
        for i in range(0, self.N):
            for j in range(self.m):
                self.probs = self.get_probs(self.G, i, self.G.nodes[i]['pop_sim'])

                s = sum(self.probs)

                r = self.rand_edge.uniform(0, s)
                k = -1
                while r >= 0:
                    k += 1
                    r -= self.probs[k]
                    

                self.G.add_edge(i, k)

            for i in range(0, self.N):
                if self.G.degree(i) > 0 and self.rand_remove.uniform(0,1) < self.r:
                    d = {nb:self.probs[nb] for nb in self.G.neighbors(i)}
                    to_remove = min(d, key = d.get)
                    self.G.remove_edge(i,to_remove)
                        
           #plot_data.append(plot_graph(G, pos))
            #pos = nx.spring_layout(G, pos=pos)
        #return G, #plot_data