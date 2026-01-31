from typing import List, Dict, Any, Set
from pathlib import Path
import ast
import networkx as nx
import json


class DependencyAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.graph = nx.DiGraph()
        self.imports: Dict[str, List[str]] = {}

    def analyze_imports(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content)

            relative_path = str(file_path.relative_to(self.repo_path)).replace(
                "\\", "/"
            )
            self.graph.add_node(relative_path, type="file")

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_dependency(relative_path, alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._add_dependency(relative_path, node.module)

        except Exception as e:
            print(f"Error analyzing imports in {file_path}: {e}")

    def _add_dependency(self, source: str, target: str):
        self.graph.add_node(target, type="module")
        self.graph.add_edge(source, target)
        if source not in self.imports:
            self.imports[source] = []
        self.imports[source].append(target)

    def export_graph_data(self, output_path: str):
        data = nx.node_link_data(self.graph)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "avg_degree": sum(dict(self.graph.degree()).values())
            / max(1, self.graph.number_of_nodes()),
        }
