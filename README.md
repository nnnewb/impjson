# imp-json

Import JSON file directly in python!

## Quick start

> data.json
```json
{
  "attr": "value"
}
```

> program.py
```python
import impjson
import sys
sys.meta_path.append(impjson.JSONImporter())
import data  # import a json file just like import a python module!

assert data.attr == 'value'
```

## Contribution

Please open issue let me known what you want to do.

## License

Apache License 2.0
