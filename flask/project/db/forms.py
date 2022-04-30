from flask import Flask, request
from wtforms import (DateField, Form, RadioField, SelectField, StringField,
                     validators)


class Page:
    """
    用于分页的类
    """

    def __init__(self, app: Flask) -> None:
        # 从配置中获取默认的页大小
        self._default_page_size = app.config.get("PAGE_SIZE", 5)

    @property
    def page_index(self) -> int:
        """
        获取当前页下标
        """
        return request.args.get("p", 1, type=int)

    @property
    def page_size(self) -> int:
        """
        获取当前页大小
        """
        return request.args.get("ps", self._default_page_size, type=int)


class UserForm(Form):
    """
    用户信息表单
    """

    # 身份证号码
    id_num = StringField(
        label="Id Num",
        validators=[validators.data_required(message="ID Num required")],
    )

    # 用户名称
    name = StringField(
        label="Name",
        validators=[validators.data_required(message="name required")],
    )

    # 用户性别
    gender = RadioField(
        label="Gender",
        choices=[("M", "Male"), ("F", "Female")],
        default="M",
        coerce=str,
        validators=[
            validators.data_required(message="gender required"),
            validators.any_of(
                ["M", "F"],
                message="gender must be one of %(values)s",
            ),
        ],
    )

    # 用户的生日
    birthday = DateField(label="Birthday")

    # 用户所在的组
    group = SelectField(
        label="Group",
        coerce=int,
        validators=[validators.data_required(message="group required")],
    )


class GroupForm(Form):
    """
    用户组表单
    """

    # 组名称
    name = StringField(
        label="Name",
        validators=[
            validators.data_required(message="name required"),
            validators.length(
                min=2,
                max=10,
                message="name length must between %(min)s and %(max)s",
            ),
        ],
    )
