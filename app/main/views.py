# 主业务逻辑中的视图和路由的定义
from flask import render_template, request, session, redirect, make_response, json
# 导入蓝图程序，用于构建路由
from . import main
# 导入db，用于操作数据库
from .. import db
# 导入实体类，用于操作数据库
from ..models import *
import datetime


# 主页的访问路径
@main.route('/')
def main_index():
    # 获取登录信息
    if 'uid' in session and 'uname' in session:
        user = User.query.filter_by(id=session.get('uid')).first()
    return render_template("index.html", params=locals())


# 登录页面的访问路径
@main.route('/login', methods=['GET', 'POST'])
def login_views():
    if request.method == "GET":
        # 判断cookies中是否有username
        if 'uname' in request.cookies:
            username = request.cookies['uname']
            # 判断uname的值是否为admin
            user = User.query.filter_by(username=username).first()
            if user:
                return redirect('/')
        return render_template("login.html")
    else:
        # 接受前端传递过来的数据
        username = request.form.get('username')
        # print(type(username), username)
        password = request.form.get('password')
        # 使用接受的用户名和密码到数据库中查询
        user = User.query.filter_by(username=username, password=password).first()
        room_change = Room_change()
        room_change.behavior = username
        room_change.operator = "登录酒店管理系统"
        room_change.changetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(room_change)
        db.session.commit()
        # 如果用户存在，将信息保存进session并重定向回首页，否则重定向登陆页
        if user:
            resp = redirect('/')
            # resp = make_response("保存cookies成功")
            resp.set_cookie("uname", username, 60 * 60 * 24 * 365)
            resp.set_cookie("upwd", password)
            session['uid'] = user.id
            session['uname'] = user.username
            return resp
        else:
            errMsg = "用户名或密码不正确"
            return render_template('login.html', errMsg=errMsg)


# 注册页面的访问路径
@main.route('/register', methods=['GET', 'POST'])
def register_views():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # 获取文本框的值并赋值给user实体对象
        user = User()
        user.username = request.form['loginname']
        user.password = request.form['upwd']
        user.email = request.form['uemail']
        user.telphone = request.form['utel']
        # 将数据保存进数据库   --注册
        db.session.add(user)
        # 手动提交，目的是为了获取提交后的user的id
        db.session.commit()
        # 当user成功插入数据库之后，程序会自动将所有信息取出来再赋值给user
        # 完成登录的行为操作
        session['uid'] = user.id
        session['uname'] = user.username
        return redirect('/')


@main.route('/03-checkuname')
def check_uname():
    username = request.args['loginname']
    user = User.query.filter_by(username=username).first()
    if user:
        # 返回1表示用户名称已存在
        return "1"
    else:
        # 返回0表示通过
        return "0"


# 退出的访问路径
@main.route('/logout')
def logout_views():
    if 'uid' in session and 'uname' in session:
        del session['uid']
        del session['uname']
    uname = request.cookies['uname']
    upwd = request.cookies['upwd']
    resp = redirect('/login')
    if uname:
        resp.delete_cookie('uname')
    if upwd:
        resp.delete_cookie('upwd')
    return resp


# system set 系统设置 房态管理
@main.route('/system_set')
def system_set_views():
    colors = Selfroom_status.query.all()
    # print(colors)
    return render_template("6.html", params=locals())


@main.route('/save_color')
def save_color():
    room_status = request.args['room_status']
    room_color = request.args['room_color']
    status = db.session.query(Selfroom_status).filter_by(room_status=room_status).first()
    status.room_color = room_color
    db.session.add(status)
    db.session.commit()
    return json.dumps(room_status)


# 楼层管理
@main.route('/system_set1')
def system_set_views1():
    floors = Room_type.query.group_by('floor').order_by("floor").all()
    # print(locals())
    return render_template("6.1.html", params=locals())


# 获取数据库楼层房间到模板
@main.route('/getrooms')
def getrooms_by_floor():
    floor = request.args['floor'][0:-1]
    # print(floor)
    rooms = Room_type.query.filter_by(floor=floor).all()
    list = []
    for i in rooms:
        list.append(i.to_dict())
    # print(json.dumps(list))
    return json.dumps(list)


# 删除楼层房间
@main.route("/deleteroom")
def deleteroom():
    roomNumber = request.args['roomNumber']
    room = Room_type.query.filter_by(roomNumber=roomNumber).first()
    db.session.delete(room)
    db.session.commit()
    # print(roomNumber)
    return json.dumps(roomNumber)


# 添加楼层房间到数据库
@main.route("/addroom")
def addroom():
    room = Room_type()
    room.roomNumber = request.args['roomNumber']
    room.roomtype = request.args['roomtype']
    room.comment = request.args['comment']
    room.floor = request.args['floor'][0:-1]
    room.id = request.args['id']
    db.session.add(room)
    db.session.commit()
    return json.dumps(request.args['roomNumber'])


