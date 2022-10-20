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
        'result': ['http', 'socketserver', 'flask', 'werkzeug', 'PermissionError: [Errno 13] Permission denied']
    }
