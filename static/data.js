// Make image
$("#makeImage").click(function(e) {
    e.preventDefault()
    var partitionSize = 0
    progressbar = `<div class="progress">
    <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:0%">0%</div>
    </div><br>`
    $("#contactsTable").html(progressbar)
    $.get("/getImageSize", function(data, status) {
        // document.write(data)
        partitionSize = data

        $.get("/makeImage", function(data, status) {
            console.log(data)
            // document.write(data)
            // $("#contactsTable").html(data)

            url = 'http://' + document.domain + ':' + location.port
            var socket = io.connect(url);
            socket.on('connect', function() {
                console.log('Websocket connected!');
                socket.emit('getProgress')
                socket.emit('keepalive')
            });

            socket.on('progress', function(msg) {
                console.log(msg.data)
                progressbar = `<div class="progress">
                <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:` + msg.data + `%">` + msg.data + `%</div>
                </div><br>`
                $("#contactsTable").html(progressbar)
                // $('#log').append('<p>Received: ' + msg.data + '</p>');
            });

            
            // $.get("/getProgress", function(data, status) {
            //     console.log(data)
            //     // document.write(data)
            //     $("#contactsTable").html(data)
            // });

            
            

        });
    });
    // $.get("/makeImage", function(data, status) {
    //     console.log(data)
    //     // document.write(data)
    //     $("#contactsTable").html(data)
    // });
});

// Get Contacts
$("#contacts").click(function(e) {
    e.preventDefault()
    $.get("/getContacts", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)
    });
});

// Get SMS
$("#sms").click(function() {
    $.get("/getSMS", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)

    });
});

// Get call logs
$("#call-logs").click(function() {
    $.get("/getLogs", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)

    });
});

// Google Map locations
$("#locations").click(function() {
    $.get("/getLocations", function(data, status) {
        var path = "<iframe src=/static/map.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});

// Whatsapp locations
$("#whatsappLocations").click(function() {
    $.get("/getWhatsappLocations", function(data, status) {
        var path = "<iframe src=/static/WhatsappMap.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});