# 修改房间信息
@main.route("/updateroom")
def updata_room():
    roomNumber1 = request.args['roomNumber1']
    room = Room_type.query.filter_by(roomNumber=roomNumber1).first()
    room.roomNumber = request.args['roomNumber2']
    room.roomtype = request.args['roomtype']
    room.comment = request.args['comment']
    try:
        db.session.add(room)
        db.session.commit()
        return json.dumps("修改成功")
    except Exception as e:
        print(e)
        return json.dumps("修改失败！")


# 删除楼层所有房间
@main.route("/deletefloor")
def deletefloor():
    floor = request.args['floor'][0:-1]
    rooms = Room_type.query.filter_by(floor=floor).all()
    for i in rooms:
        db.session.delete(i)
        db.session.commit()
    return json.dumps("删除成功！")


# 房间类型
@main.route('/system_set2')
def system_set_views2():
    return render_template("6.2.html")


# 价格管理
@main.route('/system_set3')
def system_set_views3():
    return render_template("6.3.html")


# 操作管理 修改密码
@main.route('/operation_manager')
def operation_manager_views():
    return render_template("5.html")


# 操作管理 日志浏览
@main.route('/operation_manager1')
def operation_manager_views1():
    return render_template("5.1.html")


# 房态中心
@main.route('/room_center')
def room_center():
    roomnumber = db.session.query(Room_type, Selfroom_status).filter(Room_type.id == Selfroom_status.id).all()
    # roomnumber = db.session.query(Room_type.roomNumber).all()
    # count = db.session.query(Room_type.roomNumber).count()
    # print(roomnumber, type(roomnumber))
    # print(count)
    # for r in roomnumber:
    # 	print(r)
    selfroom_status = Selfroom_status.query.all()
    print(selfroom_status)
    # list = []
    # list.append(selfroom_status.to_dict())
    # print(list)
    return render_template('2.html', params=locals())


# 办理入住
@main.route('/check_in_room')
def check_in_roon():
    return render_template('cust_order.html')


# 公共函数，change房间业务并修改颜色
def change_room_count(id, room_status):
    get_color = Selfroom_status.query.filter_by(id=id).first()
    # print(get_color)
    list = []
    list.append(get_color.to_dict())
    # print(json.dumps(list))
    html = request.args['html'].strip()
    html1 = html[:4]
    html2 = html[4:]
    # id = request.args['id']
    color = request.args['color'].strip()
    style = request.args['style'].strip()
    # styles = style[11:18]
    # print(color, styles, style)
    room_change = Room_change()
    room_change.roomtype = html2
    room_change.roomName = html1
    room_change.roomcolor = style
    room_change.roomchangedcolor = color
    room_change.room_status = room_status
    room_change.operator = "CPT"
    room_change.behavior = "房间状态修改"
    room_change.changetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # change_id = Room_type.query().filter(Room_type.roomNumber == html1).first()
    change_id = db.session.query(Room_type).filter(Room_type.roomNumber == html1).first()
    # print(change_id)
    change_id.id = id
    try:
        db.session.add(room_change)
        db.session.add(change_id)
        db.session.commit()
    except Exception as ex:
        print(ex)
    return json.dumps(list)


# 转为脏房并修改div颜色
@main.route('/change_room_gray')
def change_room_color1():
    # get_color = Selfroom_status.query.filter_by(id=5).first()
    # # print(get_color)
    # list = []
    # list.append(get_color.to_dict())
    # # print(json.dumps(list))
    # html = request.args['html'].strip()
    # html1 = html[:4]
    # html2 = html[4:]
    # # id = request.args['id']
    # color = request.args['color'].strip()
    # style = request.args['style'].strip()
    # # print(html1, html2, color, style)
    # room_change = Room_change()
    # room_change.roomtype = html2
    # room_change.roomName = html1
    # room_change.roomcolor = style
    # room_change.roomchangedcolor = color
    # room_change.room_status = "脏房"
    # room_change.changetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # # change_id = Room_type.query().filter(Room_type.roomNumber == html1).first()
    # change_id = db.session.query(Room_type).filter(Room_type.roomNumber == html1).first()
    # # print(change_id)
    # change_id.id = 5
    # try:
    # 	db.session.add(room_change)
    # 	db.session.add(change_id)
    # 	db.session.commit()
    # except Exception as ex:
    # 	print(ex)
    # return json.dumps(list)
    return change_room_count(5, "脏房")


# 转为维修房并修改div颜色
@main.route('/change_room_green')
def change_room_color2():
    # get_color = Selfroom_status.query.filter_by(id=4).first()
    # # print(get_color)
    # list = []
    # list.append(get_color.to_dict())
    # # print(json.dumps(list))
    # return json.dumps(list)
    return change_room_count(4, "维修房")


# 转为清洁未检查并修改div颜色紫色
@main.route('/change_room_violet')
def change_room_color3():
    # get_color = Selfroom_status.query.filter_by(id=6).first()
    # # print(get_color)
    # list = []
    # list.append(get_color.to_dict())
    # # print(json.dumps(list))
    # return json.dumps(list)
    return change_room_count(6, "清洁为检查")


