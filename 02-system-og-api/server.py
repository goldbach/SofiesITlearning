"""Et mini-API over HTTP, kun med Pythons standardbibliotek.

Start:  python3 server.py
Stop:   Ctrl-C
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

# Vores "database": data ligger kun i hukommelsen og forsvinder,
# når serveren stoppes. Det ændrer vi på dag 3.
maalinger = {
    1: {"id": 1, "temperatur": 21.3, "tryk": 1013},
    2: {"id": 2, "temperatur": 22.1, "tryk": 1009},
    3: {"id": 3, "temperatur": 19.8, "tryk": 1017},
}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def sti_dele(self):
        # "/maalinger/2?x=1" -> ["maalinger", "2"]
        return urlsplit(self.path).path.strip("/").split("/")

    def do_GET(self):
        dele = self.sti_dele()

        if dele == ["maalinger"]:
            self.send_json(200, list(maalinger.values()))

        elif len(dele) == 2 and dele[0] == "maalinger" and dele[1].isdigit():
            maaling = maalinger.get(int(dele[1]))
            if maaling is None:
                self.send_json(404, {"fejl": f"måling {dele[1]} findes ikke"})
            else:
                self.send_json(200, maaling)

        else:
            self.send_json(404, {"fejl": "ukendt sti"})

    def do_POST(self):
        if self.sti_dele() != ["maalinger"]:
            self.send_json(404, {"fejl": "ukendt sti"})
            return

        laengde = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(laengde))
        except json.JSONDecodeError:
            self.send_json(400, {"fejl": "body er ikke gyldig JSON"})
            return

        if "temperatur" not in data or "tryk" not in data:
            self.send_json(400, {"fejl": "både temperatur og tryk skal med"})
            return

        ny_id = max(maalinger, default=0) + 1
        maaling = {"id": ny_id, "temperatur": data["temperatur"], "tryk": data["tryk"]}
        maalinger[ny_id] = maaling
        self.send_json(201, maaling)


if __name__ == "__main__":
    adresse = ("127.0.0.1", 8000)
    print("Serveren kører på http://127.0.0.1:8000 (stop med Ctrl-C)")
    HTTPServer(adresse, Handler).serve_forever()
