from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_parse_error_text_passed() -> None:
    response = client.post(
        "error_parse",
        json={
            "error_text": (
                ' File "./public_html/d.py", line 13, in <module>\n'
                "    app.run(debug=False, host='0.0.0.0', port=80)\n"
                '  File "/usr/local/python/lib/python3.5/site-packages/flask/app.py", line 843, in run\n'
                "    run_simple(host, port, self, **options)\n"
                '  File "/usr/local/python/lib/python3.5/site-packages/werkzeug/serving.py", line 694, in run_simple\n'
                "    inner()\n"
                '  File "/usr/local/python/lib/python3.5/site-packages/werkzeug/serving.py", line 656, in inner\n'
                "    fd=fd)\n"
                '  File "/usr/local/python/lib/python3.5/site-packages/werkzeug/serving.py", line 550, in make_server\n'
                "    passthrough_errors, ssl_context, fd=fd)\n"
                '  File "/usr/local/python/lib/python3.5/site-packages/werkzeug/serving.py", line 464, in __init__\n'
                "    HTTPServer.__init__(self, (host, int(port)), handler)\n"
                '  File "/usr/local/python/lib/python3.5/socketserver.py", line 443, in __init__\n'
                "    self.server_bind()\n"
                '  File "/usr/local/python/lib/python3.5/http/server.py", line 138, in server_bind\n'
                "    socketserver.TCPServer.server_bind(self)\n"
                '  File "/usr/local/python/lib/python3.5/socketserver.py", line 457, in server_bind\n'
                "    self.socket.bind(self.server_address)\n"
                "PermissionError: [Errno 13] Permission denied"
            ),
            "language": 'Python'
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'result': [
            {'row_idx':  1, 'col_idxes': {'start':  7, 'end': 25}, 'text': './public_html/d.py', 'type': 3},
            {'row_idx':  1, 'col_idxes': {'start': 28, 'end': 35}, 'text': 'line 13', 'type': 4},
            {'row_idx':  2, 'col_idxes': {'start':  4, 'end': 49},
             'text': "app.run(debug=False, host='0.0.0.0', port=80)", 'type': 1},
            {'row_idx':  3, 'col_idxes': {'start': 54, 'end': 59}, 'text': 'flask',        'type': 2},
            {'row_idx':  5, 'col_idxes': {'start': 54, 'end': 62}, 'text': 'werkzeug',     'type': 2},
            {'row_idx':  7, 'col_idxes': {'start': 54, 'end': 62}, 'text': 'werkzeug',     'type': 2},
            {'row_idx':  9, 'col_idxes': {'start': 54, 'end': 62}, 'text': 'werkzeug',     'type': 2},
            {'row_idx': 11, 'col_idxes': {'start': 54, 'end': 62}, 'text': 'werkzeug',     'type': 2},
            {'row_idx': 13, 'col_idxes': {'start': 40, 'end': 52}, 'text': 'socketserver', 'type': 2},
            {'row_idx': 15, 'col_idxes': {'start': 40, 'end': 44}, 'text': 'http',         'type': 2},
            {'row_idx': 17, 'col_idxes': {'start': 40, 'end': 52}, 'text': 'socketserver', 'type': 2},
            {'row_idx': 19, 'col_idxes': {'start': 0, 'end': 45},
             'text': 'PermissionError: [Errno 13] Permission denied', 'type': 1},
        ]
    }
