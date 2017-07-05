var emptyEntry = '----------'

/**
 * Populate select
 */
populateSelect = function() {
    // Test if there is some data providers. If not, not need to initiate the process.
    if ($("#id_data_provider").length)
    {
        if ($("select#id_data_provider").val() == '0')
        {
             $("select#id_set").html("<option>"+emptyEntry+'</option>');
             $("select#id_set").attr('disabled', true);
             $("select#id_metadata_prefix").html('<option>'+emptyEntry+'</option>');
             $("select#id_metadata_prefix").attr('disabled', true);
        }
        else
        {
            var id = $("select#id_data_provider").val().split('|')[0];
            $.ajax({
                url : viewAllSetsGetUrl,
                type : "GET",
                dataType: "json",
                data : {
                    "id": id
                },
                success: function(data){
                    var options = '<option value="0">'+emptyEntry+'</option>';
                     for (var i = 0; i < data.length; i++) {
                        options += '<option value="' + data[i]['value'] + '">' + data[i]['key'] + '</option>';
                     }
                     $("select#id_set").attr('disabled', false);
                     $("select#id_set").html(options);
                     $("select#id_set option:first").attr('selected', 'selected');
                },
            });

            $.ajax({
                url : viewAllMetadataFormatsGetUrl,
                type : "GET",
                dataType: "json",
                data : {
                    "id": id
                },
                success: function(data){
                    var options = '<option value="0">'+emptyEntry+'</option>';
                     for (var i = 0; i < data.length; i++) {
                        options += '<option value="' + data[i] + '">' + data[i] + '</option>';
                     }
                     $("select#id_metadata_prefix").attr('disabled', false);
                     $("select#id_metadata_prefix").html(options);
                     $("select#id_metadata_prefix option:first").attr('selected', 'selected');
                },
            });
        }
    }
}