initRequestBuilder = function() {
    initSelects();

    $("select").on("change", function() {
        $("#build_errors").html("");
        $("#banner_build_errors").hide(200);
    });

    $("input").on("change", function() {
        $("#build_errors").html("");
        $("#banner_build_errors").hide(200);
    });

    $("select#id_data_provider").on("change", function() {
        initSelects();
    });

    initDatetimePicker("#id_from_date");
    initDatetimePicker("#id_until_date");
};

/**
 * Init date time picker for specified element id
 */
initDatetimePicker = function(elementId) {
    $(elementId).datetimepicker({
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
    });
};

/**
 * Init selects for request builder form
 */
initSelects = function() {
    let $idDataProvider = $("select#id_data_provider");

    // If there are no data providers, no need to initiate the form.
    if (!$idDataProvider.length)
        return;

    let emptyEntry = "----------";
    let $idSet = $("select#id_set");
    let $idMetadataPrefix = $("select#id_metadata_prefix");

    if ($idDataProvider.val() === "0") {
         $idSet.html("<option>"+emptyEntry+"</option>");
         $idSet.attr("disabled", true);
         $idMetadataPrefix.html("<option>"+emptyEntry+"</option>");
         $idMetadataPrefix.attr("disabled", true);
    } else {  // $idDataProvider.val() !== "0"
        let dataProviderId = $idDataProvider.val().split("|")[0];

        $.ajax({
            url : viewAllSetsGetUrl,
            type : "GET",
            dataType: "json",
            data : {
                "id": dataProviderId
            },
            success: function(data){
                let options = "<option value='0'>"+emptyEntry+"</option>";

                for (let i = 0; i < data.length; i++) {
                    options += "<option value='" + data[i]["value"] + "'>"
                        + data[i]["key"] + "</option>";
                }

                $idSet.attr("disabled", false);
                $idSet.html(options);

                $("select#id_set option:first").attr("selected", "selected");
            },
        });

        $.ajax({
            url : viewAllMetadataFormatsGetUrl,
            type : "GET",
            dataType: "json",
            data : {
                "id": dataProviderId
            },
            success: function(data){
                let options = "<option value='0'>"+emptyEntry+"</option>";
                for (let i = 0; i < data.length; i++) {
                    options += "<option value='" + data[i] + "'>" + data[i] +
                        "</option>";
                }
                $idMetadataPrefix.attr("disabled", false);
                $idMetadataPrefix.html(options);
                $("select#id_metadata_prefix option:first").attr(
                    "selected", "selected"
                );
            },
        });
    }
};

$(document).ready(function() {
    initRequestBuilder();
});
