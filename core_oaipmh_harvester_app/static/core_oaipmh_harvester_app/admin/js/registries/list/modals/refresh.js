var refreshTime = 30;

checkInfo = function() {
    $.when(checkUpdateData(), checkHarvestData()).done(function(a1, a2){
        $('#Refreshing').hide();
        $('#RefreshInfo').show();
        refreshInfo(refreshTime);
    });
}

refreshInfo = function(remaining) {
    if(remaining === 0)
    {
        $('#RefreshInfo').hide();
        $('#Refreshing').show();
        checkInfo();
        return;
    }
    $('#countdown').html(remaining);
    setTimeout(function(){ refreshInfo(remaining - 1); }, 1000);
}

$(document).ready(function() {
    //Refresh every refreshTime seconds
    refreshInfo(refreshTime);
});