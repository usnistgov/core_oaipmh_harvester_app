/**
 * Activate a registry
 */
activate_registry = function(event){
    event.preventDefault();
    var $registryRow = $(this).parent().parent();
    $.ajax({
        url : activateRegistryGetUrl,
        type : "GET",
        data: {
            "id": $registryRow.attr("objectid")
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).ready(function() {
    $('.activate-registry-btn').on('click', activate_registry);
});