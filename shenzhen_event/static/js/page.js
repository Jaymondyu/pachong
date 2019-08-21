var MYID;
var REQUESTURL="/table" //保存此时筛选发送的ajax地址
var DPISELECT="0" //保存此时筛选要发送的dpi值（哪个部门）;
// 存储各分页总数
var TOTAL ={"total":0}
var COMPLETE ={"total":0}
var IN_PLAN ={"total":0}
var LATE ={"total":0}
var NEAR ={"total":0}

var CURRENTCLASS = TOTAL; //当前筛选dpi所对应的条件
//页面初始化
function pageInit(){
    var sendJson = {
        "dpi":DPISELECT,
        "page":1
    }
    $.ajax({
        type: "post",
        url: "/table",
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response)
            var getTpl = $('#tabletr').html();
            var view = $('.cnt-table tbody');
            layui.laytpl(getTpl).render(data, function (html) {
                view.html(html);
            });


        }
    });
    //获取初始对应dpi下面各部门的总页数
    var sendJson = {
        "dpi":DPISELECT
    };
    $.ajax({
        type: "post",
        url: "/table/page",
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response);
            TOTAL.total = data[0].total;
            COMPLETE.total = data[0].complete;
            IN_PLAN.total = data[0].in_plan;
            LATE.total = data[0].late;
            NEAR.total = data[0].near;
            console.log(TOTAL);
            console.log(CURRENTCLASS.total)
            pageTotal(CURRENTCLASS.total)
        }
    });
}

pageInit()

//新增事件
$('.add-btn').click(function () {
    var getTpl = $('#addalert').html();
    var view = $('body');
    layui.laytpl(getTpl).render({}, function (html) {
        view.append(html);
    });

    layui.laydate.render({
        elem: '#mydate1' //指定元素
    });
    layui.laydate.render({
        elem: '#mydate2' //指定元素
    });
})

//取消新增
$('body').on('click', '.cancel-btn', function () {
    $('.add-alert-wrap').remove();
})

//确定新增
$('body').on('click', '.j-sumbit', function () {
    var event_name  = $('.my-text').val();
    var plan_time = $('#mydate1').val();
    var start_plan = $('#mydate2').val();
    var dpi =  parseInt($('.j-selec-zrf').val()) ;

    sendJson = {
        "event_name":event_name,
        "start_plan":start_plan,
        "plan_time":plan_time,
        "dpi":dpi,
        "finish_time":""
    };

    $.ajax({
        type: "post",
        url: "/table/insert",
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response)
            var getTpl = $('#tabletr').html();
            var view = $('.cnt-table tbody');
            layui.laytpl(getTpl).render(data, function (html) {
                view.html(html);
            });
            $('.add-alert-wrap').remove()

        },
        error:function(){
            $('.add-alert-wrap').remove()
        }
    });
})



//选择责任方联动责任人
$('body').on('change', '.j-selec-zrf', function () {
    var currentp = "";
    switch ($(this).val()) {
        case "1":
            currentp = "张福生"
            break
        case "2":
            currentp = "黄兴"
            break
        case "3":
            currentp = "唐光勤"
            break
        case "4":
            currentp = "蔡超"
            break
        case "8":
            currentp = "李宇"
            break
        case "12":
            currentp = "李亮"
            break
    };
    $('.add-zrr-p').html("");
    $('.add-zrr-p').html(currentp)
});


//消项
$('body').on('click', '.j-xiaox', function () {
    var myid = $(this).parents('tr').attr('data-id');
    var event_name = $(this).parents('tr').find("td").eq(0).text();

    sendJson = {
        "id":myid,
    };

    layui.layer.open({
        title: '确定要销项吗？',
        content: "任务事件："+event_name,
        yes:function(index){
            $.ajax({
                type: "post",
                url: "/table/cancel",
                contentType:'application/json;charset=UTF-8',
                data:JSON.stringify(sendJson),
                success:function (response) {
                    var data = JSON.parse(response)
                    var getTpl = $('#tabletr').html();
                    var view = $('.cnt-table tbody');
                    layui.laytpl(getTpl).render(data, function (html) {
                        view.html(html);
                    });
                    $('.add-alert-wrap').remove()

                },
                error:function(){
                    $('.add-alert-wrap').remove()
                }
            });
            layui.layer.close(index)
        }
      });


});

//修改
$('body').on('click', '.j-modify2', function () {
    var thisTd = $(this).parents('tr').find("td");
    MYID = $(this).parents('tr').attr('data-id');
    var event_name = thisTd.eq(0).text();
    var start_plan = thisTd.eq(1).text();
    var plan_time = thisTd.eq(2).text();
    var dpi = thisTd.eq(5).text();
    var zrr = thisTd.eq(6).text();

    var oldData = {
        "event_name":event_name,
        "plan_time":plan_time,
        "dpi":dpi,
        "start_plan":start_plan,
        "zrr":zrr
    };

    var getTpl = $('#modifyalert').html();
    var view = $('body');
    layui.laytpl(getTpl).render(oldData, function (html) {
        view.append(html);
    });
    layui.laydate.render({
        elem: '#mydate3' //指定元素
    });
    layui.laydate.render({
        elem: '#mydate4' //指定元素
    });

});

//删除
$('body').on('click', '.j-del', function () {
    var event_name = $(this).parents('tr').find("td").eq(0).text();
    var myid = $(this).parents('tr').attr('data-id');

    sendJson = {
        "id":myid,
    };
     layui.layer.open({
        title: '确定要删除吗？',
        content: "任务事件："+event_name,
        yes:function(index){
            $.ajax({
                type: "post",
                url: "/table/delete",
                contentType:'application/json;charset=UTF-8',
                data:JSON.stringify(sendJson),
                success:function (response) {
                    var data = JSON.parse(response)
                    var getTpl = $('#tabletr').html();
                    var view = $('.cnt-table tbody');
                    layui.laytpl(getTpl).render(data, function (html) {
                        view.html(html);
                    });
                    $('.add-alert-wrap').remove()

                },
                error:function(){
                    $('.add-alert-wrap').remove()
                }
            });
            layui.layer.close(index)
        }
      });

});

