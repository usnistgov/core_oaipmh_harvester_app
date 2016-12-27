harvestRegistry = function(event)
{
    event.preventDefault();

    var $registryRow = $(this).parent().parent();
    var objectID = $registryRow.attr("objectid");
    $("#bannerHarvest"+objectID).show(200);
    $("#harvest"+objectID).hide(200);

    $.ajax({
        url : harvestRegistryGetUrl,
        type : "GET",
        dataType: "json",
        async: true,
        data : {
        	id : objectID,
        },
        success: function(data){
            checkHarvestData();
        },
        error:function(data){

        },
    });
}

checkHarvestData = function()
{
    return $.ajax({
        url : checkHarvestRegistryGetUrl,
        type : "GET",
        dataType: "json",
        async: true,
        data : {
        },
        success: function(data){
            $.map(data, function (item) {
                if(item.is_harvesting)
                {
                    $("#harvest" + item.registry_id).hide(200);
                    $("#bannerHarvest"+ item.registry_id).show(200);
                }
                else
                {
                    $("#bannerHarvest"+ item.registry_id).hide(200);
                    $("#harvest" + item.registry_id).show(200);
                    $("#name"+ item.registry_id).html(item.name);
                }
             });
        },
        error:function(data){
	    }
    });
}

harvestAllRegistries = function(event)
{
    $('.harvest-registry-btn').click();
}

$(document).ready(function() {
    $('.harvest-registry-btn').on('click', harvestRegistry);
    $('.harvest-all-registries-btn').on('click', harvestAllRegistries);
});