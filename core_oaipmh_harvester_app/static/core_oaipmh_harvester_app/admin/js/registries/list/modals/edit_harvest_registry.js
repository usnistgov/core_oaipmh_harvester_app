var openEditHarvestRegistryModal = function(event) {
    event.preventDefault();

    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    var registryName = $registryRow.find("td:first").text();

    $("#edit-harvest-registry-modal-form").html("");
    $(".edit-harvest-registry-name").text(registryName);
    $("#edit-harvest-registry-modal").modal("show");

    load_edit_harvest_registry_form(objectID);
}

load_edit_harvest_registry_form = function(objectID){
    $("#banner_edit_harvest_wait").show(200);
	$.ajax({
        url : editHarvestRegistryGetPostUrl,
        type : "GET",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            $("#banner_edit_harvest_wait").hide(200);
            $("#edit-harvest-registry-modal-form").html(data.template);
        }
    });
}

var editHarvestRegistry = function(event) {
   var formData = new FormData($("#edit-harvest-registry-form")[0]);
   $.ajax({
        url: editHarvestRegistryGetPostUrl,
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
            $("#form_edit_harvest_errors").html(data.responseText);
            $("#banner_edit_harvest_errors").show(200)
        },
    })
    ;
}

$(".edit-harvest-registry-btn").on('click', openEditHarvestRegistryModal);

