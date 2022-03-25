from web_app import create_app, socketio

app = create_app()

def run_server(*args, **kwargs):
    socketio.run(app)

if __name__ == '__main__':
    socketio.run(app)
