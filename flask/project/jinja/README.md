# Jinja2

## Setup and run

1. Install `node.js` and `npm`
2. Run the following command:
    ```bash
    $ npm run setup
    $ npm run package:dev
    ```
3. Start flask app


## Template

### Keep or Remove white-space in template

Keep white space:

```jinja2
{% if a > b %}
	<div class="result">{{ a - b }}</div>
{% endif %}
```

Remove leading and tail white-space:

```jinja2
{%- if a > b %}
	<div class="result">{{ a - b }}</div>
{% endif -%}
```

Remove all white-space:

```jinja2
{%- if a > b -%}
	<div class="result">{{ a - b }}</div>
{%- endif -%}
```

### Change jinja variable delimiter

Jinja2 use `{{` and `}}` for expression delimiter, but some js framework also use this delimiter (for example: Vue), so either jinja2 or js framework need change expression delimiter

Change jinja2 delimiter:

```python
... # create flask app object

app.jinja_env.variable_start_string = '${'
app.jinja_env.variable_end_string = '}'
```

Change vue delimiter:

vue-entends.js

```javascript
import SrcVue from "vue";

export const Vue = SrcVue.extend({
    delimiters: ['${', '}']
});
```

use-vue.js

```javascript
import {Vue} from "vue-entends";

const vue = new Vue({
    ...
});
```

