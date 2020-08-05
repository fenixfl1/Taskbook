from pyngrok import ngrok
import os
import sys
from runserver import app

app.config.from_mapping(
    BASE_URL='http://localhost:5000',
    USE_NGROK=os.environ.get('USE_NGROK', 'False') == 'True'
)

port = sys.argv[sys.argv.index('--port') + 1] \
    if '--port' in sys.argv else 5000

public_url = ngrok.connect(port)
print(' * ngrok tunnel \'{}\' -> \'http://127.0.0.1:{}/\''.
      format(public_url, port))

app.config['BASE_URL'] = public_url
