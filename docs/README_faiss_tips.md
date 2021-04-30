
```python
# Show params
print("N:", index.ntotal)
print("D:", index.d)
print("Is trained:", index.is_trained)

# Remove ids from the index, larger ids will be shifted above
index.remove_ids(np.array([0,1,2]))

# Get the vector representation by its id
_id = 123
index.reconstruct(_id)
```
