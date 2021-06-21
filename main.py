import http.server
import re
import socketserver
import sys
import requests
import getopt
from lxml import html

port = 8000
domain = 'https://habr.com'


def run_server():
    with socketserver.TCPServer(('', port), ProxyHandler) as httpd:
        print(f'Server started on port {port}')
        print(f'Proxying from {domain}')
        httpd.serve_forever()


class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        request_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                           'Accept-Encoding': 'gzip, deflate',
                           'Accept-Language': 'ru-RU,en;q=0.5',
                           'Connection': 'keep-alive',
                           'Cookie': ''}
        for header, value in request_headers.items():
            request_header = self.headers.get(header)
            if request_header:
                request_headers[header] = request_header

        response_headers = {'Content-Type': 'text/html; charset=UTF-8'}
        try:
            response = requests.get(domain + self.path, headers=request_headers)
            status_code = response.status_code
            content = response.content
            if response.headers.get('Content-Type', '').startswith('text/html'):
                content = bytes(modify_page(content), 'utf-8')

            for header, value in response_headers.items():
                if header in response.headers.keys() and response.headers[header]:
                    response_headers[header] = response.headers[header]
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            status_code = 500
            content = b'<h1>Error from the source server</h1>'

        self.send_response(status_code)
        for header, value in response_headers.items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(content)


def modify_page(page):
    pattern = re.compile(r"(?!(([^<]+)?>))(?<!([{.\']))(\b\w{6}\b)")
    page = html.fromstring(page)
    body = page.find('body')
    for tag in body.iter():
        if tag.tag == 'a':
            old_url = tag.attrib.get('href', '')
            tag.attrib['href'] = old_url.replace(domain, '')
        elif tag.tag in ('script', 'style', 'meta', 'link'):
            continue

        if tag.text:
            tag.text = pattern.sub(r'\1\2\3\4™', tag.text)

        if tag.tail:
            tag.tail = pattern.sub(r'\1\2\3\4™', tag.tail)

    return html.tostring(page, encoding='unicode')


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], '', ['port=', 'domain=']
        )
    except getopt.GetoptError:
        print('usage: main.py [--port, --domain]')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--port':
            port = int(arg)
        elif opt == '--domain':
            domain = arg

    exist_scheme = re.match(r'^(http)s?://', domain)
    if not exist_scheme:
        domain = 'https://' + domain
    run_server()