# 转为转停用房并修改div颜色红色
@main.route('/change_room_red')
def change_room_color4():
    # get_color = Selfroom_status.query.filter_by(id=1).first()
    # # print(get_color)
    # list = []
    # list.append(get_color.to_dict())
    # # print(json.dumps(list))
    # return json.dumps(list)
    return change_room_count(1, "停用房")


# 转为清洁检查房并修改div颜色蓝色
@main.route('/change_room_blue')
def change_room_color5():
    # get_color = Selfroom_status.query.filter_by(id=3).first()
    # # print(get_color)
    # list = []
    # list.append(get_color.to_dict())
    # # print(json.dumps(list))
    # return json.dumps(list)
    return change_room_count(3, "清洁检查房")


# 返回客户预订页面
@main.route('/Customers_booking')
def Customers_booking():
    # room_type = request.args['room_type']
    # print(room_type)
    return render_template("hotelyuding.html")


# 客户预订业务处理
@main.route('/business_process', methods=['POST'])
def business_process():
    channel = request.form['channel']
    card_number = request.form['card_number']
    roomtype = request.form['rotype']
    roomnumber = request.form['roomnumber']
    fwName = request.form['rnum']
    showDate = request.form['showDate']
    if showDate == "":
        showDate = datetime.datetime.now()
    beginDate = request.form['beginDate']
    if beginDate == "":
        beginDate = datetime.datetime.now()
    endDate = request.form['endDate']
    if endDate == "":
        endDate = datetime.datetime.now()
    customerName = request.form['username']
    phone = request.form['phonnumbe']
    assure = request.form['guarantee']
    comment = request.form['comment']
    # print(channel, card_number, roomtype, roomnumber, fwName, showDate, beginDate, endDate, customerName, phone, assure,
    # 	  comment)
    order_infor = Order_information()
    order_infor.channel = channel
    order_infor.card_number = card_number
    order_infor.customerName = customerName
    order_infor.roomtype = roomtype
    order_infor.number = roomnumber
    order_infor.showDate = showDate
    order_infor.beginDate = beginDate
    order_infor.endDate = endDate
    order_infor.phone = phone
    order_infor.fwName = fwName
    order_infor.assure = assure
    order_infor.comment = comment
    order_infor.createDate = datetime.datetime.now()
    try:
        db.session.add(order_infor)
        db.session.commit()
    except Exception as ex:
        print(ex)

    return redirect('/room_center')


# 客户管理 在住客人
@main.route('/customer_in')
def customer_in_views():
    return render_template("zaizhu.html")


# 客户管理 在住客人业务处理逻辑
@main.route('/customer_select')
def customer_select():
    name = request.args['user']
    card = request.args['card']
    phone = request.args['phone']
    list = []
    # print(name,card,phone)
    if name and card and phone:
        info = User_information.query.filter_by(customerName=name).filter_by(idcard=card).filter_by(phone=phone).all()
        # print(info)
        # print(info.to_dict())
        for i in info:
            # print(i)
            list.append(i.to_dict())
    # info_dict = info.to_dict()
    # print(info_dict, type(info_dict))
    j_info = json.dumps(list)
    print(j_info)
    # print(list)
    # return "11"
    return j_info


# 客户管理 历史客人
@main.route('/customer_history')
def customer_history_views1():
    return render_template("lishi.html")


# 客户管理 在住客人业务处理逻辑
@main.route('/customer_select')
def customer_select():
    name = request.args['user']
    card = request.args['card']
    phone = request.args['phone']
    list = []
    # print(name,card,phone)
    if name == "" and card == "" and phone == "":
        info = db.session.query(User_information, Order_room).filter(
            Order_room.customerName == User_information.customerName).filter(
            db.cast(Order_room.beginDate, db.Date) == db.cast(datetime.datetime.now(), db.Date)).all()
        print(info)
        for i in info:
            print(i)
            for o in i:
                # print(i.to_dict())
                list.append(o.to_dict())
        print(json.dumps(list))
        return json.dumps(list)

    if name and card and phone:
        # info = User_information.query.filter_by(customerName=name).filter_by(idcard=card).filter_by(phone=phone).all()
        info = db.session.query(User_information, Order_room).filter(
            User_information.customerName == Order_room.customerName).filter(
            User_information.customerName == name).filter(User_information.idcard == card).filter(
            User_information.phone == phone).filter(
            db.cast(Order_room.beginDate, db.Date) == db.cast(datetime.datetime.now(), db.Date)).first()
        print(info)
    # print(info)
    # print(info.to_dict())
    for i in info:
        print(i)
        # print(i.to_dict())
        list.append(i.to_dict())
    # info_dict = info.to_dict()
    # print(info_dict, type(info_dict))
    # print(json.dumps(list))
    print(list)
    return json.dumps(list)
