var openEditRegistryModal = function(event) {
    event.preventDefault();

    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    var registryName = $registryRow.find("td:first").text();

    $(".edit-registry-name").text(registryName);
    $("#edit-registry-modal").modal("show");

    load_edit_registry_form(objectID);
}

load_edit_registry_form = function(objectID){
	$.ajax({
        url : editRegistryGetPostUrl,
        type : "GET",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            $("#edit-registry-modal-form").html(data.template);
        }
    });
}

clearEditError = function ()
{
    $("#banner_edit_errors").hide()
    $("#form_edit_errors").html("");
}

validateEditRegistry = function()
{
    errors = ""
    harvest = $( "#id_harvest_rate" ).val();
    if (!(Math.floor(harvest) == harvest && $.isNumeric(harvest) && harvest > 0)){
        errors += "<li>Please enter a positive integer.</li>"
    }
	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_edit_errors").html(errors);
		$("#banner_edit_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}

var editRegistry = function(event) {
    clearEditError();
    if(validateEditRegistry())
    {
       var formData = new FormData($("#edit-registry-form")[0]);
       $.ajax({
            url: editRegistryGetPostUrl,
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            async:true,
            success: function(data){
                window.location = indexRegistryUrl
            },
            error:function(data){
                $("#form_edit_errors").html(data.responseText);
                $("#banner_edit_errors").show(200)
            },
        })
        ;
    }
}

$(".edit-registry-btn").on('click', openEditRegistryModal);
