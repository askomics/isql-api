from isqlapi import app, IsqlApi

if __name__ == "__main__":
    api = IsqlApi()
    app.run(port=api.port)