//确定修改
$('body').on('click', '.j-modify', function () {
    var event_name  = $('.my-text').val();
    var plan_time = $('#mydate3').val();
    var start_plan = $('#mydate4').val();
    var dpi =  parseInt($('.j-selec-zrf').val()) ;

    sendJson = {
        "event_name":event_name,
        "start_plan":start_plan,
        "plan_time":plan_time,
        "dpi":dpi,
        "id":MYID,
        "finish_time":""
    };

    $.ajax({
        type: "post",
        url: "/table/change",
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response)
            var getTpl = $('#tabletr').html();
            var view = $('.cnt-table tbody');
            layui.laytpl(getTpl).render(data, function (html) {
                view.html(html);
            });
            $('.add-alert-wrap').remove()

        },
        error:function(){
            $('.add-alert-wrap').remove()
        }
    });
})

//过滤排序


$('.filter-btn').click(function(){
    $('.filter-btn').removeClass('clickclass');
    $(this).addClass('clickclass');
    var currentVal = $(this).attr('data-val');
    switch(currentVal){
        case "0":
        REQUESTURL = "/table";
        CURRENTCLASS = TOTAL
        break
        case "1":
        REQUESTURL = "/table/late";
        CURRENTCLASS = LATE
        break
        case "2":
        REQUESTURL = "/table/near";
        CURRENTCLASS = NEAR
        break
        case "3":
        REQUESTURL = "/table/complete";
        CURRENTCLASS = COMPLETE
        break
        case "4":
        REQUESTURL = "/table/in_plan";
        CURRENTCLASS = IN_PLAN
        break
    };
    var sendJson = {
        "dpi":DPISELECT,
        "page":1
    }
    $.ajax({
        type: "post",
        url: REQUESTURL,
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response)
            var getTpl = $('#tabletr').html();
            var view = $('.cnt-table tbody');
            layui.laytpl(getTpl).render(data, function (html) {
                view.html(html);
            });
            pageTotal(CURRENTCLASS.total)

        }
    });

});

//总体统计

$.ajax({
    type: "get",
    url: "/table/count",
    success:function (response) {
        var data = JSON.parse(response)
        $('.j-t-wc').text(data[0].complete);
        $('.j-t-jhl').text(data[0].in_plan);
        $('.j-t-zh').text(data[0].late);
        $('.j-t-lj').text(data[0].near);
    }
});

//获取日期,且更新进度条
var JINGFUCONFIG = ['07','08','09','10'] //手工配置对应的进度日期
$.ajax({
    type: "get",
    url: "/table/date",
    success:function (response) {
        $('.cnt-sp').text(response);
        var cuMonth = response.slice(5,7);
        var jinduIndex =  JINGFUCONFIG.indexOf(cuMonth)
        var curProClass = ""
        switch(jinduIndex){
            case 0:
            curProClass = "j0";
            break
            case 1:
            curProClass = "j1";
            break
            case 2:
            curProClass = "j2";
            break
            case 3:
            curProClass = "j3";
            break
        };
        $('.tyl-progress').removeClass(curProClass);
        $('.tyl-progress').addClass(curProClass);
    },
    error:function(err){
        alert(JSON.stringify(err))
    }
});


//下拉框筛选查询
$('#sx-select').change(function(){
    DPISELECT = $(this).val()
    var sendJson = {
        "dpi":DPISELECT
    }
    $.ajax({
        type: "post",
        url: REQUESTURL,
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response)
            var getTpl = $('#tabletr').html();
            var view = $('.cnt-table tbody');
            layui.laytpl(getTpl).render(data, function (html) {
                view.html(html);
            });


        }
    });
    //获取对应DPI的所有项的分页总数
    $.ajax({
        type: "post",
        url: "/table/page",
        contentType:'application/json;charset=UTF-8',
        data:JSON.stringify(sendJson),
        success:function (response) {
            var data = JSON.parse(response);
            TOTAL.total = data[0].total;
            COMPLETE.total = data[0].complete;
            IN_PLAN.total = data[0].in_plan;
            LATE.total = data[0].late;
            NEAR.total = data[0].near;
            pageTotal(CURRENTCLASS.total)
        }
    });
})

//各分页


//初始化分页函数
function pageTotal(totalpage){

    layui.use('laypage', function(){
        var laypage = layui.laypage;
        //执行一个laypage实例
        laypage.render({
          theme:'#1E9FFF',
          groups:5,
          elem: 'paging' //注意，这里的 test1 是 ID，不用加 # 号
          ,count: totalpage
          ,jump: function(obj, first){
          //obj包含了当前分页的所有参数，比如：
          console.log(obj.curr); //得到当前页，以便向服务端请求对应页的数据。
          console.log(obj.limit); //得到每页显示的条数
          //
            var sendJson = {
                "dpi":DPISELECT,
                "page":obj.curr
            }
            $.ajax({
                type: "post",
                url: REQUESTURL,
                contentType:'application/json;charset=UTF-8',
                data:JSON.stringify(sendJson),
                success:function (response) {
                    var data = JSON.parse(response)
                    var getTpl = $('#tabletr').html();
                    var view = $('.cnt-table tbody');
                    layui.laytpl(getTpl).render(data, function (html) {
                        view.html(html);
                    });
                }
            });

          //首次不执行
          if(!first){
            //do something
          }
        }
        });
      });
}
