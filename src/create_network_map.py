
import osmnx as ox
from pathlib import Path

graph_path = Path("data/raw/delhi_walk_network.graphml")
output_dir = Path("outputs/maps")
output_dir.mkdir(parents=True, exist_ok=True)

G = ox.load_graphml(graph_path)

fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_color="#2563eb",
    edge_linewidth=0.6,
    bgcolor="white",
    show=False,
    close=False,
)

output_path = output_dir / "walking_network.png"
fig.savefig(output_path, dpi=300, bbox_inches="tight")

print("Network map saved to:", output_path)
