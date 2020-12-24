# How to profile python script

### dependencies
```bash
pip install gprof2dot
sudo apt install graphviz
```

### profiling
```bash
python -m cProfile -o output_stats main.py
```

### visualization
```bash
gprof2dot -f pstats output_stats | dot -Tpng -o output.png
```
