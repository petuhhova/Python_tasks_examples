def get_digraph_from_edges(read_str):
    """Gets digraph as adjacency lists from list of edges,
    reading from a stream by read_str method
    first string consists of 2 numbers: number of vertexes and number of edges separated with ' '
    next m strings are edges like 'vertex1_id vertex2_id'
    Returns number of vertexes, number of edges and digraph
    """
    n,m=map(int,read_str().split())
    digraph={i:set() for i in range(n)}
    for _ in range(m):
        v,u=map(int,read_str().split())
        digraph[v].add(u)
    return digraph

def get_graph_from_edges(read_str,n=None,m=None):
    """Gets graph as adjacency lists from list of edges,
    n-number,m-number of edges
    reading from a stream by read_str method
    if n or m is None:
    read from first string 2 numbers:
    number of vertexes and number of edges separated with ' '
    next m strings are edges like 'vertex1_id vertex2_id'
    Returns graph
    """
    if m is None or n is None:
        n,m=map(int,read_str().split())
    graph={i:set() for i in range(n)}
    for _ in range(m):
        v1,v2=map(int,read_str().split())
        for u,v in (v1,v2),(v2,v1):
            graph[v].add(u)
    return graph

def get_weighted_graph(read_line,n=None,m=None):
    if m is None or n is None:
        n,m=map(int,read_line().split())
    graph={i:{} for i in range(n)}
    for _ in range(m):
        v1,v2,w=read_line().split()
        v1,v2=map(int,(v1,v2))
        w=float(w)
        for u,v in (v1,v2),(v2,v1):
            graph[v][u]=w
    return graph

def get_weighted_digraph(read_line,n=None,m=None):
    if m is None or n is None:
        n,m=map(int,read_line().split())
    graph={i:{} for i in range(n)}
    for _ in range(m):
        v,u,w=read_line().split()
        v,u=map(int,(v,u))
        w=float(w)
        graph[v][u]=w
    return graph
