$(function() {

    $("#learner-add").live("click", function() {

        clearErrors();

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

    $("#learner-remove").live("click", function() {

        clearErrors();

        if ( $('#div-learner-listing input:checked:enabled').size() != 0 ) {

            var remove_list = [];
            $('#div-learner-listing input:checked:enabled').each(
            function(index, para) { 
                remove_list[index] = $(para).attr('value');
            });

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

        }

    });

function updateLearnerListingPostRemove(data) {

    // delete selected table entries    
    $('#div-learner-listing input:checked:enabled').parent().parent().remove()

    // if no entries now exist
    if ( $('#div-learner-listing tr:last').length == 0 ) {
       // no table entries exist yet to clone, use hidden template
       var message = $('#no-learners-template').clone().html()
       $('#div-learner-listing').html(message)
    }
    else {
        //fix styling in table
        $('#div-learner-listing tr:odd').removeClass("odd even").addClass("even")
        $('#div-learner-listing tr:even').removeClass("odd even").addClass("odd")
    }

    showStatusMessage(data);
}

function updateLearnerListingPostAdd(data) {

    if ( data.status != 'error' ) {
        var id = data.learner_id;
        var code = data.learner_code;
        var name = data.learner_name;
        var editurl = data.learner_editurl;
        var gender = data.learner_gender;
        var lang = data.learner_lang;
    
        if ( $('#div-learner-listing tr:last').length == 0 ) {
            // no table entries exist yet to clone, use hidden template
            var first_row = $('#table-row-template').clone().html()
            $('#div-learner-listing').html(first_row)
        }
        else {
            // clone last table row
            var row = $('#div-learner-listing tr:last').clone();
            $('#div-learner-listing tr:last').after(row);
        }

        //fix styling
        $('#div-learner-listing tr:odd').removeClass("odd even").addClass("even")
        $('#div-learner-listing tr:even').removeClass("odd even").addClass("odd")

        // update contents of cloned row to reflect contents of json callback

        //checkbox
        $('#div-learner-listing tr:last #id-learner').attr('value',id)
        $('#div-learner-listing tr:last #id-learner').attr("checked", false)
        // code
        $('#div-learner-listing tr:last td:nth-child(2)').html(code)
        // name link
        $('#div-learner-listing tr:last td:nth-child(3) a').attr('href', editurl)
        $('#div-learner-listing tr:last td:nth-child(3) a').addClass('edit_link')
        $('#div-learner-listing tr:last td:nth-child(3) a').html(name)
        // language
        $('#div-learner-listing tr:last td:nth-child(4)').html(lang)
        // gender
        $('#div-learner-listing tr:last td:nth-child(5)').html(gender)

        // clear the learner code and name fields
        $('#classlist-code').attr('value','')
        $('#classlist-name').attr('value','')

        showStatusMessage(data);
    }
    else {
        showStatusMessage(data);
    }
    
}

function displayError(data) {
    var data = {'status' : 'error', 'msg' : 'ajax error'}
    showStatusMessage(data);
}

function clearErrors() {
    $('.portalMessage').removeClass('info error').hide()
    // if there were more than one error boxes active, remove all but 1st one.
    $('#content').find(".portalMessage:gt(0)").remove() 
}

function showStatusMessage(data) {

    if ( $('.portalMessage').length == 0 ) {
        // if there is no portal message div in the template yet        
        $('#content').prepend('<dl class="portalMessage"><dt></dt><dd></dd>'+
                              '</dl>');
    }
    $('.portalMessage').addClass(data.status)
    var msg = data.status_msg.charAt(0).toUpperCase() + data.status_msg.slice(1)
    $('.portalMessage dt').html(msg)
    $('.portalMessage dd').html(data.msg)
    $('.portalMessage').show()
}

});
