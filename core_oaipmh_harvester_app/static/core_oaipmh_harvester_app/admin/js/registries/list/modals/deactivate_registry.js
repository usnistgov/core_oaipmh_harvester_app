/**
 * Disable a template
 */
deactivateRegistry = function(event)
{
    event.preventDefault();

    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    var registryName = $registryRow.find("td:first").text();

    $(".deactivate-registry-name").text(registryName);
    $("#deactivate-registry-id").val(objectID);
    $("#deactivate-registry-modal").modal("show");
}

/**
 * AJAX call, delete a template
 * @param objectID id of the object
 */
deactivate_registry = function(event){
    event.preventDefault();

    $.ajax({
        url : deactivateRegistryGetUrl,
        type : "GET",
        data: {
            "id": $("#deactivate-registry-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.deactivate-registry-btn').on('click', deactivateRegistry);
    $('#deactivate-registry-yes').on('click', deactivate_registry);
});