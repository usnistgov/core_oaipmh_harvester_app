var openAddRegistryModal = function(event) {
    event.preventDefault();

    $("#add-registry-modal").modal("show");
}

clearAddError = function ()
{
    $("#banner_add_errors").hide();
    $("#add-registry-errors").html("");
}

validateAddRegistry = function()
{
    errors = ""
    if ($( "#id_url" ).val().trim() == ""){
        errors += "<li>Please enter a URL.</li>"
    }
    harvest = $( "#id_harvest_rate" ).val();
    if (!(Math.floor(harvest) == harvest && $.isNumeric(harvest) && harvest > 0)){
        errors += "<li>Please enter a positive integer.</li>"
    }
	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_add_errors").html(errors);
		$("#banner_add_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}

var saveRegistry = function(event) {
    clearAddError();
    if(validateAddRegistry())
    {
       $("#banner_add_wait").show(200);
       var formData = new FormData($("#add-registry-form")[0]);
       $.ajax({
            url: addRegistryPostUrl,
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
                $("#banner_add_wait").hide(200);
                $("#form_add_errors").html(data.responseText);
                $("#banner_add_errors").show(200)
            },
        })
        ;
    }
}

$(document).on("click", ".add-registry-btn", openAddRegistryModal);

