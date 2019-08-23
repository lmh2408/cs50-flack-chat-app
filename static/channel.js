document.addEventListener("DOMContentLoaded", function()
{
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on("connect", function()
    {
        socket.emit("joinchannel", {"channel_name": );

        document.querySelector("#send_message").onsubmit = function(){
            // take input
            const message = document.querySelector("#message_text").value;

            // send input
            socket.emit("get_message", {"message": message});
        };
    });
});
