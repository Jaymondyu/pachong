// 点击弹出摄像头
var CURRENTIFRAMEURL = "" //保存当前监控视频的地址
var CURRENTTEXT = ""
$('.j-v').click(function(){
    var curDataId = $(this).attr('data-id');
    switch(curDataId){
        case "1":
        CURRENTIFRAMEURL = "http://www.tylin-js.com.cn:8888/monitor/jiangjin/index2.html";
        CURRENTTEXT = "2号塔吊"
        break
        case "2":
        CURRENTIFRAMEURL = "http://www.tylin-js.com.cn:8888/monitor/jiangjin/index1.html";
        break
        case "3":
        CURRENTIFRAMEURL = "http://www.tylin-js.com.cn:8888/monitor/jiangjin/index3.html";
        break
        case "4":
        CURRENTIFRAMEURL = "http://www.tylin-js.com.cn:8888/monitor/jiangjin/index4.html";
        break
        case "5":
        CURRENTIFRAMEURL = "http://www.tylin-js.com.cn:8888/monitor/jiangjin/index5.html";
        break
    };

    $('.iframe-alert').show()
    $('#myiframe').attr('src',CURRENTIFRAMEURL);
});


$('.iframe-close').click(function(){
    $('.iframe-alert').hide()
    $('#myiframe').attr('src',"");
})


//塔吊资料
$('.tips').click(function(){
    var curDataId = $(this).attr('data-id'); 
    switch(curDataId){
        case "1":
        CURRENTTEXT = "2号塔吊"
        break
        case "2":
        CURRENTTEXT = "1号塔吊"
        break
        case "3":
        CURRENTTEXT = "2号塔吊"
        break
        case "4":
        CURRENTTEXT = "4号塔吊"
        break
        case "5":
        CURRENTTEXT = "5号塔吊"
        break
    };
    $('.iframe-text').slideDown().find('p').text(CURRENTTEXT);
});


$('.iframe-close2').click(function(){
    $('.iframe-text').slideUp().find('p').text("");
})








































































































