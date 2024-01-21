if __name__ == '__main__':
    from scripts.modules.flask_rest import flask_app
    from scripts.modules.websockets import websockets_app

    flask_app.run_defaut_ssl_app()
    websockets_app.run_async_ws()
