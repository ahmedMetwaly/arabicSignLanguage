web: gunicorn signsToApp:app --worker-connections 500 -w 1 --preload --backlog 128 -k eventlet --log-file -
