// Get Contacts
$("#contacts").click(function() {
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

// Map locations
$("#locations").click(function() {
    $.get("/getLocations", function(data, status) {
        var path = "<iframe src=/static/map.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});