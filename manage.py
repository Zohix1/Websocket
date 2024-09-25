from app import create_app, socketio

app = create_app()

if __name__ == "__main__":

    # 使用Gevent协程的异步并发库，实现高并发Websocket连接
    socketio.run(app, debug=True, host='0.0.0.0', port=8080, server_options={"async_mode": "gevent"})
