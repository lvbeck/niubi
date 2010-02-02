var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
try {
    var pageTracker = _gat._getTracker("UA-10256201-1");
    pageTracker._trackPageview();
} catch(err) {}

function setCurrent(elem){
    var i, a;
    for(i=0; (a = elem.parentNode.childNodes[i]); i++){
        a.className = "";
    }
    elem.className="current";     
}

function setContent(id, path){
    var cid = id;
    $.get(path, function(data){
        $("#"+cid).html(data);
    });  
}

function setActiveStyleSheet(title) {
    var i, a, main;
    for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
        if(a.getAttribute("rel").indexOf("style") != -1 && a.getAttribute("title")) {
            a.disabled = true;
            if(a.getAttribute("title") == title) a.disabled = false;
        }
    }
    for(i=0; (a = document.getElementsByTagName("li")[i]); i++) {
        if(a.getAttribute("title")) {
            if(a.getAttribute("title")==title) {
                    a.className = "current";
            } else {
                    a.className = "";
            }
        }
    }
}

function getActiveStyleSheet() {
    var i, a;
    for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
        if(a.getAttribute("rel").indexOf("style") != -1 && a.getAttribute("title") && !a.disabled) return a.getAttribute("title");
    }
    return null;
}

function getPreferredStyleSheet() {
    var i, a;
    for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
        if(a.getAttribute("rel").indexOf("style") != -1
            && a.getAttribute("rel").indexOf("alt") == -1
            && a.getAttribute("title")
        ) return a.getAttribute("title");
    }
    return null;
}

function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

window.onload = function(e) {
    var cookie = readCookie("style");
    var title = cookie ? cookie : getPreferredStyleSheet();
    setActiveStyleSheet(title);
}

window.onunload = function(e) {
    var title = getActiveStyleSheet();
    createCookie("style", title, 365);
}

jQuery(document).ready(function(){
    jQuery(".ui-accordion-container").accordion({
        header: ".ui-accordion-header",
        autoHeight: false,
	clearStyle: true,
        alwaysOpen: false
    });

    jQuery(function($){
        jQuery.datepicker.regional['zh-CN'] = {
                clearText: '清除', clearStatus: '清除已选日期',
                closeText: '关闭', closeStatus: '不改变当前选择',
                prevText: '&#x3c;上月', prevStatus: '显示上月',
                prevBigText: '&#x3c;&#x3c;', prevBigStatus: '显示上一年',
                nextText: '下月&#x3e;', nextStatus: '显示下月',
                nextBigText: '&#x3e;&#x3e;', nextBigStatus: '显示下一年',
                currentText: '今天', currentStatus: '显示本月',
                monthNames: ['一月','二月','三月','四月','五月','六月',
                '七月','八月','九月','十月','十一月','十二月'],
                monthNamesShort: ['一','二','三','四','五','六',
                '七','八','九','十','十一','十二'],
                monthStatus: '选择月份', yearStatus: '选择年份',
                weekHeader: '周', weekStatus: '年内周次',
                dayNames: ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'],
                dayNamesShort: ['周日','周一','周二','周三','周四','周五','周六'],
                dayNamesMin: ['日','一','二','三','四','五','六'],
                dayStatus: '设置 DD 为一周起始', dateStatus: '选择 m月 d日, DD',
                dateFormat: 'yy-mm-dd', firstDay: 1, 
                initStatus: '请选择日期', isRTL: false};
        $.datepicker.setDefaults($.datepicker.regional['zh-CN']);
    });

    jQuery('#ui-datepicker').datepicker({
	changeFirstDay: false
    });
    jQuery("textarea > br").each( function() { jQuery(this).replaceWith( "\n" ); } );
    SyntaxHighlighter.config.bloggerMode = true;
    SyntaxHighlighter.config.clipboardSwf = "http://alexgorbatchev.com/pub/sh/current/scripts/clipboard.swf";
    SyntaxHighlighter.all();
    dp.SyntaxHighlighter.HighlightAll("code");       
});

// Call this function when the page has been loaded
function initialize() {  
    var searchControl = new google.search.SearchControl();
    // create a drawOptions object
    var drawOptions = new google.search.DrawOptions();  
    // tell the searcher to draw itself in tabbed mode
    drawOptions.setDrawMode(google.search.SearchControl.DRAW_MODE_LINEAR);
    // create a searcher options object
    var searchOptions = new google.search.SearcherOptions();
    // set up for open expansion mode
    searchOptions.setExpandMode(google.search.SearchControl.EXPAND_MODE_CLOSED);
    
    //searchControl.addSearcher(new google.search.LocalSearch(),searchOptions);
    var siteSearch = new google.search.WebSearch();
    siteSearch.setUserDefinedLabel("站内");
    siteSearch.setUserDefinedClassSuffix("siteSearch");
    siteSearch.setSiteRestriction(document.location.hostname);    
    searchControl.addSearcher(siteSearch,searchOptions);
    searchControl.addSearcher(new google.search.WebSearch(),searchOptions);
    searchControl.addSearcher(new google.search.BlogSearch(),searchOptions);
    searchControl.addSearcher(new google.search.VideoSearch(),searchOptions);
    //searchControl.addSearcher(new google.search.NewsSearch(),searchOptions);
    searchControl.addSearcher(new google.search.ImageSearch(),searchOptions);
    //searchControl.addSearcher(new google.search.BookSearch(),searchOptions);    
    searchControl.draw(document.getElementById("searchcontrol"),drawOptions); 
}

google.setOnLoadCallback(initialize);