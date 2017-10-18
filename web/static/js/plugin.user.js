// ==UserScript==
// @name          搜索重排
// @namespace     http://diveintogreasemonkey.org/download/
// @description   对百度搜索结果评分并重排
// @require      /System/server/web/static/js/jquery-1.11.3.js 
// @grant         GM_addStyle 
// @include       *www.baidu.com*
// @exclude       http://diveintogreasemonkey.org/*
// @exclude       http://www.diveintogreasemonkey.org/*
// ==/UserScript==

GM_addStyle('#s_tab a.i{ width: 108px; color: blue; font-size: 18px; font-weight: bold; }');//文字的大小
//GM_addStyle('#s_tab{background:pink;}');
GM_addStyle('.result-op { display: none; }');    
GM_addStyle('.result { position: relative; }');
GM_addStyle('.result .score-container { width: 300px; height: 240px; display: none; border: 1px solid #eee; position: absolute; left: 550px; top: 0px; box-shadow: 1px 1px 1px #ccc; padding: 10px; background: white}');
GM_addStyle('.result .score-container .score { font-size: 18px; color: #666; }');
GM_addStyle('.result .score-container img { width: 100% }');
GM_addStyle('.result.down:before { content: "▲";color: red;position: absolute;left: -19px; }');
GM_addStyle('.result.up:before { content: "▼";color: green;position: absolute;left: -19px; }');
//GM_addStyle('.hide { display: none!important }');
GM_addStyle('.result:hover .score-container { display: block; }');
GM_addStyle('#loading { display: none; position: fixed; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; top:0; left:0; text-align: center; text-align: center; }');
GM_addStyle('#loading .load { display: inline-block; background: white; border: 1px solid #ccc; border-radius: 3px; width: 120px; height: 50px; padding: 15px; text-align: center; margin-top: 30% }');
GM_addStyle('#loading .load p { font-size: 12px; margin-top: 5px }');
//$("body").css("background-color","#000000"); //测试效果，背景变黑
$('#s_tab').append($('<a>').text('点此重排').addClass('i').attr('href', 'javascript:void(0)').click(get_score));

if($('.leftBlock').length){//如果有结果
    $('<div>').addClass('anchor').insertAfter('.leftBlock');
}else{
    $('#content_left').prepend($('<div>').addClass('anchor'));
}

results = [];
scores = [];

$('.result').each(
    function(ind, item) {
        results.push($(item).find('.t a').attr('href'));
        //alert('fighting!');
        html = "<div>得分:<span class='score'></span></div>"+  "<div class='img-container'><img></div>";//以下这些都是一个初始化的过程，至于其具体的值是在后面的运算中逐渐加进来的
        $(item).append($('<div>').addClass('.score-container hide').attr('id', 'score-'+ind).html(html));
    });

load_html = "<div class='load'>评分中...<img src='http://jimpunk.net/Loading/wp-content/uploads/loading3.gif' width=15><p>已完成：<span class='done'>0</span>/"+3+"</p></div>"//算分时显示的东西

$('body').append($('<div></div>').attr('id', 'loading').html(load_html));

function show_loading(){
    $('#loading').show();
    update_loading(0);
}

function hide_loading(){//将loading隐藏起来
    $('#loading').hide();
}

function update_loading(x){
    x = x===undefined? (parseInt($('#loading .done').text()) + 1): x;
    $('#loading .done').text(x);
    if(x==3){   
        hide_loading();
        resort();
    }
}

function resort(){
    //alert('you are right');//出现
    sorted = scores.sort(function(a, b){
        return parseFloat(a.res) - parseFloat(b.res);
    });
    //alert('you are right');//出现
    //GM_log(sorted);//dont know
    alert('you are right');//没出现，所以先注释掉上一句
    for(i=0;i<3;i++){
           s = sorted[i];
        $('#score-'+s.id).parents('.result').addClass('new-'+i).insertAfter('#content_left .anchor');
        //alert('...');//这里出现了
        if(parseInt(s.id)>i){
               $('#score-'+s.id).parents('.result').addClass('up');
        }
        if(parseInt(s.id)<i){
            $('#score-'+s.id).parents('.result').addClass('down');
        }       
    }
}
//下面这个函数是用来以对话框的形式显示分数的，可以不管它
function writeObj(obj){
    var description = "";
    for(var i in obj){  
        var property=obj[i];  
        description+=i+" = "+property+"\n"; 
    }  
    alert(description);
}

function get_score(){ 
    show_loading();
    $('.result .score-container').removeClass('hide');//把所有有hide的都去掉
    for(i=0;i<3;i++){
        (function(ii){
    $.ajax({
        type: "POST", 
         dataType: "json", 
         url: 'https://127.0.0.1:81/api/json',
        data:{'id':i,'res':results[i]},
        timeout:170000,
        success: function (data) { //数据传输完一次 就做一次下面的操作
          scores.push(data);
           
             sf = parseFloat(data['res']);
            score = sf.toFixed(2);
            writeObj(data);//显示分数和排序
            //alert(score);
             id = data['id'];
             $('#score-'+id+' .score').text(score+'分');//最终输出分数的地方
             $('#score-'+id+' img').attr('src', 'https://127.0.0.1:81/extractor/screenshot'+encodeURIComponent(data.img)+'?r='+Math.random());
             update_loading();//加一次的目的 演示中的效果
       },
        error: function (err) {
            update_loading();
            $('#score-'+ii+' .score').text('评分出现了错误');
        }
     });
 })(i);
}
};

