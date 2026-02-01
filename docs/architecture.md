# System Architecture

## Directory Structure

- `analyzers/`: Core analysis logic (AST, Z3, LibCST, PySnooper).
- `collectors/`: Data ingestion modules (Git, GitHub).
- `visualizers/`: Chart generation logic.
- `utils/`: Shared utilities (Cache, FontConfig).
- `data/`: Intermediate storage for analysis results.
- `output/`: Final generated charts and reports.

## Design Patterns used

- **Visitor Pattern**: Used in AST and LibCST analysis for tree traversal.
- **Strategy Pattern**: Used in Visualizers to switch between chart types.
- **Singleton Pattern**: Applied to Cache management.
- **Factory Pattern**: Used for creating specific collector instances.

## Integration Points

The `main.py` entry point acts as the orchestrator:
1. Initializes configuration.
2. Instantiates collectors to fetch data.
3. Passes data to analyzers for processing.
4. Feeds analysis results to visualizers.
5. Generates the final report.
