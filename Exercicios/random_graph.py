import networkx as nx
import matplotlib.pyplot as plt
import random

def connected(graph):
    return True if len(list(nx.connected_components(graph))) == 1 else False


def create_random_graph(vertices):
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1, vertices + 1)])
    edges = []

    while not connected(G):
        n1 = random.randint(1, vertices)
        n2 = random.randint(1, vertices)
        edge = (n1, n2)
        if edge not in edges and n1 != n2:
            G.add_edge(n1, n2)
            edges.append((n1, n2))

    
    print(f"Edges created: {len(edges)}") 
    return (len(edges), G)


def test_random_graph(vertices, config):
    out = [create_random_graph(vertices) for _ in range(config)]
    colors = ['blue', 'black', 'red', 'pink', 'green', 'orange', 'purple', 'yellow']
    edges = []
    graphs = []
    for edge_num, graph in out:
        graphs.append(graph)
        edges.append(edge_num)

    i = 1
    edge_av = sum(edges) / len(edges)
    plt.figure(figsize=(22,13))
    plt.axis("off")
    plt.title(f"{vertices} Nodes (Average edges created: {edge_av:.3f})")
    for graph in graphs:
        options = {
            'node_color': colors[i % (len(colors))],
            'node_size': 80,
            'width': 3,
        }
        sub = plt.subplot(5, 6, i)
        nx.draw(graph, **options)
        i += 1

    plt.show()

    plt.figure()
    x_axis = [i for i in range(1, 31)]

    plt.plot(x_axis, edges)
    plt.title('Edges created per graph')
    plt.xlabel('Graph')
    plt.ylabel('Edges')

    plt.show()

    return edge_av

def test_range_of_graphs(start, end, config):
    x_ax = []
    y_ax = []

    for i in range(start, end):
        x_ax.append(i)
        y_ax.append(test_random_graph(i, config))

    plt.show()
    plt.figure()
    plt.plot(x_ax, y_ax)
    plt.title(f'Average nmr of edges per nmr of nodes ({config})')
    plt.xlabel('Number of edges')
    plt.ylabel('Number of nodes')
    plt.show()

test_range_of_graphs(2, 31, 30)


