$(function() {

    $("#classlist-save").bind('click', function() {
        console.log("SAVE")
        var title = $('#classlist-title').val()
        $.ajax({
            url: '@@renameclasslist',
            data: {
                'title': title
            },
            dataType: "json",
            success: updateView,
            error: displayError,
        });
    });

    $("#learner-add").bind('click', function() {
        console.log("ADD")
    });

    $("#learner-remove").bind('click', function() {
        console.log("REMOVE")
    });

});

function updateView(data) {
    var result = data.result;
    var contents = data.contents;
    var url = data.url
    console.log(result)
    console.log(contents)
    if (result == 'info') {
//        window.location.href = url
        console.log('INFO')
    }
    else if (result == 'error') {
        console.log('ERROR')
    }
}

function displayError(data) {
    // XXX update with real error
    console.log('AJAX ERROR')
}
