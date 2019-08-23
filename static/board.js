document.addEventListener("DOMContentLoaded", function()
{
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // send #new-channel
    socket.on("connect", function()
    {
        // send new channel name
        document.querySelector("#create_channel").onsubmit = function()
        {
            var new_channel = document.querySelector("#new_channel").value;
            socket.emit("add_channel", {"new_channel": new_channel});
            document.querySelector("#new_channel").value = "";
            return false;
        };

        // request display channel
        socket.emit("display_channel");
    });

    // display response when adding channel
    socket.on("add_channel_response", function(data)
    {
        console.log(data);
        if (data["add_success"] == false)
        {
            document.querySelector("#create_error").innerHTML =
                `<div class="row justify-content-center my-1">
                    <div class="col-10 text-center">
                        <span class="text-danger">Channel name is either empty or already exists</span>
                    </div>
                </div>`;

            setTimeout(function()
            {
                document.querySelector("#create_error").innerHTML = "";
            }, 5000);
        }
        else
        {
            document.querySelector("#create_error").innerHTML =
                `<div class="row justify-content-center my-1">
                    <div class="col-10 text-center">
                        <span class="text-success">Channel "${data["added_channel"]}" created</span>
                    </div>
                </div>`;

            setTimeout(function()
            {
                document.querySelector("#create_error").innerHTML = "";
            }, 5000);
        }
    });

    // display a list of channel
    socket.on("channels_list", function(data)
    {
        console.log(data);

        // merge local list with new list
        var display = document.querySelector("#channel_list");
        display.innerHTML = "";
        for (let i = 0, l = data.length; i < l; i++)
        {
            // add item to display
            display.insertAdjacentHTML("afterbegin",
            `
                <div class="row justify-content-center mb-3">
                    <div class="col-8 col-md-5 border rounded bg-light shadow text-center p-3">
                        <a href="/channel/${data[i]}"><span>${data[i]}</span></a>
                    </div>
                </div>
            `);
        }
    });
});
