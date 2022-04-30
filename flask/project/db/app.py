from datetime import datetime
from typing import Any, Callable, Dict, NoReturn, Union

import pytz
from flask import Flask, abort, redirect, request
from forms import GroupForm, Page, UserForm
from models import Group, User, UserGroup, to_dict
from sqlalchemy.exc import IntegrityError
from werkzeug import Response

from db import db
from db import init_app as init_app_db
from db import transaction
from utils import (Assets, HttpMethodOverrideMiddleware, templated,
                   watch_files_for_develop)

# 创建 Flask 对象
app = Flask(__name__, template_folder="templates", static_folder="static")
# 对 http 请求方法进行覆盖操作
app.wsgi_app = HttpMethodOverrideMiddleware(app.wsgi_app)
# 在 jinja 中注册 assets 对象
app.jinja_env.globals["assets"] = Assets(app)


def tz() -> Callable[[datetime], datetime]:
    """
    返回一个函数，用于将日期时间对象从 UTC（默认）时区转换到东八区
    """
    zone = pytz.timezone(app.config.get("TIME_ZONE", "Asia/Shanghai"))

    def time_zone(time: datetime):
        """
        进行时区转换
        """
        return time.replace(tzinfo=pytz.UTC).astimezone(zone)

    return time_zone


# 在 jinja 中注册 tz 函数
app.jinja_env.globals["tz"] = tz()
# 读取配置文件
app.config.from_pyfile("conf.py")

# 初始化数据库配置
init_app_db(app)


page = Page(app)


@app.route("/", methods=["GET"])
@templated()
def index() -> Dict[str, Any]:
    users = User.find_all(page)
    user_ids = [u.id for u in users.items]
    user_groups = {
        ug.user_id: ug.group.name for ug in UserGroup.find_by_users_with_group(user_ids)}
    return dict(users=users.items, page=dict(page_index=users.page, page_count=users.pages), user_groups=user_groups)


@app.route("/", methods=["POST"])
@templated("user.html")
@transaction()
def create_user() -> Union[Dict[str, Any], Response]:
    """
    创建一个用户
    """
    form = UserForm(request.form)
    groups_ = Group.find_all()
    form.group.choices = [(g.id, g.name) for g in groups_]
    if not form.validate():
        return dict(form=form), 400

    # 创建一个 User 实体
    user = User(
        id_num=form.id_num.data,
        name=form.name.data,
        gender=form.gender.data,
        birthday=form.birthday.data,
    )

    try:
        user.create()
        group_ = next(filter(lambda g: g.id == form.group.data, groups_))
        UserGroup(user=user, group=group_).create()
        return redirect("/")
    except IntegrityError as err:
        if err.orig.args[0] != 1062:
            raise

        form.id_num.errors = [
            f"\"{form.id_num.data}\" already exist, try other id num",
        ]
        db.session.rollback()
        return dict(form=form)


@app.route("/new", methods=["GET"])
@templated("user.html")
def new_user() -> Dict[str, Any]:
    """
    创建用户信息，获取表单页面
    """
    form = UserForm()
    form.group.choices = [
        (g.id, g.name) for g in Group.find_all()
    ]
    return dict(form=form)


@app.route("/<int:id_>/edit", methods=["GET"])
@templated("user.html")
def edit_user(id_: int) -> Union[Dict[str, Any], NoReturn]:
    """
    编辑用户信息，获取表单页面
    """
    user = User.find_by_id(id_)
    if not user:
        return abort(404)

    form = UserForm(data=to_dict(user))
    form.group.choices = list(map(lambda g: (g.id, g.name), Group.find_all()))
    return dict(id=id_, form=form)


@app.route("/<int:id_>", methods=["PUT"])
@templated("user.html")
@transaction()
def update_user(id_: int) -> Union[Dict[str, Any], Response, NoReturn]:
    """
    更新用户信息
    """
    user = User.find_by_id(id_)
    if not user:
        return abort(404)

    form = UserForm(request.form)
    groups_ = Group.find_all()
    form.group.choices = [(g.id, g.name) for g in groups_]

    if not form.validate():
        return dict(form=form)

    try:
        user.update(
            id_num=form.id_num.data,
            name=form.name.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
        )

        UserGroup.delete_by_user(user)

        group_ = next(filter(lambda g: g.id == form.group.data, groups_))
        UserGroup(user=user, group=group_).create()

        return redirect("/")
    except IntegrityError as err:
        if err.orig.args[0] != 1062:
            raise

        form.id_num.errors = [
            f"\"{form.id_num.data}\" already exist, try other id num",
        ]

        db.session.rollback()
        return dict(form=form)


@app.route("/<int:id_>", methods=["DELETE"])
@templated()
@transaction()
def delete_user(id_: int) -> Union[Response, NoReturn]:
    """
    删除用户
    """
    user = User.find_by_id(id_)
    if not user:
        return abort(404)

    UserGroup.delete_by_user(user)
    user.delete()

    return redirect("/")


@app.route("/groups", methods=["GET"])
@templated("group.html")
def groups() -> Dict[str, Any]:
    """
    获取组列表
    """
    return dict(
        back_url=request.args.get("__back", "/"),
        groups=Group.find_all(),
        form=GroupForm(),
    )


@app.route("/groups", methods=["POST"])
@templated("group.html")
@transaction()
def create_group() -> Union[Dict[str, Any], Response]:
    """
    创建用户组
    """
    back_url = request.args.get("__back", "/")
    form = GroupForm(request.form)
    if not form.validate():
        return dict(back_url=back_url, groups=Group.find_all(), form=form), 400

    group_ = Group(name=form.name.data)
    try:
        group_.create()
        return redirect("/groups?__back={}".format(back_url))
    except IntegrityError as err:
        if err.orig.args[0] != 1062:
            raise

        form.name.errors = [
            f"\"{form.name.data}\" already exist, try other name"
        ]
        db.session.rollback()

        return dict(
            back_url=back_url,
            groups=Group.find_all(),
            form=form,
        )


@app.route("/groups/<int:id_>", methods=["DELETE"])
@transaction()
def group_delete(id_) -> Union[Response, NoReturn]:
    """
    删除组
    """
    group_ = Group.find_by_id(id_)
    if not group_:
        abort(404)

    group_.delete()
    return redirect("/groups?__back={}".format(request.args.get("__back")))


@app.route("/configs", methods=["GET"])
@templated()
def configs() -> Dict[str, Any]:
    """
    获取数据库配置
    """
    configs_ = [
        item for item in app.config.items()
        if item[0].startswith("SQLALCHEMY")
    ]
    return dict(configs=configs_)


if __name__ == "__main__":
    # 启动 flask 应用
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        extra_files=watch_files_for_develop(app),
    )
