# Flask Context Hook

## Hooks

### For `Flask` object

```python
from flask import Flask

app = Flask(...)
...

# Callback when first request coming
@app.before_first_request
def _before_first_request():
    pass

# Callback when every request coming
@app.before_request
def _before_request():
    pass

# Callback before every response send back
@app.after_request
def _after_request(response):
    pass

# Callback when one session complete
@app.teardown_request
def _teardown_request(exception):
    pass
```

### For `Blueprint` object

```python
from flask import Blueprint

bp = Blueprint(...)
...

# Just like @app.before_first_request
@bp.before_app_first_request()
def _before_app_first_request():
    pass

# Just like @app.before_request
@bp.before_app_request()
def _before_app_request():
    pass

# Just like @app.before_request,
# but only for current blueprint
@bp.before_request
def _before_request():
    pass

# Just like @app.after_request,
# but only for current blueprint
@bp.after_request
def _after_request(response):
    pass

# Just like @app.teardown_request,
# but only for current blueprint
@bp.teardown_request
def _teardown_request(exception):
    pass
```

### Without decorate

```python
from flask import Flask

app = Flask(...)
...

def _before_request():
    pass

app.before_request(_before_request)
```
