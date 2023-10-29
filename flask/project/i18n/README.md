# Flask Babel

## Setup project

1. Install Flask-Babel

    ```bash
    $ pip install Flask-Babel
    ```

2. Create `.mo` language files:

    ```bash
    $ pybabel compile -d message
    ```

## Setup Babel

> [Babel Home Page](https://pythonhosted.org/Flask-Babel/)

### Babel Config

- Create `babel.cfg` file at root of project directory:

```conf
[python: **.py]
[jinja2: **/templates/**.html]
extensions = jinja2.ext.autoescape, jinja2.ext.with_
```

- In flask config pyfile, add the following options:

```conf
BABEL_TRANSLATION_DIRECTORIES = 'message'
BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
BABEL_DEFAULT_TIMEZONE = 'UTC'
BABEL_SUPPORT_LOCALES = ['en', 'en_US', 'zh', 'zh_CN', 'zh_TW']
```

> config pyfile can load by app like this: `app.config.from_pyfile('conf.py')`

### Babel Setup

- Create babel object from Flask app object:

```python
from flask_babel import Babel

babel = Babel(app)
```

- Add babel events listener

```python
from flask import request, session

@babel.localeselector
def get_locale():
    lang = session.get('lang')
    if lang:
        return lang
    return request.accept_languages.best_match(app.config['BABEL_SUPPORT_LOCALES'], 'zh_CN')

@babel.timezoneselector
def get_timezone():
    zone = session.get('time_zone')
    if zone:
        return zone
    return 'UTC'
```

## Create translate files

**In project directory, run the following commands:**

- Create pot file, template of all other translate files

```bash
$ pybabel extract -F babel.cfg -k lazy_gettext -o message/messages.pot .
```

- Create po file for each language:

```bash
pybabel init -i message/messages.pot -d message -l en_US
pybabel init -i message/messages.pot -d message -l zh_Hans_CN
```

- Or update exist `.po` file:

```bash
$ pybabel update -i message/messages.pot -d message
```

- Edit each po file

```plain
...
#: templates/index.html:26
msgid "Spring Goeth All in White"
msgstr "春之女神着素装"

#: templates/index.html:27
msgid "Robert Bridges"
msgstr "罗伯特·布里季"
...
```

- Compile translate file to binary format:

```bash
$ pybabel compile -d message
```
