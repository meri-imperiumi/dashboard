import urllib.request
import json
import websocket
from config import signalk_host, signalk_port

def get_state():
    url = 'http://{}:{}/signalk/v1/api/vessels/self/navigation/state/value'.format(signalk_host, signalk_port)
    req = urllib.request.Request(url)
    try:
        r = urllib.request.urlopen(req).read()
        cont = json.loads(r.decode('utf-8'))
        print("Initial state {}".format(cont))
        return cont
    except:
        return None

def connect(on_message, on_error, on_open):
    url = 'ws://{}:{}/signalk/v1/stream?subscribe=none'.format(signalk_host, signalk_port)
    print(url)
    ws = websocket.WebSocketApp(url,
        on_message = on_message,
        on_error = on_error,
        on_open = on_open)
    ws.run_forever()

def subscribe(ws, paths):
    # First unsubscribe from previous
    ws.send(json.dumps({
        'context': '*',
        'unsubscribe': [
            {
                'path': '*'
            }
        ]
    }))
    # Then subscribe to feed
    subscribes = []
    for path in paths:
        subscribes.append({
            'path': path,
            'period': 3000,
            'format': 'delta',
            'policy': 'fixed'
        })

    ws.send(json.dumps({
         'context': 'vessels.self',
         'subscribe': subscribes
     }))
