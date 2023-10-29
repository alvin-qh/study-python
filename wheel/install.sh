# 前置操作:
# 1. 退出 virtualenv
# 2. 删除 .venv 文件夹
# 3. 创建 virtualenv: python -m venv .venv --prompt=wheel

pip install --no-index --find-links=wheelhouse -r requirements.txt
