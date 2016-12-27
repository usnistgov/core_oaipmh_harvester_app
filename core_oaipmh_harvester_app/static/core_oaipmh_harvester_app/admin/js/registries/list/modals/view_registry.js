var openViewRegistryModal = function(event) {
    event.preventDefault();

    $("#view-registry-modal-table").html("");
    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    var registryName = $registryRow.find("td:first").text();

    $(".view-registry-name").text(registryName);
    $("#view-registry-modal").modal("show");

    load_view_registry_table(objectID);
}

load_view_registry_table = function(objectID){
    $("#banner_wait").show(200);
	$.ajax({
        url : viewRegistryGetUrl,
        type : "GET",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            $("#banner_wait").hide(200);
            $("#view-registry-modal-table").html(data.template);
        }
    });
}

$('.view-registry-btn').on('click', openViewRegistryModal);
