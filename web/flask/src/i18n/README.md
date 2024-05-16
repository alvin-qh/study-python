# Flask 国际化

- [Flask 国际化](#flask-国际化)
  - [1. 初始化命令](#1-初始化命令)
  - [2. 使用 Babel](#2-使用-babel)
    - [2.1. Babel 配置](#21-babel-配置)
    - [2.2. Python 代码](#22-python-代码)
  - [3. 创建多语言文件](#3-创建多语言文件)

## 1. 初始化命令

1. 安装 `Flask-Babel`

    ```bash
    pip install Flask-Babel
    ```

2. 创建 `.mo` 语言文件:

    ```bash
    pybabel compile -d message
    ```

## 2. 使用 Babel

参见 Babel 主页 <https://pythonhosted.org/Flask-Babel>

### 2.1. Babel 配置

- 在当前目录下创建 `babel.cfg` 文件:

  ```conf
  [python: **.py]
  [jinja2: **/templates/**.html]
  extensions = jinja2.ext.autoescape, jinja2.ext.with_
  ```

- 在 Flask 配置文件 (`conf.py`) 中, 增加如下内容:

  ```conf
  BABEL_TRANSLATION_DIRECTORIES = 'message'
  BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'
  BABEL_DEFAULT_TIMEZONE = 'UTC'
  BABEL_SUPPORT_LOCALES = ['en', 'en_US', 'zh', 'zh_CN', 'zh_TW']
  ```

### 2.2. Python 代码

- 创建 `Babel` 对象

  ```python
  from flask_babel import Babel

  babel = Babel(app)
  ```

- 添加 Babel 事件处理函数

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

## 3. 创建多语言文件

在当前目录下执行如下命令:

- 创建 `.pot` 文件, 作为多语言模板文件

  ```bash
  pybabel extract -F babel.cfg -k lazy_gettext -o message/messages.pot .
  ```

- 基于 `.pot` 文件, 为各语言生成对应的 `.po` 文件, 作为翻译文件

  ```bash
  pybabel init -i message/messages.pot -d message -l en_US
  pybabel init -i message/messages.pot -d message -l zh_Hans_CN
  ```

- 如果 `.po` 文件已存在, 则可通过新生成的 `.pot` 文件对其进行更新:

  ```bash
  pybabel update -i message/messages.pot -d message
  ```

- 编辑每个 `.po` 文件, 增加对应语言的翻译

  ```po
  ...
  #: templates/index.html:26
  msgid "Spring Goeth All in White"
  msgstr "春之女神着素装"

  #: templates/index.html:27
  msgid "Robert Bridges"
  msgstr "罗伯特·布里季"
  ...
  ```

- 编译 `.po` 文件, 生成 `.mo` 文件

  ```bash
  pybabel compile -d message
  ```
