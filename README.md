# de.unikn.fillinger.vision

### config
```python
# [START config]
API_KEY = "<API_KEY>"
MAX_RESULTS = 10

API_URI= 'https://vision.googleapis.com/v1/images:annotate?key='
# [END config]
```

### usage
```bash
python main.py -i ./path/to/images -o ./path/to/result.csv
```

### result
```bash
collect images from ./data/right  /
analyze images |###                             | 1/10
create CSV file to ./test.csv \
```
