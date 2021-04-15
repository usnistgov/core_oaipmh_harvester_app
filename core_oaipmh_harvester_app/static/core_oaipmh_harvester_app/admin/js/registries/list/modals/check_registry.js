/**
 * Check the availability of a registry
 */
checkStatus = function(event)
{
    event.preventDefault();

    var $registryTd = $(this).parent();
    var $registryRow = $(this).parent().parent();
    var url = $registryRow.attr("url");

    $registryTd.html('<i class="fas fa-spinner fa-spin"></i>');

    $.ajax({
        url : checkRegistryGetUrl,
        type : "GET",
        dataType: "json",
        async: true,
        data : {
        	url : url,
        },
        success: function(data){
            if (data.is_available)
            {
                $registryTd.html('<i class="fas fa-signal"></i> Available');
                $registryTd.css("color", "#5cb85c");
            }
            else {
                $registryTd.html('<i class="fas fa-signal"></i> Unavailable');
                $registryTd.css("color", "#d9534f");
            }
        },
        error:function(data){
            $registryTd.html('<i class="fas fa-warning"></i> Error while checking');
            $registryTd.css("color", "#d9534f");
        },
    });
}

checkAllStatus = function(event)
{
    $('.check-registry-btn').click();
}

$(document).ready(function() {
    $('.check-registry-btn').on('click', checkStatus);
    $('.check-all-registries-btn').on('click', checkAllStatus);
});