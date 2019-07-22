import websocket
import argparse

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print("error = ", error)

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Access token")
    args = parser.parse_args()
    if args.token is not None:
        token = args.token
    else:
        print("access token argument (--token xxx) is required!")
        exit(1)

    websocket.enableTrace(True)
    url = "ws://danilo-robot.herokuapp.com/robot"

    protocol_str = "sec-websocket-protocol: " + token
    ws = websocket.WebSocketApp(url,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        header = [protocol_str])
    ws.run_forever()