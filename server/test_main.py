from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_parse_error_text_passed():
    response = client.post(
        "error_parse",
        json={"error_text": "node:internal/modules/cjs/loader:988\n  \
            throw err;\n  ^\n\nError: Cannot find module '/usr/src/app/web/yarn.js'\n    \
                at Function.Module._resolveFilename (node:internal/modules/cjs/loader:985:15)\n    \
                    at Function.Module._load (node:internal/modules/cjs/loader:833:27)\n    \
                        at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:81:12)\n    \
                            at node:internal/main/run_main_module:22:47 {\n  code: 'MODULE_NOT_FOUND',\n  \
                                requireStack: []\n}"}
    )
    assert response.status_code == 200
    assert response.json() == {
        'result': ['Error: Cannot find module __FILE__', "  code: 'MODULE_NOT_FOUND',"]
        }
