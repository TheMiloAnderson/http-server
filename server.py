from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json

class OkRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('do_GET')
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
        # import pdb; pdb.set_trace()
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        print('path', parsed_path.path)

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.format(' ').encode())

        elif parsed_path.path == '/cows':
            print('got /cows')
            bun = cow.Bunny()

            try:
                msg = bun.milk(parsed_qs['msg'][0])

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.format(msg).encode())
            except:
                print('400 Bad Request.')
                self.send_response_only(400)
                self.end_headers()
        else:
            print('404 Not Found.')
            self.send_response_only(404)
            self.end_headers()


    def do_POST(self):

        cont_len = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(cont_len).decode()
        tmp_array = post_data.split("=")
        tmp_list = tmp_array[1].split("+")

        post_data = ""
        for i in range(len(tmp_list)):
            post_data += tmp_list[i] + " "

        parsed_path = urlparse(self.path)

        # if parsed_path.path == '/cows':
        if parsed_path.path :
            bun = cow.Bunny()
            msg = bun.milk(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            reply = json.dumps(msg)
            self.wfile.write(reply.encode())
        # except:
        #     print('404 Not found.')

if __name__ == '__main__':
    server_addr = ('', 5000)
    server = HTTPServer(server_addr, OkRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
