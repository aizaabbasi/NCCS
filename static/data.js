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
        console.log(data)
        // document.write(map.html) 
        var path = "<iframe src=\"{{ url_for('static', filename='map.html') }}\"></iframe> "
        // $("#contactsTable").load(map.html)
        console.log(path)

    });
});