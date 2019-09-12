import urllib.request
import json
import websocket

def get_state():
    url = 'http://127.0.0.1/signalk/v1/api/vessels/self/navigation/state/value'
    req = urllib.request.Request(url)
    try:
        r = urllib.request.urlopen(req).read()
        cont = json.loads(r.decode('utf-8'))
        return cont
    except:
        return None

def connect(on_message, on_error, on_open):
    ws = websocket.WebSocketApp("ws://127.0.0.1/signalk/v1/stream",
        on_message = on_message,
        on_error = on_error,
        on_open = on_open)
    ws.run_forever()
