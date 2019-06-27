# 与当前项目相关的模型文件，即所有的实体类在此编写
from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telphone = db.Column(db.String(50), nullable=False)


# class User_information(db.Model):
# 	__tablename__ = "user_information"
# 	id = db.Column(db.Integer, primary_key=True)
# 	customerName = db.Column(db.String(50), nullable=False)
# 	age = db.Column(db.String(20), nullable=False)
# 	sex = db.Column(db.String(20), nullable=False)
# 	idcard = db.Column(db.String(30), nullable=False)
# 	address = db.Column(db.String(50), nullable=False)
# 	nativeplace = db.Column(db.String(30), nullable=False)
# 	roomHobby = db.Column(db.String(50))
# 	referrer = db.Column(db.String(50))
class User_information(db.Model):
    __tablename__ = "user_information"
    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    idcardtype = db.Column(db.String(20), nullable=True)
    idcard = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    nativeplace = db.Column(db.String(30), nullable=False)
    roomHobby = db.Column(db.String(50))
    referrer = db.Column(db.String(50))

    def to_dict(self):
        dic = {
            "id": self.id,
            "customerName": self.customerName,
            "age": self.age,
            "sex": self.sex,
            "phone": self.phone,
            "idcardtype": self.idcardtype,
            "idcard": self.idcard,
            "address": self.address,
            "nativeplace": self.nativeplace,
            "roomHobby": self.roomHobby,
            "referrer": self.referrer,
        }
        return dic


class Room_type(db.Model):
    __tablename__ = "room_types"
    roomNumber = db.Column(db.String(50), primary_key=True)
    code = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float, nullable=True)
    floor = db.Column(db.String(20), nullable=True)
    id = db.Column(db.Integer, nullable=False)
    roomtype = db.Column(db.String(20), nullable=True)
    day_price = db.Column(db.Float, nullable=True)
    month_price = db.Column(db.Float, nullable=True)
    timer_price = db.Column(db.Float, nullable=True)
    # 备注
    comment = db.Column(db.String(255), nullable=True)


class Selfroom_status(db.Model):
    __tablename__ = "selfroom_status"
    id = db.Column(db.Integer, nullable=False)
    room_status = db.Column(db.String(50), primary_key=True)
    room_color = db.Column(db.String(30), nullable=True)

    def to_dict(self):
        dic = {
            "id": self.id,
            "room_status": self.room_status,
            "room_color": self.room_color
        }
        return dic


class Room_change(db.Model):
    __tablename__ = 'room_change'
    id = db.Column(db.Integer, primary_key=True)
    roomtype = db.Column(db.String(50), nullable=True)
    roomName = db.Column(db.String(50), nullable=True)
    roomcolor = db.Column(db.String(50), nullable=True)
    roomchangedcolor = db.Column(db.String(50), nullable=True)
    room_status = db.Column(db.String(50), nullable=True)
    # 操作员
    operator = db.Column(db.String(50), nullable=True)
    # 行为
    behavior = db.Column(db.String(200), nullable=True)
    changetime = db.Column(db.DateTime, nullable=False)


class Order_information(db.Model):
    __tablename__ = 'order_information'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.String(50), nullable=True)
    card_number = db.Column(db.String(50), nullable=True)
    customerName = db.Column(db.String(50), nullable=True)
    roomtype = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=True)
    createDate = db.Column(db.DateTime, nullable=True)
    showDate = db.Column(db.DateTime, nullable=True)
    beginDate = db.Column(db.DateTime, nullable=True)
    endDate = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    fwName = db.Column(db.String(30), nullable=True)
    assure = db.Column(db.String(30), nullable=True)
    comment = db.Column(db.String(100), nullable=True)


class Room_price(db.Model):
    __tablename__ = "room_price"
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    roomtype = db.Column(db.String(20), nullable=True)
    dayrent = db.Column(db.String(20), nullable=True)
    monthrent = db.Column(db.String(20), nullable=True)
    timeout = db.Column(db.String(20), nullable=True)



class Roomtype_info(db.Model):
    __tablename__ = "roomtype_info"
    id = db.Column(db.Integer, nullable=False,primary_key=True)
    code = db.Column(db.String(20), nullable=True)
    roomtype = db.Column(db.String(20), nullable=True)
    excess_number = db.Column(db.Integer,nullable=True)