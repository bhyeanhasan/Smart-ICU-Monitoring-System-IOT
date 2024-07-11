import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Client connected")
        self.write_message("Welcome to the WebSocket server!")

    def on_message(self, message):
        print(f"Received message: {message}")
        self.write_message(f"Server received: {message}")

    def on_close(self):
        print("Client disconnected")

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    print("WebSocket server is running on ws://0.0.0.0:8080/websocket")
    tornado.ioloop.IOLoop.current().start()
