# Dependency-Aware Pipeline Runner & CI/CD Orchestrator

## Objectives
- Build a Python-based pipeline orchestration engine that models job dependencies using Directed Acyclic Graphs (DAGs).
- Implement Kahn's topological sorting algorithm to determine correct execution order.
- Integrate DFS-based cycle detection to prevent pipeline deadlocks.
- Handle job failures robustly with automated downstream skip propagation.

## Tools Used
- **Python 3**: Core orchestration logic, classes, and subprocess execution.
- **PyYAML**: Parsing declarative pipeline configuration files.
- **Graph Algorithms**: Kahn's Topological Sort and Depth-First Search (DFS) cycle validation.

## Key Skills Demonstrated
- **Pipeline Orchestration**: Designing custom CI/CD job runners with strict dependency enforcement.
- **Data Structures & Algorithms**: Applying graph theory and sorting algorithms to real-world infrastructure problems.
- **Fault Propagation**: Managing failure states and cascading skip actions across dependent tasks.
- **Declarative Configuration**: Translating YAML schemas into executable dependency trees.

## Troubleshooting Log
- **Issue**: Incorrect execution order when multiple independent jobs exist.
  - **Resolution**: Implemented in-degree counting with Kahn's algorithm (`deque`) to correctly process all nodes with zero incoming edges in parallelized order.
- **Issue**: Downstream tasks executing despite upstream failures.
  - **Resolution**: Created `mark_downstream_skipped()` utilizing BFS queue traversal over the dependency graph to propagate `SKIPPED` statuses instantly.
