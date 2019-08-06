var MAX_DEGREE = [];
var MIN_DEGREE = [];

//获取当天的详细信息
$.ajax({
    type: "get",
    url: "/weather_qq/shenzhen/now",
    dataType: "json",
    success:function (response) {
        var d_degree = response[0].degree,
            d_weather = response[0].weather,
            d_wind_power = response[0].wind_power,
            d_timer = transferTime(response[0].update_time),
            d_pa = response[0].pressure,
            d_shidu = response[0].humidity;
            d_power = response[0].wind_power;

        var d_fengxiang = ""
        switch(response[0].wind_direction){
            case "0":
            d_fengxiang = "微风"
            break;
            case "1":
            d_fengxiang = "东北风"
            break;
            case "2":
            d_fengxiang = "东风"
            break;
            case "3":
            d_fengxiang = "东南风"
            break;
            case "4":
            d_fengxiang = "南风"
            break;
            case "5":
            d_fengxiang = "西南风"
            break;
            case "6":
            d_fengxiang = "西风"
            break;
            case "7":
            d_fengxiang = "西北风"
            break;
            case "8":
            d_fengxiang = "北风"
            break;
        }
        
        $('.j-shijian').text(d_timer);
        $('.j-wd').text(d_degree);
        $('.j-weather').text(d_weather);
        $('.j-fj').text(d_power);
        $('.j-shidu').text(d_shidu);
        $('.j-qiya').text(d_pa);
        $('.j-fx').text(d_fengxiang);

    }
})


//获取7天的天气预报
$.ajax({
    type: "get",
    url: "/weather_qq/shenzhen/7d",
    dataType: "json",
    success:function (response) {

        //显示7天日期
        var allele = $('.date-item');       
        for(var i=0;i<allele.length;i++){
            var month = response[i].time.substr(5,2);
            var date = response[i].time.substr(8,2);
            var shijian = month+'月'+date+"日";
           $(allele[i]).text(shijian);
        }
        //显示天气和最高气温
        var totalele = ""
        for(var i=0;i<response.length;i++){
            var currentele = `<div class="week-prediction-item">
            <div class="week-prediction-item-t">${response[i].day_weather}</div>
            <div class="week-prediction-item-icon state1"></div>
            <div class="week-prediction-item-temp">${response[i].max_degree}'</div>
          </div>`;
          totalele += currentele
        }
        $('.c_cnt_hight').append(totalele);
        $('.c_cnt_hight').find('.week-prediction-item').eq(0).addClass('ts1')

        //显示天气和最底气温
        var totalele = ""
        for(var i=0;i<response.length;i++){
            var currentele = `<div class="week-prediction-item">
            <div class="week-prediction-item-t">${response[i].day_weather}</div>
            <div class="week-prediction-item-icon state1"></div>
            <div class="week-prediction-item-temp">${response[i].min_degree}'</div>
          </div>`;
          totalele += currentele
        }
        $('.c_cnt_low').append(totalele);
        $('.c_cnt_low').find('.week-prediction-item').eq(0).addClass('ts1')
        //初始化echarts数据
        for(var i=0;i<response.length;i++){
            MAX_DEGREE.push(response[i].max_degree)
            MIN_DEGREE.push(response[i].min_degree)
        }

        myecharts(MAX_DEGREE,MIN_DEGREE)  

    }
});

//获取12小时的天气预报
$.ajax({
    type: "get",
    url: "/weather_qq/shenzhen",
    dataType: "json",
    success:function (response) {        
        //逐小时预报
        var totalele = ""
        for(var i=0;i<response.length;i++){
           var cur_time =  transferTime(response[i].update_time);
            var currentele = `<div class="h-prediction-item">
            <div class="h-prediction-item-h">${cur_time}:00</div>
            <div class="h-prediction-item-icon state1"></div>
            <div class="h-prediction-item-temp">${response[i].degree}'</div>
          </div>`;
          totalele += currentele
        };
        $('.h-prediction').append(totalele);

    }
});


//天气预警
$.ajax({
    type: "get",
    url: "/weather_qq/shenzhen/alarm",
    dataType: "json",
    success:function (response) { 
        if(response[0] !== 0){
            $('.light-mask').eq(0).show()
        };
        if(response[1] !== 0){
            $('.light-mask').eq(1).show() 
        };
        $('.j-y-t').text(response[2]);
        $('.j-g-t').text(response[3]);
     }
})


//echart开始
function myecharts(MAX_DEGREE,MIN_DEGREE){
    option = {
        color: ["#2682ff", "#ff7d26"],
        title: {
            show: false,
            text: '折线图堆叠'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            show: false,
            data: ['最高温度', '最低温度',]
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        /* toolbox: {
            feature: {
                saveAsImage: {}
            }
        }, */
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
            axisLine: {
                show: false,
            },
            axisLabel: {
                show: false
            },
            splitArea: {
                show: false
            }, splitLine: {
                show: false
            }, axisTick: {
                show: false
            }
        },
        yAxis: {
            type: 'value',
            axisLine: {
                show: false,
            }, splitArea: {
                show: false
            },
            splitLine: {
                show: false
            }, axisLabel: {
                show: false
            }, axisTick: {
                show: false
            }
    
        },
        series: [
            {
                name: '最高温度',
                type: 'line',
                smooth: true, //平滑曲线显示
                showAllSymbol: true, //显示所有图形。
                symbol: "circle", //标记的图形为实心圆
                symbolSize: 6, //
                data: MAX_DEGREE
            },
            {
                name: '最低温度',
                type: 'line',
                smooth: true, //平滑曲线显示
                showAllSymbol: true, //显示所有图形。
                symbol: "circle", //标记的图形为实心圆
                symbolSize: 6, //
                data: MIN_DEGREE
            }
        ]
    };
    
    var dom = document.getElementById("myecharts");
    var myChart = echarts.init(dom);
    myChart.setOption(option, true);
}

//转换时间

function transferTime(date){
    return currenttime = date.substr(8,2)
}





































