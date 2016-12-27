/**
 * Disable a template
 */
deleteRegistry = function(event)
{
    event.preventDefault();

    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    var registryName = $registryRow.find("td:first").text();

    $(".delete-registry-name").text(registryName);
    $("#delete-registry-id").val(objectID);
    $("#delete-registry-modal").modal("show");
}

/**
 * AJAX call, delete a template
 * @param objectID id of the object
 */
delete_registry = function(event){
    event.preventDefault();

    $.ajax({
        url : deleteRegistryGetUrl,
        type : "GET",
        data: {
            "id": $("#delete-registry-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.delete-registry-btn').on('click', deleteRegistry);
    $('#delete-registry-yes').on('click', delete_registry);
});