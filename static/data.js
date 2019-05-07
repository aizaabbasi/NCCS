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
    // $.get("/makeImage", function(data, status) {
    //     console.log(data)
    //     // document.write(data)
    //     $("#contactsTable").html(data)
    // });
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
    e.preventDefault()
    $("#table_div").hide()
    $.get("/getContacts", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)
    });
});

// Get SMS
$("#sms").click(function() {
    $("#table_div").hide()
    $.get("/getSMS", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)

    });
});

// Get call logs
$("#call-logs").click(function() {
    $("#table_div").hide()
    $.get("/getLogs", function(data, status) {
        console.log(data)
        // document.write(data)
        $("#contactsTable").html(data)

    });
});

// Google Map locations
$("#locations").click(function() {
    $("#table_div").hide()
    $.get("/getLocations", function(data, status) {
        var path = "<iframe src=/static/map.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});

// Whatsapp locations
$("#whatsappLocations").click(function() {
    $("#table_div").hide()
    $.get("/getWhatsappLocations", function(data, status) {
        var path = "<iframe src=/static/WhatsappMap.html style=\"width:100%; height:500px\"></iframe>"
        path = path.replace(/[^\x20-\x7E]/g, '');
        console.log(path)
        $("#contactsTable").html(path)
    });
});
// Facebook Profile
$("#facebookprofile").click(function() {
    $("#table_div").hide()
    $.get("/getFacebookUserName", function(data, status) {
        console.log(data);
        window.open(data, '_blank');        
    });
});

// Facebook Contacts
$("#facebookcontacts").click(function() {
    $("#table_div").hide()
    $.get("/getFacebookContacts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
      
        
    });
});

// Whatsapp Contacts
$("#whatsappcontacts").click(function() {
    $("#table_div").hide()
    $.get("/getWhatsappContacts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});

// Whatsapp Chat
$("#whatsappmessages").click(function() {
    $("#table_div").hide()
    $.get("/getWhatsappMessages", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
    });
});

// Whatsapp Groups 
$("#whatsappgroups").click(function() {
    $("#table_div").hide()
    $.get("/getWhatsappGroups", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)

    });
});

// Synced Accounts 
$("#syncaccounts").click(function() {
    $.get("/getSyncedAccounts", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
            
    //     var tbl=$("<table/>").attr("id","mytable");
    //     $("#div1").append(tbl);
    //     for(var i=0;i<data.length;i++)
    //     {
    //         var tr="<tr>";
    //         var td1="<td>"+data[i]+"</td>";


    //     $("#contactsTable").append(tr+td1); 

    // }   
      
        
    });
});

// Device Info 
$("#deviceinfo").click(function() {
    $("#table_div").hide()
    $.get("/getDeviceInfo", function(data, status) {
        console.log(data)
        $("#contactsTable").html(data)
      
        
    });
});

// Audio Files 
$("#audio").click(function() {                          // Click handler for audio button
    $("#table_div").show()
    $.get("/getAudioFiles", function(data, status) {    // Send GET request to 'getAudioFiles' URL
        $("#contactsTable").html("")
        // $("#contactsTable").append('<table class="table table-striped">')
        // $("#contactsTable").append("<thead> <tr> <th> File </th> </tr> </thead>")
        // $("#contactsTable").append("<tbody>")
        // console.log(data)
        for (i=0; i<data.length; i++)
        {
            var temp = encodeURI(data[i])
            path = "<a href= " + temp + ">" + data[i] + "</a>"
            $("#table_div").append("<tr><td>" + path + "</td></tr>");
            // div = document.getElementById("contactsTable")
            // $("#contactsTable").append("<tr>")
            // $("#contactsTable").append("<td>")
            // // div.insertAdjacentHTML( 'beforeend', path );
            // $("#contactsTable").append(path)
            // $("#contactsTable").append("</td>")
            // $("#contactsTable").append("</tr>")
        }
        // $("#contactsTable").append("</tbody>")
        // $("#contactsTable").append("</table>")

    });
});