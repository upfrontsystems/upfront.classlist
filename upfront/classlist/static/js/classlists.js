$(function() {

    $("#classlist-save").bind('click', function() {
        console.log("SAVE")
        var title = $('#classlist-title').val()
        var ajax_url = '@@renameclasslist?title=' + title;
        $.ajax({
            url: ajax_url,
            success: function(data) {
                $('.result').html(data);
                console.log("SAVE was performed");
            }
        });
    });

    $("#learner-add").bind('click', function() {
        console.log("ADD")
    });

    $("#learner-remove").bind('click', function() {
        console.log("REMOVE")
    });

});
