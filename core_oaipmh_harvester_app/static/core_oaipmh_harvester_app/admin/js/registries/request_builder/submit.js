/**
* Perform check before submit
*/
checkSubmit = function() {
    let $buildErrors = $("#build_errors");
    let $bannerBuildErrors = $("#banner_build_errors");
    let $result = $("#result");

    $buildErrors.html("");
    $bannerBuildErrors.hide(200);
    $("#download-xml").hide();
    $result.text("");
    $result.hide();

    let label = "";
    let metadataPrefixValue = $("select#id_metadata_prefix").val();
    let identifierValue = $("#id_identifier").val();
    let resumptionTokenValue = $("#id_resumption_token").val();
    let dataProviderValue = $("select#id_data_provider").val();
    let verbValue = $("select#id_verb").val();

    if (dataProviderValue === "0") {
        label = "Please pick a data provider.";
    } else if (verbValue === "0") {
        label = "Please pick a verb.";
    } else {
        if (verbValue === "2") {
            if (metadataPrefixValue === "0") {
                label = "Please pick a metadata prefix.";
            } else if (identifierValue.trim() === "") {
                label = "Please provide an identifier.";
            }
        } else if (verbValue === "3" || verbValue === "5") {
            if (metadataPrefixValue === "0" && resumptionTokenValue === "") {
                label = "Please pick a metadata prefix.";
            }
        }
    }

    if (label === "") {
        submit();
    } else {
        $bannerBuildErrors.show(200);
        $buildErrors.html(label);
    }
};

submit = function() {
    $("#submit-btn").attr("disabled", "disabled");
    $("#banner_submit_wait").show(200);

    let $result = $("#result");
    let requestBuilderArgs = {};
    let setValue = $("select#id_set").val();
    let metadataPrefixValue = $("select#id_metadata_prefix").val();
    let identifierValue = $("#id_identifier").val();
    let resumptionTokenValue = $("#id_resumption_token").val();
    let fromDateValue = $("#id_from_date").val();
    let untilDateValue = $("#id_until_until_date").val();
    let dataProviderValue = $("select#id_data_provider").val();
    let verbValue = $("select#id_verb").val();

    if (setValue !== "0")
        requestBuilderArgs["set"] = setValue;

    if (metadataPrefixValue !== "0")
        requestBuilderArgs["metadataPrefix"] = metadataPrefixValue;

    if (identifierValue !== "")
        requestBuilderArgs["identifier"] = identifierValue;

    if (typeof resumptionTokenValue !== "undefined" &&
        resumptionTokenValue !== "")
        requestBuilderArgs["resumptionToken"] = resumptionTokenValue;

    if (fromDateValue !== "")
        requestBuilderArgs["from"] = fromDateValue;

    if (untilDateValue !== "")
        requestBuilderArgs["until"] = untilDateValue;

    let callURL = "";
    if (dataProviderValue !== "0")
        callURL = dataProviderValue.split("|")[1];

    switch(verbValue)
    {
       case "1": requestBuilderArgs["verb"] = "Identify"; break;
       case "2": requestBuilderArgs["verb"] = "GetRecord"; break;
       case "3": requestBuilderArgs["verb"] = "ListRecords"; break;
       case "4": requestBuilderArgs["verb"] = "ListSets"; break;
       case "5": requestBuilderArgs["verb"] = "ListIdentifiers"; break;
       case "6": requestBuilderArgs["verb"] = "ListMetadataFormats"; break;
    }

    $.ajax({
        url : dataGetUrl,
        type : "GET",
        dataType: "json",
        data : {
            url : callURL,
            args_url : JSON.stringify(requestBuilderArgs),
        },
        success: function(data){
            $("#banner_submit_wait").hide(200);
            $result.html(data.message);
            $result.show();
            $("#download-xml").show(100);
        },
        complete: function(data){
            $("#submit-btn").removeAttr("disabled");
            $("#banner_submit_wait").hide(200);
        },
        error:function(data){
            $("#banner_submit_wait").hide(200);
            $("#banner_build_errors").show(200);
            $("#build_errors").html(data.responseText);
        }
    });
};
