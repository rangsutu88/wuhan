
    var BUSYING = false;   //ＤＷＲ调用控制变量
    $(document).ready(function(){
        var  object = document.getElementsByName( 'lenn41' );
        for ( var  i = 0 ;i < object.length;i ++ )  {
            var a = object[i].innerHTML;
            a = a.replace(/\s/gi,'');
            if(a.length > 41){
                object[i].innerHTML =a.substring(0,40)+ "...";
            }
        }

        var pages = parseInt("246");
        $(".quotes").find("a").eq(1).addClass("current");
        if(pages>12){
            $("#back").removeClass("disabled");
        }
        $("#front").click(function(){
            var firstPage = $(".quotes").find("a").eq(1).text();
            var lastPage = $(".quotes").find("a").eq(12).text();
            var pagesum = parseInt("246");
            if(parseInt(firstPage)>1){
                $("a[name='pagenum']").each(function(){
                    $(this).removeAttr("class");
                    $(this).text(parseInt($(this).text())-1);
                    $(this).attr("id",parseInt($(this).text()));
                    $(this).addClass($(this).text());
                })
            }
            if((pagesum>parseInt(lastPage)-1)){
                $("#back").removeClass("disabled");
            }else{
                $("#back").addClass("disabled");
            }
            if((parseInt(firstPage)-1)>1){
                $("#front").removeClass("disabled");
            }else{
                $("#front").addClass("disabled");
            }
        })
        $("#back").click(function(){
            var firstPage = $(".quotes").find("a").eq(1).text();
            var lastPage = $(".quotes").find("a").eq(12).text();
            var pagesum = parseInt("246");
            if(pagesum>parseInt(lastPage)){
                $("a[name='pagenum']").each(function(){
//                    if($(this).id.indexOf("_")>-1){
//                        var ids = $(this).text().split("_");
//                        $(this).text((parseInt(ids[0])+1)+ids[1]);
//                        $(this).attr("id",parseInt($(this).text()));
//                    }else{
                    $(this).removeAttr("class");
                    $(this).text(parseInt($(this).text())+1);
                    $(this).attr("id",parseInt($(this).text()));
                    $(this).addClass($(this).text());
//                    }
                })
            }
            if((parseInt(firstPage)+1)>1){
                $("#front").removeClass("disabled");
            }else{
                $("#front").addClass("disabled");
            }
            if((pagesum>parseInt(lastPage)+1)){
                $("#back").removeClass("disabled");
            }else{
                $("#back").addClass("disabled");
            }
        })
        $("a[name='pagenum']").click(function(){
            var page=$(this).text();
            $("a[name='pagenum']").each(function(){
                $(this).removeClass("current");
            })
            $("."+page).addClass("current");
            pageClick1(page);
        });

    });
    function pageClick(id){
        $("a[name='pagenum']").each(function(){
            $(this).removeClass("current");
        })
        $("#"+id).addClass("current");//todo 当前页未标记
        var paramap = {};
        paramap["_COLCODE"]=$("#col_code").val();
        paramap["_INDEX"]=id;      //页码
        paramap["_PAGESIZE"]=10;
        paramap["_REGION"]=$("#region").val();
        dwrmng.queryWithoutUi(7, paramap, ret_getdate);
    }
    function pageClick1(id){
        var ids=id.split("_");

//        $("#"+ids[0]).addClass("current");//todo 当前页未标记
        var paramap = {};
        paramap["_COLCODE"]=$("#col_code").val();
        paramap["_INDEX"]=ids[0];      //页码
        paramap["_PAGESIZE"]=10;
        paramap["_REGION"]=$("#region").val();
        paramap["_KEYWORD"]=ids[1];
        dwrmng.queryWithoutUi(7, paramap, ret_getdate);
    }
    var ret_getdate=function(data){
        var col=$("#col_code").val();
        var j = parseInt(col.substring(col.length-1,col.length))-1;
        if(col=="01"||col=="02"||col=="06"||col=="10"){
            j=0;
        }
        try{
            if (data!=null) {
                var singles = data.rsltStringValue;
                var subject = singles.split("?");
                $("#tagContent"+j).empty();
                if(col=="0701"){
                    if(!((subject[0]==null) || (subject[0]==""))){
                        for(var i=0; i<subject.length; i++){
                            var single = subject[i].split(",");
                            $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                            "<a href='/sdgp2014/site/viewContract370200.jsp?contractId="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>"+single[1]+"</a></div>"+
                            "<div class='neitime'>"+single[2]+"</div></div>")
                        }
                    }else{
                        $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'><a href='#' title=''>没有查询到信息！</a></div><div class='neitime'></div></div>")
                    }
                }else if(col=="0702"){
                    if(!((subject[0]==null) || (subject[0]==""))){
                        for(var i=0; i<subject.length; i++){
                            var single = subject[i].split(",");
                            $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                            "<a href='/sdgp2014/site/viewChk370200.jsp?contractId="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>"+single[1]+"</a></div>"+
                            "<div class='neitime'>"+single[2]+"</div></div>")
                        }
                    }else{
                        $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'><a href='#' title=''>没有查询到信息！</a></div><div class='neitime'></div></div>")
                    }
                }else if(col.substring(0,2)=="05"||col.substring(0,2)=="04"){
                    if(!((subject[0]==null) || (subject[0]==""))){
                        for(var i=0; i<subject.length; i++){
                            var single = subject[i].split(",");
                            if(single[3]=="370202"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[市南区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370203"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[市北区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370211"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[黄岛区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370212"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[崂山区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370213"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[李沧区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370214"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[城阳区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370281"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[胶州市]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370282"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[即墨区]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370283"){
                                $("#tagContent"+j).append("<div class='neitzbox'><div class='neinewli'>"+
                                "<a href='read370200.jsp?id="+single[0]+"&flag=0401' title='"+single[1]+"' target='_blank'>[平度市]"+single[1]+"</a></div>"+
                                "<div class='neitime'>"+single[2]+"</div></div>");
                            }else if(single[3]=="370285"){
                                $("#tagContent"+j).append("<div class='neitzbo…