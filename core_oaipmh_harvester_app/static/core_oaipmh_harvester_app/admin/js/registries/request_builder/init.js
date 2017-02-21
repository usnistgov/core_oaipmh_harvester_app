InitBuildRequest = function(){
    populateSelect();
    $("select").on('change', function() {
      $("#build_errors").html("");
      $("#banner_build_errors").hide(200);
    });
    $("input").on('change', function() {
      $("#build_errors").html("");
      $("#banner_build_errors").hide(200);
    });

    $("select#id_data_provider").on('change', function() {
      populateSelect();
    });

    InitDatetimePicker('#id_until');
    InitDatetimePicker('#id_From');
}

InitDatetimePicker = function(object_id) {
    $(object_id).datetimepicker({
        weekStart: 1,
        todayBtn:  1,
		autoclose: 1,
		todayHighlight: 1,
		startView: 2,
		forceParse: 0,
        showMeridian: 1
    });
}

$(document).ready(function() {
    //Refresh every refreshTime seconds
    InitBuildRequest();
});
