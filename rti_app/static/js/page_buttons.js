$(document).ready(function(){
    $('#forward_button').click(function(){
        var searchParams = new URLSearchParams(window.location.search); //?anything=123
        // console.log(searchParams.get("anything")) //123
        var page = searchParams.get("page")

    });
});

$(document).ready(function(){
    $('#rev_button').click(function(){
        var searchParams = new URLSearchParams(window.location.search); //?anything=123
        // console.log(searchParams.get("anything")) //123
        var page = searchParams.get("page")
    });
});