# coding: utf-8
"""テスト用の WebSocket Echo サーバー

動かし方::

    pip install tornado
    python wsecho.py
"""

from tornado import (ioloop, web, websocket)
from tornado.options import define, options

class IndexHandler(web.RequestHandler):
    def get(self):
        self.write(self.HTML % {'host': self.request.host})
    HTML = """\
<!doctype html>
<html>
<body>
<script>
var ws = new WebSocket("ws://%(host)s/echo");
ws.onmessage = function (e) {
    console.log("recieved:", e);
    var msg = e.data;
    document.getElementById("recieved").innerHTML += msg + "<br>";
};

function send_message() {
    var msg = document.getElementById("message_to_send").value;
    console.log("sending:", msg);
    ws.send(msg);
    return false;
}
</script>
hello
<div id="recieved"></div>
<form>
<input type="text" name="message" id="message_to_send">
<input type="submit" onclick="return send_message();">
</form>
</body>
</html>
"""


class EchoHandler(websocket.WebSocketHandler):
    def open(self):
        print "opened"

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print "closed."


application = web.Application([
    (r'/echo', EchoHandler),
    (r'/', IndexHandler),
    ])


define("port", 8989, int)

if __name__ == '__main__':
    options.parse_command_line()
    application.listen(options.port)
    loop = ioloop.IOLoop.instance()
    print "Start listening:", options.port
    loop.start()
