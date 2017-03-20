/**
* Perform check before submit
*/
checkSubmit = function() {
    $("#build_errors").html("");
    $("#banner_build_errors").hide(200);
    $("#downloadXML").hide();
    $("#result").text('');
    var label = '';
    if ($("select#id_data_provider").val() == '0') {
        label = 'Please pick a data provider.';
    } else if ($("select#id_verb").val() == '0') {
        label = 'Please pick a verb.';
    } else {
        if ($("select#id_verb").val() == '2') {
            if ($("select#id_metadata_prefix").val() == '0') {
                label = 'Please pick a metadata prefix.';
            } else if ($("#id_identifiers").val().trim() == '') {
                label = 'Please provide an identifier.';
            }
        } else if ($("select#id_verb").val() == '3' || $("select#id_verb").val() == '5') {
            if ($("select#id_metadata_prefix").val() == '0' && $("#id_resumption_token").val() == '') {
                label = 'Please pick a metadata prefix.';
            }
        }
    }
    if (label == '') {
        submit();
    } else {
        $("#banner_build_errors").show(200);
        $("#build_errors").html(label);
    }
}

submit = function() {
   $("#submitBtn").attr("disabled","disabled");
   $("#banner_submit_wait").show(200);
   var data_url = {};

    if ($("select#id_set").val() != '0')
    {
        data_url['set'] = $("select#id_set").val();
    }

    if ($("select#id_metadata_prefix").val() != '0')
    {
        data_url['metadataPrefix'] = $("select#id_metadata_prefix").val();
    }

    if ($("#id_identifiers").val() != '')
    {
        data_url['identifier'] = $("#id_identifiers").val();
    }

    if (typeof $("#id_resumptionToken").val() !== 'undefined' && $("#id_resumptionToken").val() != '')
    {
        data_url['resumptionToken'] = $("#id_resumption_token").val();
    }

    if ($("#id_From").val() != '')
    {
        data_url['from'] = $("#id_From").val();
    }

    if ($("#id_until").val() != '')
    {
        data_url['until'] = $("#id_until").val();
    }

    var callURL = '';
    if ($("select#id_data_provider").val() != '0')
    {
        callURL = $("select#id_data_provider").val().split('|')[1];
    }
    switch($("select#id_verb").val())
    {
       case '1': data_url['verb'] = 'Identify'; break;
       case '2': data_url['verb'] = 'GetRecord'; break;
       case '3': data_url['verb'] = 'ListRecords'; break;
       case '4': data_url['verb'] = 'ListSets'; break;
       case '5': data_url['verb'] = 'ListIdentifiers'; break;
       case '6': data_url['verb'] = 'ListMetadataFormats'; break;
    }

   $.ajax({
            url : dataGetUrl,
            type : "GET",
            dataType: "json",
            data : {
                url : callURL,
                args_url : JSON.stringify(data_url),
            },
            success: function(data){
                $("#banner_submit_wait").hide(200);
                $("#result").html(data.message);
                $("#downloadXML").show(100);
            },
            complete: function(data){
                $("#submitBtn").removeAttr("disabled");
                $("#banner_submit_wait").hide(200);
            },
            error:function(data){
                $("#banner_submit_wait").hide(200);
                $("#banner_build_errors").show(200);
                $("#build_errors").html(data.responseText);
            }
        });
}