# OSM Tools

Tools for OpenStreetMap editing.

All of them made with virtual environment. Preparing:
```bash
. venv/bin/activate
pip install -r requirements.txt
```

## get-names-from-wikidata.py

Enrich `name:*` tags with Wikidata.

### How to use

1. Download desired data with JOSM (Overpass API recommended)
2. Save downloaded data as file
3. Delete data layer
4. Enrich data:
```bash
python get-names-from-wikidata.py -i source.osm -o destination.osm
```
5. Open new file `destination.osm` in JOSM
6. Filter out non-modified items
7. Thoroughly check all modified items for errors and fix them
8. If no errors remains, upload your changes to OSM or use them by desired way

