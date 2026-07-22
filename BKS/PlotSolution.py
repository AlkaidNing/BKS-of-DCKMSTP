import os
import re
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def parse_filename(filename):
    basename = os.path.splitext(os.path.basename(filename))[0]
    match = re.match(r'^(.+)-(\d+)-(\d+)-([\d.]+)$', basename)
    if match:
        return match.group(1), int(match.group(2)), int(match.group(3)), float(match.group(4))
    return None, None, None, None


def validate_dc_k_mst(edges, k, d):
    selected_nodes = set()
    for u, v, _ in edges:
        selected_nodes.add(u)
        selected_nodes.add(v)

    degrees = {}
    for u, v, _ in edges:
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1

    num_nodes = len(selected_nodes)
    num_edges = len(edges)
    valid = (num_nodes == k and num_edges == k - 1
             and all(1 <= deg <= d for deg in degrees.values()))

    return valid, num_nodes, num_edges, degrees


def main():
    filename = "ch150.tsp-50-2-1676.52.txt"

    if not os.path.exists(filename):
        return

    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return

    try:
        n = int(lines[0])
    except ValueError:
        return

    coords = {}
    idx = 1
    for i in range(n):
        parts = lines[idx].split()
        coords[parts[0]] = (float(parts[1]), float(parts[2]))
        idx += 1

    edges = []
    total_length = 0.0
    while idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 3:
            edges.append((parts[0], parts[1], float(parts[2])))
            total_length += float(parts[2])
        idx += 1

    inst, k, d, value = parse_filename(filename)
    if k and d:
        ok, num_n, num_e, degrees = validate_dc_k_mst(edges, k, d)
        print(f"Instance: {inst}  k={k}  d={d}  value: {total_length:.2f}")
        print(f"  vertex number: {num_n} {'==' if num_n == k else '!='} {k} (k)")
        print(f"  edges number:   {num_e} {'==' if num_e == k-1 else '!='} {k-1} (k-1)")
        print(f"  degree constraint: {'YES' if all(v <= d for v in degrees.values()) else 'NO'} (d={d})")
        print(f"  connectivity: {'YES' if num_e == num_n - 1 else 'NO'}")
        print(f" {'✓ Valid Solution' if ok else '✗ Invalid Solution'}")

    G = nx.Graph()
    for node, pos in coords.items():
        G.add_node(node, pos=pos)
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = nx.get_node_attributes(G, 'pos')

    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)

    nx.draw(
        G, pos, ax=ax,
        with_labels=True,
        node_color='black',
        edgecolors='black',
        linewidths=1,
        edge_color='black',
        node_size=20,
        font_size=0
    )
    base_name = os.path.splitext(os.path.basename(filename))[0]
    ax.set_title(f"{base_name}  {total_length:.2f}")
    plt.show()

if __name__ == "__main__":
    main()