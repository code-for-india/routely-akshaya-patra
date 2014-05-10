$(function() {
    $('#vehicle-item').click(function(event) {
        var target = $(event.target);
        var vehicleId = target.attr('data-vehicle');
        $.ajax({
            type    : "POST",
            url     : "/vehicle",
            data    : {
                vehicle_id  : vehicleId
            },
            success : function(data) {
                // Handle the data
            },
            error   : function(error) {
                alert("error! " + error.message);
            }
        })
    });
})();