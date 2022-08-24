from sage.all import *
import sage.graphs.graph
from sage.graphs.generators.basic import CycleGraph


def is_prime_graph(g: sage.graphs.graph.Graph) -> bool:
    """
    Check if a graph is a prime graph
    :param g: Input graph
    :return: Boolean value for whether g is a prime graph or not
    """
    if len(g.vertices()) <= 2:
        return False
    if not g.is_connected():
        return False
    h = g.complement()
    if not h.is_triangle_free():
        return false
    if not h.chromatic_number() <= 3:
        return false
    return True


def is_minimal_prime_graph(g: sage.graphs.graph.Graph) -> bool:
    """
    Checks if a graph is a minimal prime graph
    :param g: Input graph
    :return: Boolean value for whether g is a minimal prime graph or not
    """
    if len(g.vertices()) <= 2:
        return False
    if not g.is_connected():
        return False
    h = g.complement()
    if not h.is_triangle_free():
        return false
    if not h.chromatic_number() <= 3:
        return false
    for edge in g.edges():
        h.add_edge(edge)
        # probably inefficient - could try enumerating all colorings of h and check if there is a coloring of h where
        # e doesnt break it since each chromatic number is exponential i think, this would mean 1 exponential + a
        # linearish thing (in # of colorings) triangle free can do something similar, make table of which edges would
        # introduce triangle triangle free is polynomial though and table would be n^3 so idk if it helps _that_ much
        # still worth looking into
        if (h.is_triangle_free()) and h.chromatic_number() <= 3:
            return False
        h.delete_edge(edge)
    return True


class IsMinimalPrimeGraphDetail:
    graph: sage.graphs.graph.Graph
    connected: bool
    vertices: int
    bad_edges: list
    fail: int

    def __str__(self):
        if self.fail == 0:
            return "Passed"
        elif self.fail == 1:
            return "Graph not connected"
        elif self.fail == 2:
            return "Graph had <= 2 vertices"
        elif self.fail == 3:
            return "Graph not minimal"
        elif self.fail == 4:
            return "Complement not triangle free"
        elif self.fail == 5:
            return "Complement not 3-colorable"
        else:
            return "None"

    def __init__(self):
        self.graph = Graph()
        self.connected = false
        self.vertices = -1
        self.bad_edges = []
        self.fail = -1

    def __init__(self, graph, connected, vertices):
        self.graph = graph
        self.connected = connected
        self.vertices = vertices
        self.bad_edges = []
        self.fail = -1


def is_minimal_prime_graph_detail(g: sage.graphs.graph.Graph) -> IsMinimalPrimeGraphDetail:
    """
    Check if a graph is a minimal prime graph and returns a set of information to allow for determination of why the
    graph is not minimal
    :param g: Input graph
    :return: An IsMinimalPrimeGraphDetail object containing artifacts from the checking process
    """
    m = IsMinimalPrimeGraphDetail(g, g.is_connected, len(g.vertices()))
    if not m.connected:
        m.fail = 1
    if m.vertices <= 2:
        m.fail = 2
    h = g.complement()
    if not h.is_triangle_free():
        m.fail = 4
    if not h.chromatic_number() <= 3:
        m.fail = 5
    for edge in g.edges():
        h.add_edge(edge)
        if (h.is_triangle_free()) and h.chromatic_number() <= 3:
            m.bad_edges.append(edge)
            m.fail = 3
        h.delete_edge(edge)
    if m.fail == -1:
        m.fail = 0
    return m


class IsBaseGraphDetail:
    u_neighbors: set
    v_neighbors: set
    u: int
    v: int

    def __init__(self, u_neighbors, v_neighbors, u, v):
        self.u_neighbors = u_neighbors;
        self.v_neighbors = v_neighbors;
        self.u = u
        self.v = v


def is_base_graph(g: sage.graphs.graph.Graph) -> bool:
    """
    Checks if a graph is a base graph i.e. no adjacent vertices share the same set of neighbors excluding themselves
    :param g: Input graph
    :return: Boolean value for whether `g` is a base graph or not
    """
    g_vertices = g.vertices()
    g_vertices_count = len(g_vertices)
    for u in range(0, g_vertices_count):
        u_v = g_vertices[u]
        for v in range(u + 1, g_vertices_count):
            v_v = g_vertices[v]
            u_n = g.neighbors(u_v)  # might be worth it to move to outer part of loop
            v_n = g.neighbors(v_v)
            if v_v in u_n:
                u_n.remove(v_v)
            if u_v in v_n:
                v_n.remove(u_v)
            u_n = set(u_n)
            v_n = set(v_n)
            if u_n == v_n:
                return false
    return True


def is_base_graph_detail(g: sage.graphs.graph.Graph) -> [IsBaseGraphDetail]:
    """
    Checks if a graph is a base graph i.e. no adjacent vertices share the same set of neighbors excluding themselves
    :param g: Input graph
    :return: List of duplicated vertices and their neighbors
    """
    ret = []
    g_vertices = g.vertices()
    g_vertices_count = len(g_vertices)
    for u in range(0, g_vertices_count):
        u_v = g_vertices[u]
        for v in range(u + 1, g_vertices_count):
            v_v = g_vertices[v]
            u_n = g.neighbors(u_v)  # might be worth it to move to outer part of loop
            v_n = g.neighbors(v_v)
            if v_v in u_n:
                u_n.remove(v_v)
            if u_v in v_n:
                v_n.remove(u_v)
            u_n = set(u_n)
            v_n = set(v_n)
            if u_n == v_n:
                ibgd = IsBaseGraphDetail(u_n, v_n, u_v, u_v)
                ret.append(ibgd)
    return ret


def is_generated_graph(g: sage.graphs.graph.Graph, n: int = 1) -> bool:
    for h in g.connected_subgraph_iterator():
        if len(h.vertices()) == len(g.vertices()) - n:
            if h.is_minimal_prime_graph():
                return True;
    return False;


def duplicate_vertex(g: sage.graphs.graph.Graph, v) -> sage.graphs.graph.Graph:
    """
    Given a graph `g` and vertex `v` returns the graph constructed by duplicating the vertex `v`
    `v` must be a valid vertex in `g`
    `g` should have vertices labeled by integers starting at 0
    The new vertex from the duplication is labeled by `len(h.vertices())`
    :param g: Input graph
    :param v: Vertex to duplicate
    :return: Graph after vertex duplication
    """
    h = g.copy()
    u = len(h.vertices())
    h.add_vertex(u)
    # print(h.neighbors((v)))
    for x in h.neighbors(v):
        h.add_edge(u, x)
    h.add_edge(v, u)
    return h


# Add methods to sage.graphs.graph.Graph

sage.graphs.graph.Graph.is_prime_graph = is_prime_graph
sage.graphs.graph.Graph.is_minimal_prime_graph = is_minimal_prime_graph
sage.graphs.graph.Graph.is_minimal_prime_graph_detail = is_minimal_prime_graph_detail
sage.graphs.graph.Graph.is_base_graph = is_base_graph
sage.graphs.graph.Graph.duplicate_vertex = duplicate_vertex
sage.graphs.graph.Graph.is_generated_graph = is_generated_graph
