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
 * Build a jQuery collection of <option> elements from a data array.
 * toOption(item) must return {value, text} for each item.
 */
buildOptionList = function(data, toOption) {
    let $optionList = $();

    for (let i = 0; i < data.length; i++) {
        let option = toOption(data[i]);
        $optionList = $optionList.add(
            $("<option>").val(option.value).text(option.text)
        );
    }

    return $optionList;
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
                let $optionList = $("<option>").val("0").text(emptyEntry).add(
                    buildOptionList(data, function(item) {
                        return {value: item["value"], text: item["key"]};
                    })
                );

                $idSet.attr("disabled", false);
                $idSet.empty().append($optionList);

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
                let $optionList = $("<option>").val("0").text(emptyEntry).add(
                    buildOptionList(data, function(item) {
                        return {value: item, text: item};
                    })
                );

                $idMetadataPrefix.attr("disabled", false);
                $idMetadataPrefix.empty().append($optionList);
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
