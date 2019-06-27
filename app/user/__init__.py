# user目录：针对用户业务逻辑处理的目录
# 针对用户业务逻辑处理的初始化行为
from flask import Blueprint
# 蓝图的声明
user = Blueprint('user', __name__)
from . import views
