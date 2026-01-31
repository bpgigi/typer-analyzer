from typing import Dict, List, Any
import plotly.graph_objects as go
import json


class InteractiveCharts:
    def create_sankey_diagram(
        self,
        call_chains: List[Dict[str, str]],
        output_file: str = "33_call_chain_sankey.html",
    ):
        if not call_chains:
            return

        labels = []
        source_indices = []
        target_indices = []
        values = []

        label_map = {}

        for chain in call_chains:
            src = chain["source"]
            tgt = chain["target"]
            val = chain.get("value", 1)

            if src not in label_map:
                label_map[src] = len(labels)
                labels.append(src)
            if tgt not in label_map:
                label_map[tgt] = len(labels)
                labels.append(tgt)

            source_indices.append(label_map[src])
            target_indices.append(label_map[tgt])
            values.append(val)

        node_colors = [
            "#E85A4F",
            "#E98074",
            "#D8C3A5",
            "#8E8D8A",
            "#EAE7DC",
            "#F4A460",
            "#CD853F",
            "#DEB887",
        ] * (len(labels) // 8 + 1)

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=labels,
                        color=node_colors[: len(labels)],
                    ),
                    link=dict(
                        source=source_indices,
                        target=target_indices,
                        value=values,
                        color="rgba(232, 90, 79, 0.4)",
                    ),
                )
            ]
        )

        fig.update_layout(
            title_text="Function Call Chain Analysis",
            font_size=10,
            width=1000,
            height=800,
        )

        fig.write_html(output_file)

    def create_3d_scatter(
        self,
        data: List[Dict[str, Any]],
        output_file: str = "23_3d_commit_distribution.html",
    ):
        pass
