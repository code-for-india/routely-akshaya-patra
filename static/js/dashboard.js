$(function() {

    $(document).ready(function() {
        $.ajax({
            type    : "GET",
            url     : "/data",
            success : function(data) {
                // Handle the data

                // 
                // [ 
                //    [
                //         {
                //             lat : 12,
                //             lon : 34
                //         },
                //         {
                //             lat : 13,
                //             lon : 24
                //         }
                //     ],
                //     [
                //         {
                //             lat : 56,
                //             lon : 78
                //         },
                //         {
                //             lat : 58,
                //             lon : 67
                //         }
                //     ],
                // ],

                // [
                //     [
                //         {
                //             lat : 12,
                //             lon : 34
                //         },
                //         {
                //             lat : 13,
                //             lon : 24
                //         }
                //     ],
                //     [
                //         {
                //             lat : 56,
                //             lon : 78
                //         },
                //         {
                //             lat : 58,
                //             lon : 67
                //         }
                //     ],
                // ]
                // ]

                window.data = data;

                // Stitch number of tabs equal to number of regions
                // var htmlstring = '<ul class="nav nav-tabs">';
                // for (var i = data.length - 1; i >= 0; i--) {
                //     if (i == data.length) {
                //         htmlstring += '<li class="active"><a href="#">R - ' + i + '</a></li>'
                //     }
                //     htmlstring += '<li><a href="#">R - ' + i + '</a></li>';
                // };
                // htmlstring += '</ul>\n'

                // for (var i = data.length - 1; i >= 0; i--) {
                //     htmlstring += <div class="list-group">
                //     for (var j = data[i].length - 1; j >= 0; j--) {
                //         data[i][j]
                //     };
                // };

                var htmlstring = '';
                for (var i = data.length - 1; i >= 0; i--) {
                    for (var j = data[i].length - 1; j >= 0; j--) {
                        htmlstring += '<a href="#" class="list-group-item" id="vehicle-item" data-vehicle="' + i + ',' + j + '">R - ' + i + ' V - ' + j + '</a>'
                    };
                };


  <!-- Tab panes -->
<div class="tab-content">
  <div class="tab-pane active" id="home">...</div>
  <div class="tab-pane" id="profile">...</div>
  <div class="tab-pane" id="messages">...</div>
  <div class="tab-pane" id="settings">...</div>
</div>
            },
            error   : function(error) {
                alert("error! " + error.message);
            }
        });
    });

    $('#vehicle-item').click(function(event) {
        var target = $(event.target);
        var vehicleCode = target.attr('data-vehicle');
        var codes = vehicleCode.split(',');
        for (var i = codes.length - 1; i >= 0; i--) {
            codes[i] = parseInt(codes[i]);
        };

        // Create the tsp object
        tsp = new BpTspSolver(map);
        // Set your preferences
        tsp.setTravelMode(google.maps.DirectionsTravelMode.DRIVING);

        // Add points (by coordinates, or by address).
        // The first point added is the starting location.
        // The last point added is the final destination (in the case of A - Z mode)
        var vehicle_coordinates = data[codes[0]][codes[1]];
        for (var i = vehicle_coordinates.length - 1; i >= 0; i--) {
            tsp.addWaypoint(new google.maps.LatLng(vehicle_coordinates.lat, vehicle_coordinates.lng));
        };


        // tsp.addWaypoint(new google.maps.LatLng(13.1072034, 77.697427), function () { console.log("I am doing awesome")});  // Note: The callback is new for version 3, to ensure waypoints and addresses appear in the order they were added in.
        // tsp.addWaypoint(new google.maps.LatLng(13.1072034, 77.797427), function () { console.log("I am doing really awesome")});
        // tsp.addWaypoint(new google.maps.LatLng(13.1072034, 77.997427), function () { console.log("I am doing shitting awesome")});
        // Or, if you want to start in the first location and end at the last,
        // but don't care about the order of the points in between:
        tsp.solveRoundTrip(function (mytsp) {
            directionsDisplay.setDirections(mytsp.getGDirections());

        });
    });
})();