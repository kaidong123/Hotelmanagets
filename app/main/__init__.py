# main 目录：包含主要的业务逻辑的路由和视图
# __init__.py 对主业务逻辑程序的初始化操作
# Blueprint 蓝图
from flask import Blueprint

# 蓝图的声明
main = Blueprint('main', __name__)
from . import views
