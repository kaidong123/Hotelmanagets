function createXhr() {
    if (window.XMLHttpRequest) {
        return new XMLHttpRequest();
    } else {
        return new ActiveXObject("Micorsoft.XMLHTTP");
    }
}

//用户名验证
function checkname() {
    var xhr = createXhr();
    var url = "/03-checkuname?loginname=" + $("#text1").val();
    xhr.open('get', url, true);
    var div = document.getElementById("div1");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            if (xhr.responseText == "1") {
                $("#div1").html("用户名已存在");
                return false;
            } else {
                div.innerHTML = "";
                var name1 = document.tijiao.text1.value;
                if (name1 == "") {
                    div.innerHTML = "用户名不能为空！";
                    document.tijiao.text1.focus();
                    return false;
                }
                if (name1.length < 4 || name1.length > 16) {
                    div.innerHTML = "长度4-16个字符";
                    document.tijiao.text1.select();
                    return false;
                }
                var charname1 = name1.toLowerCase();
                for (var i = 0; i < name1.length; i++) {
                    var charname = charname1.charAt(i);
                    if (!(charname >= 0 && charname <= 9) && (!(charname >= 'a' && charname <= 'z')) && (charname != '_')) {
                        div.innerHTML = "用户名包含非法字符";
                        document.form.tijiao.select();
                        return false;
                    }
                }
                $("#div1").html("通过").css("color","black");
            }

        }
    };
    xhr.send(null);
    return true;
}

//密码验证
function checkpassword() {
    var div = document.getElementById("div2");
    div.innerHTML = "";
    var password = document.tijiao.text2.value;
    if (password == "") {
        div.innerHTML = "密码不能为空";
        document.tijiao.text2.focus();
        return false;
    }
    if (password.length < 4 || password.length > 16) {
        div.innerHTML = "密码长度为4-16位";
        document.tijiao.text2.select();
        return false;
    }
    return true;
}

function checkrepassword() {
    var div = document.getElementById("div3");
    div.innerHTML = "";
    var password = document.tijiao.text2.value;
    var repass = document.tijiao.text3.value;
    if (repass == "") {
        div.innerHTML = "密码不能为空";
        document.tijiao.text3.focus();
        return false;
    }
    if (password != repass) {
        div.innerHTML = "密码不一致";
        document.tijiao.text3.select();
        return false;
    }
    return true;
}

//邮箱验证
function checkEmail() {
    var div = document.getElementById("div4");
    div.innerHTML = "";
    var email = document.tijiao.text5.value;
    var sw = email.indexOf("@", 0);
    var sw1 = email.indexOf(".", 0);
    var tt = sw1 - sw;
    if (email.length == 0) {
        div.innerHTML = "邮箱不能为空";
        document.tijiao.text5.focus();
        return false;
    }

    if (email.indexOf("@", 0) == -1) {
        div.innerHTML = "必须包含@符号";
        document.tijiao.text5.select();
        return false;
    }

    if (email.indexOf(".", 0) == -1) {
        div.innerHTML = "必须包含.符号";
        document.tijiao.text5.select();
        return false;
    }

    if (tt == 1) {
        div.innerHTML = "@和.不能一起";
        document.tijiao.text5.select();
        return false;
    }

    if (sw > sw1) {
        div.innerHTML = "@符号必须在.之前";
        document.tijiao.text5.select();
        return false;
    }
    else {
        return true;
    }
    return true;
}

function checkPhone() {
    var div = document.getElementById("div5");
    div.innerHTML = "";
    var phone = document.getElementById('phone1').value;
    if (!(/^1[34578]\d{9}$/.test(phone))) {
        // alert("手机号码有误，请重填");
        div.innerHTML = "手机号码有误，请重填";
        return false;
    }
    return true
}


function check() {
    if (checkname() && checkpassword() && checkrepassword() && checkEmail() && checkPhone()) {
        return true;
    }
    else {
        return false;
    }
}
