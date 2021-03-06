from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json


class OkRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>cowpy</title>
                </head>
                <body>
                    <nav>
                        <a href="/cow">cowsay</a>
                    </nav>
                    <main style="white-space: pre-wrap;">
                    {}
                    </main>
                </body>
                </html>
                """
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.format(' ').encode())

        elif parsed_path.path == '/cows':
            if 'msg' in parsed_qs.keys():
                bun = cow.Bunny()
                msg = bun.milk(parsed_qs['msg'][0])

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.format(msg).encode())
            else:
                self.send_error(400)
        else:
            self.send_error(404)

    def do_POST(self):
        #import pdb; pdb.set_trace()
        cont_len = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(cont_len).decode()
        print(post_data)
        """         tmp_array = post_data.split("=")
        tmp_list = tmp_array[1].split("+")

        post_data = ""
        for i in range(len(tmp_list)):
            post_data += tmp_list[i] + " " """

        parsed_path = urlparse(self.path)

        if parsed_path.path == '/cows':
            if post_data.startswith('msg'):
                bun = cow.Bunny()
                msg = bun.milk('post_data')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                reply = json.dumps(msg)
                self.wfile.write(reply.encode())
            else:
                self.send_error(400)
        else:
            self.send_error(404)


if __name__ == '__main__':
    server_addr = ('', 5000)
    server = HTTPServer(server_addr, OkRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
