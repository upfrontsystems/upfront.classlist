$(function() {

    $("#learner-add").bind('click', function() {
        console.log("ADD")
    });

    $("#learner-remove").bind('click', function() {
        var remove_list = [];
        $('#learner-listing input:checked:enabled').each(function(index, para) { 
            remove_list[index] = $(para).attr('value');
        });
        var title = $('#classlist-title').val()
        $.ajax({
            url: '@@removelearners',
            data: {
                'remove_uids': remove_list,
            },
            traditional: true, // needed to send js array via ajax
            dataType: "json",
            success: updateLearnerListing,
            error: displayError,
        });

    });

});

function updateView(data) {
    var result = data.result;
    var contents = data.contents;
    console.log(result)
    console.log(contents)
    if (result == 'info') {
        console.log('INFO')
    }
    else if (result == 'error') {
        console.log('ERROR')
    }
}

function updateLearnerListing(data) {
    // XXX create this function
}

function displayError(data) {
    // XXX update with real error
    console.log('AJAX ERROR')
}
