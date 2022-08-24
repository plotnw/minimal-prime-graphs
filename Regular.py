import sage.all
import sage.graphs
import MinimalPrimeGraph
import MinimalPrimeGraphExamples

def construct_regular(n, k):
    g = graphs.CompleteGraph(n).complement().copy()
    for i in g.vertices():
        for j in g.vertices():
            diff = (i - j) % n
            if k <= diff <= (2*k-1):
                g.add_edge(i,j)
    g.name("TFRG_" + str(n) + "_" + str(k))
    return g

def construct_regular_complement(n, k):
    g = construct_regular(n, k).copy()
    g = g.complement()
    g.name("TFRG_" + str(n) + "_" + str(k) + "_c")
    return g

BASE = []
for n in range (5, 100):
    for k in range((n+2)//6, n-1):
        g = construct_regular_complement(n,k)
        if g.is_minimal_prime_graph():
            is_base_graph = g.is_base_graph()
            if is_base_graph:
                BASE.append(g)
