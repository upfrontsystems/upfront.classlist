$(function() {

    $("#learner-add").bind('click', function() {

        var learner_code = $('#classlist-code').attr('value')
        var learner_name = $('#classlist-name').attr('value')
        var learner_gender = $('#classlist-gender').attr('value')
        var learner_lang_id = $('#classlist-homeLanguage').attr('value')
        var learner_lang = 
            $('#classlist-homeLanguage option[value='+learner_lang_id+']').html()  

        $.ajax({
            url: '@@addlearner',
            data: {
                'learner_code': learner_code,
                'learner_name': learner_name,
                'learner_gender': learner_gender,
                'learner_lang_id': learner_lang_id,
                'learner_lang': learner_lang
            },
            dataType: "json",
            success: updateLearnerListingPostAdd,
            error: displayError,
        });

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
                'remove_ids': remove_list,
            },
            traditional: true, // needed to send js array via ajax
            dataType: "json",
            success: updateLearnerListingPostRemove,
            error: displayError,
        });

    });

});

function updateLearnerListingPostRemove(data) {
    // delete selected table entries    
    $('#learner-listing input:checked:enabled').parent().parent().remove()
}

function updateLearnerListingPostAdd(data) {

    var id = data.learner_id;
    var code = data.learner_code;
    var name = data.learner_name;
    var editurl = data.learner_editurl;
    var gender = data.learner_gender;
    var lang = data.learner_lang;

    // clone last table row
    var row = $('#learner-listing tr:last').clone();
    $('#learner-listing tr:last').after(row);

    //fix styling
    $('#learner-listing tr:odd').removeClass("odd even").addClass("even")
    $('#learner-listing tr:even').removeClass("odd even").addClass("odd")

    // update contents of cloned row to reflect contents of json callback
    $('#learner-listing tr:last #id-learner').attr('value',id)
    $('#learner-listing tr:last td:nth-child(2)').html(code)
    $('#learner-listing tr:last td:nth-child(3) a').attr('href',editurl)
    $('#learner-listing tr:last td:nth-child(3) a').html(name)
    $('#learner-listing tr:last td:nth-child(4)').html(lang)
    $('#learner-listing tr:last td:nth-child(5)').html(gender)
}

function displayError(data) {
    // XXX update with real error
    console.log('AJAX ERROR')
}
