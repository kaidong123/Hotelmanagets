var div = document.getElementById('flash');
var img = div.getElementsByTagName('img');
/*选中div下所有的图片*/
var ul = document.getElementsByTagName('ul')[0];
var li = ul.getElementsByTagName('li');
var div_r = document.getElementById('left_span');
var div_l = document.getElementById('right_span');
var len = img.length;
var count = 0;

/*设置count来显示当前图片的序号*/
function run() { /*将定时器里的函数提取到外部*/
    count++;
    count = count == 5 ? 0 : count;
    /*当图片加载到最后一张时，使其归零*/
    for (var i = 0; i < len; i++) {
        img[i].style.display = 'none';
        /*利用for循环使除当前count位其他图片隐藏*/
    }
    img[count].style.display = 'block';
    /*显示当前count的值所代表的图片*/
    for (var i = 0; i < li.length; i++) {
        li[i].style.backgroundColor = "#fff";
        /*原理同上*/
    }
    li[count].style.backgroundColor = "#f40";
};
var timer = setInterval(run, 1500);
/*定义定时器，使图片每隔2s更换一次*/
div.onmouseover = function () {
    clearInterval(timer);
};
div.onmouseout = function () { /*定义鼠标移出事件，当鼠标移出div区域，轮播继续*/
    timer = setInterval(run, 1500);
};
for (var i = 0; i < len; i++) {
    li[i].index = i;
    /*定义index记录当前鼠标在li的位置*/
    li[i].onmouseenter = function () { /*定义鼠标经过事件*/
        for (var i = 0; i < len; i++) { /*通过for循环将所有图片隐藏，圆点背景设为白色*/
            li[i].style.background = '#fff';
            img[i].style.display = 'none';
        }
        this.style.background = '#f40';
        /*设置当前所指圆点的背景色*/
        img[this.index].style.display = 'block';
        /*使圆点对应的图片显示*/
    }
}
div_r.onclick = function () { /*因为span没有设置宽高，直接把事件添加到他的父级*/
    // console.log('12');
    run();
    /*直接调用现成的run函数*/
};

function reverse() {
    // console.log('34');
    count--;
    count = count == -1 ? 4 : count;
    for (var i = 0; i < len; i++) {
        img[i].style.display = 'none';
        /*利用for循环使除当前count位其他图片隐藏*/
    }
    img[count].style.display = 'block';
    /*显示当前count的值所代表的图片*/
    for (var i = 0; i < li.length; i++) {
        li[i].style.backgroundColor = "#fff";
        /*原理同上*/
    }
    li[count].style.backgroundColor = "#f40";
}

div_l.onclick = function () {
    reverse();
    /*重新设置函数*/
};
//
// $(function () {
//     $("#img-captcha").click(function (event) {
//        var self = $(this);
//        var src = self.attr('src');
//        var newsrc = xtparam.setParam(src, "xx", Math.random());
//        self.attr('src', newsrc)
//     });
// });
//页面加载时，生成随机验证码
window.onload = function () {
    createCode(4);
};

//生成验证码的方法
function createCode(length) {
    var code = "";
    var codeLength = parseInt(length); //验证码的长度
    var checkCode = document.getElementById("checkCode");
    ////所有候选组成验证码的字符，当然也可以用中文的
    var codeChars = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z');
    //循环组成验证码的字符串
    for (var i = 0; i < codeLength; i++) {
        //获取随机验证码下标
        var charNum = Math.floor(Math.random() * 62);
        //组合成指定字符验证码
        code += codeChars[charNum];
    }
    if (checkCode) {
        //为验证码区域添加样式名
        checkCode.className = "code";
        //将生成验证码赋值到显示区
        checkCode.innerHTML = code;
    }
}

//检查验证码是否正确
function securitycode() {
    //获取显示区生成的验证码
    var checkCode = document.getElementById("checkCode").innerHTML;
    //获取输入的验证码
    var inputCode = document.getElementById("inputCode").value;
    if (inputCode.length <= 0) {
        alert("请输入验证码！");
        return false
    } else if (inputCode.toUpperCase() != checkCode.toUpperCase()) {
        alert("验证码输入有误！");
        createCode(4);
        return false
    } else {
        // alert("验证码正确！");
        return true
    }
}

function validateCode() {
    //获取显示区生成的验证码
    var checkCode = document.getElementById("checkCode").innerHTML;
    //获取输入的验证码
    var inputCode = document.getElementById("inputCode").value;
    console.log(checkCode);
    console.log(inputCode);
    if (inputCode.length <= 0) {
        alert("请输入验证码！");
    } else if (inputCode.toUpperCase() != checkCode.toUpperCase()) {
        alert("验证码输入有误！");
        createCode(4);
    } else {
        alert("验证码正确！");
    }
}
function hidden_msg() {
    var uname = document.getElementsByClassName("msg")[0].innerHTML;
    console.log(uname);
    if(uname){
        document.getElementsByClassName("msg")[0].innerHTML = "";
    }
    return false;
}














