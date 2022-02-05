import urllib.request
import json
import websocket
import threading
import logging
from config import signalk_host, signalk_port

logger = logging.getLogger(__name__)

def get_state():
    url = 'http://{}:{}/signalk/v1/api/vessels/self/navigation/state/value'.format(signalk_host, signalk_port)
    req = urllib.request.Request(url)
    try:
        r = urllib.request.urlopen(req).read()
        cont = json.loads(r.decode('utf-8'))
        logger.debug("Initial state {}".format(cont))
        return cont
    except:
        return None

def connect(on_message, on_error, on_open, on_close):
    url = 'ws://{}:{}/signalk/v1/stream?subscribe=none'.format(signalk_host, signalk_port)
    ws = websocket.WebSocketApp(url,
        on_message = on_message,
        on_error = on_error,
        on_open = on_open,
        on_close = on_close)
    wst = threading.Thread(target=ws.run_forever)
    wst.start()

def subscribe(ws, pathlist):
    # First unsubscribe from previous
    ws.send(json.dumps({
        'context': '*',
        'unsubscribe': [
            {
                'path': '*'
            }
        ]
    }))
    logger.debug('Subscribe: To start subscribe')
    # Then subscribe to feed
    subscribes = []
    
    for path in pathlist:
        subscribes.append({
            'path': str(path),
            'period': 3000,
            'format': 'delta',
            'policy': 'fixed'
        })

    ws.send(json.dumps({
         'context': 'vessels.self',
         'subscribe': subscribes
     }))
