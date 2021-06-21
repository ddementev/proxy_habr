# Proxy Habr

HTTP-proxy-server to modify the source pages, adding after every word with six character the ™ sign.

### Installation
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
### Run server
```
$ python3 main.py
```
Default the server started on the port 8000 and proxying from a domain https://habr.com.
if need to change the port specify a parameter --port number_port.
if need to change the domain specify a parameter --domain example.com
```
$ python3 main.py --port 8080 --domain example.com
```
### Run tests
For to run a tests need install development environment and run tests.py script with help pytest
```
$ pip install -r requirements_dev.txt
$ pytest -q tests.py
```
