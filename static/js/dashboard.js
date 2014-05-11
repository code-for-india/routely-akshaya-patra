

    $(document).ready(function() {

        $.ajax({
            type    : "GET",
            url     : "/data",
            success : function(data) {
                // Handle the data
                   console.log("Doing some thniing");
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

                window.data = JSON.parse(data);

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
                for (var i = 0; i < data.length; i++) {
                    for (var j = 0; j < data[i].length; j++) {
                        htmlstring += '<a href="#" onclick="clickhandler(event)" class="list-group-item" id="vehicle-item" data-vehicle="' + j + "," + i + '">R - ' + j + ' V - ' + i + '</a>';
                    };
                };

                $(".list-group").append(htmlstring);




            },
            error   : function(error) {
                alert("error! " + error.message);
            }
        });
    });
    function clickhandler(event) {
                       console.log("Hello")
                        var target = event.target;
                        var vehicleCode = target.getAttribute('data-vehicle');
                        var codes = vehicleCode.split(',');
                        for (var i = 0; i < codes.length; i++) {
                            codes[i] = parseInt(codes[i]);
                        };
                        console.log(codes);
// Get the HTML DOM element that will contain your map
                // We are using a div with id="map" seen below in the <body>

                        tsp.startOver();
                        // Set your preferences
                        tsp.setTravelMode(google.maps.DirectionsTravelMode.DRIVING);

                        // Add points (by coordinates, or by address).
                        // The first point added is the starting location.
                        // The last point added is the final destination (in the case of A - Z mode)
                        var origin = new google.maps.LatLng(12.9261416, 77.5975514);
                        tsp.addWaypoint(origin)
                        var vehicle_coordinates = data[codes[0]][codes[1]];
                        console.log(JSON.stringify(vehicle_coordinates));
                        for (var i = 0; i < vehicle_coordinates.length; i++) {
                            console.log(vehicle_coordinates.lat)
                            tsp.addWaypoint(new google.maps.LatLng(vehicle_coordinates[i].lat, vehicle_coordinates[i].lng));
                        };


                        // tsp.addWaypoint(new google.maps.LatLng(13.1072034, 77.697427), function () { console.log("I am doing awesome")});  // Note: The callback is new for version 3, to ensure waypoints and addresses appear in the order they were added in.
                        // tsp.addWaypoint(new google.maps.LatLng(13.1072034, 77.797427), function () { console.log("I am doing really awesome")});
                        // tsp.addWaypoint(new google.maps.LatLng(13.1072034, 77.997427), function () { console.log("I am doing shitting awesome")});
                        // Or, if you want to start in the first location and end at the last,
                        // but don't care about the order of the points in between:
                        tsp.solveRoundTrip(function (mytsp) {
                            directionsDisplay.setDirections(mytsp.getGDirections());

                        });
                    }
    ;

