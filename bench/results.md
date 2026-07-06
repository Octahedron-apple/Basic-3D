# Benchmark Results

Performance profiling comparing 3D projection, depth sorting, and topological calculation time vs. actual Pygame graphics drawing time. Run on a headless configuration.

| Scene / Workload | Math & Sort Calc (ms) | Pygame Draw Call (ms) | Total Frame (ms) | Avg FPS | 10% Low FPS | 1% Low FPS |
| --- | --- | --- | --- | --- | --- | --- |
| UV Sphere (Faces + Edges + Nodes) | 2.964 | 5.779 | 8.744 | 114.4 | 84.3 | 82.8 |
| 3D Text Engine (Faces + Edges) | 3.918 | 5.480 | 9.398 | 106.4 | 105.3 | 94.1 |
| Solar System Mock (Orbits + 800 Nodes) | 4.936 | 2.364 | 7.299 | 137.0 | 132.6 | 124.0 |
| Penguin Showcase (penger.py Mock) | 6.414 | 10.371 | 16.785 | 59.6 | 58.8 | 56.3 |
| Character Test (test_chars.py - Demo Testing) | 4.536 | 7.095 | 11.632 | 86.0 | 84.0 | 81.2 |
| Font Generation Atlas (fontgen) | 12.614 | 0.000 | 12.614 | 79.3 | 79.3 | 79.3 |
