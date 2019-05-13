$(document).ready(function () {
    $("#table_div").hide() 
});

// Make image
$("#makeImage").click(function(e) {
    e.preventDefault()
    $("#table_div").hide()
    var partitionSize = 0
    progressbar = `<div class="progress">
    <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:0%; color: black;">0%</div>
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
            });

            var progress = 0.0
            socket.on('progress', function(msg) {
                progress = msg.data
                progress = parseFloat(progress)
                console.log(progress)
                progressbar = `<div class="progress">
                <div class="progress-bar bg-info progress-bar-striped progress-bar-animated" style="width:` + msg.data + `%; color: black;">` + msg.data + `%</div>
                </div><br>`
                $("#contactsTable").html(progressbar)
                if (progress >= 100)
                {
                    socket.disconnect();    // Disconnect socket
                }
                else
                {
                    socket.emit('getProgress')
                }
            });     
            

        });
    });
});

// Mount image
$("#mountImage").click(function(e) {
    e.preventDefault()
    $("#table_div").hide()
    // Mount image
    $.get("/mountImage", function(data, status) {
        console.log(data)
        $("#contactsTable").html('<h2>Done</h2>')
    });
});

// Get Contacts
$("#contacts").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getContacts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});

// Get SMS
$("#sms").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getSMS", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)

    });
});

// Get call logs
$("#call-logs").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getLogs", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)

    });
});

// Google Map locations
$("#locations").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getLocations", function(data, status) {
        var path = "<iframe src=/static/map.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});

// Whatsapp locations
$("#whatsappLocations").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getWhatsappLocations", function(data, status) {
        var path = "<iframe src=/static/WhatsappMap.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});
// Facebook Profile
$("#facebookprofile").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getFacebookUserName", function(data, status) {
        console.log(data);
        window.open(data, '_blank');        
    });
});

// Facebook Contacts
$("#facebookcontacts").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getFacebookContacts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
      
        
    });
});

// Whatsapp Contacts
$("#whatsappcontacts").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getWhatsappContacts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});

// Whatsapp Chat
$("#whatsappmessages").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getWhatsappMessages", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});

// Whatsapp Groups 
$("#whatsappgroups").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getWhatsappGroups", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)

    });
});

// Synced Accounts 
$("#syncaccounts").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $.get("/getSyncedAccounts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
        
    });
});

// Device Info 
$("#deviceinfo").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getDeviceInfo", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
      
        
    });
});

// Audio Files 
$("#audio").click(function(e) {                          // Click handler for audio button
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").html("")
    $("#table_div").show()
    $.get("/getAudioFiles", function(data, status) {    // Send GET request to 'getAudioFiles' URL
        $("#contactsTable").html("")
        // Graph
        var path = "<center><iframe src=/static/graphs/audio.png style=\"width:100%; height:500px\"></iframe></center>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
        $("#table_div").append("<thead> <tr> <th> File </th> </tr> </thead>")
        for (i=0; i<data.length; i++)
        {
            var temp = encodeURI(data[i])
            path = "<a href= " + temp + ">" + data[i] + "</a>"
            $("#table_div").append("<tr><td>" + path + "</td></tr>");
        }

    });
});


// Video Files 
$("#video").click(function(e) {                          // Click handler for audio button
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").html("")
    $("#table_div").show()
    $.get("/getVideoFiles", function(data, status) {    // Send GET request to 'getVideoFiles' URL
        $("#contactsTable").html("")
        // Graph
        var path = "<center><iframe src=/static/graphs/videos.png style=\"width:100%; height:500px\"></iframe></center>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
        $("#table_div").append("<thead> <tr> <th> File </th> </tr> </thead>")
        // console.log(data)
        for (i=0; i<data.length; i++)
        {
            var temp = encodeURI(data[i])
            path = "<a href= " + temp + ">" + data[i] + "</a>"
            $("#table_div").append("<tr><td>" + path + "</td></tr>");
        }

    });
});
// Documents 
$("#documents").click(function(e) {                          // Click handler for audio button
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").html("")
    $("#table_div").show()
    $.get("/getDocuments", function(data, status) {    // Send GET request to 'getDocuments' URL
        $("#contactsTable").html("")
        // Graph
        var path = "<center><iframe src=/static/graphs/documents.png style=\"width:100%; height:500px\"></iframe></center>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
        $("#table_div").append("<thead> <tr> <th> File </th> </tr> </thead>")
        // console.log(data)
        for (i=0; i<data.length; i++)
        {
            var temp = encodeURI(data[i])
            path = "<a href= " + temp + ">" + data[i] + "</a>"
            $("#table_div").append("<tr><td>" + path + "</td></tr>");
        }

    });
});


// Pictures 
$("#pictures").click(function(e) {                          // Click handler for audio button
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").html("")
    $("#table_div").show()
    $.get("/getPictures", function(data, status) {    // Send GET request to 'getPictures' URL
        $("#contactsTable").html("")
        // Graph
        var path = "<center><iframe src=/static/graphs/pictures.png style=\"width:100%; height:500px\"></iframe></center>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
        $("#table_div").append("<thead> <tr> <th> File </th> </tr> </thead>")
        for (i=0; i<data.length; i++)
        {
            var temp = encodeURI(data[i])
            path = "<a href= " + temp + ">" + data[i] + "</a>"
            $("#table_div").append("<tr><td>" + path + "</td></tr>");
        }
    });
});

// Get Skype Contacts
$("#skypeContacts").click(function(e) {
    e.preventDefault()
    $("#table_div").hide()
    $.get("/getSkypeContacts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});

// Chrome Bookmarks 
$("#bookmarks").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getChromeBookmarks", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)

    });
});

// Login Data 
$("#login").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getChromeLogin", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)

    });
});
// Chrome Browser History 
$("#history").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getChromeHistory", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)

    });
});

// Chrome Web Data 
$("#webdata").click(function(e) {
    e.preventDefault()          // Prevents going to top of the page
    $("#table_div").hide()
    $.get("/getChromeWebData", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});



// Get Skype Messages
$("#skypeMessages").click(function(e) {
    e.preventDefault()
    $("#table_div").hide()
    $.get("/getSkypeMessages", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)

    });
});

// GPS from Exif
$("#imagelocations").click(function() {
    $("#table_div").hide()
    $.get("/getImageLocations", function(data, status) {
        var path = "<iframe src=/static/ImagesMap.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});


// metadata from Exif 
$("#metadata").click(function() {
    $("#table_div").html("")
    $("#table_div").show()
    $.get("/getMetadata", function(data, status) {    // Send GET request to 'getMetadata' URL
        $("#contactsTable").html("")
    });
});
