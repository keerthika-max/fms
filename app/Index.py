import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line
from dotenv import load_dotenv
import socket
import ssl

load_dotenv()  # Load environment variables from .env file

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Create WSGI application
application = get_wsgi_application()

class ServerE:
    _server_instance = None
    port = int(os.getenv('PORT', 8002))
    is_production = os.getenv('NODE_ENV') == 'production'
    server = None

    def __init__(self):
        self.run_server()

    @classmethod
    def get_server_instance(cls):
        if not cls._server_instance:
            cls._server_instance = cls()
        return cls._server_instance

    def run_server(self):
        if self.is_production:
            self.create_https_server()
        else:
            self.create_http_server()

    def create_http_server(self):
        from django.core.servers.basehttp import run

        print(f"Starting HTTP server on port {self.port}...")
        run(addr='0.0.0.0', port=self.port, wsgi_handler=application)

    def create_https_server(self):
        from wsgiref.simple_server import make_server
        from socketserver import ThreadingMixIn

        class ThreadedWSGIServer(ThreadingMixIn, make_server):
            pass

        key_path = os.getenv('SSL_PRIVATE_KEY_PATH', '/var/www/html/server/ssl/private.key')
        cert_path = os.getenv('SSL_CERTIFICATE_PATH', '/var/www/html/server/ssl/certificate.crt')
        ca_path = os.getenv('SSL_CA_PATH', '/var/www/html/server/ssl/ca.crt')

        # Load SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        if ca_path:
            ssl_context.load_verify_locations(cafile=ca_path)

        print(f"Starting HTTPS server on port {self.port}...")
        server = ThreadedWSGIServer('0.0.0.0', self.port, application)
        server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
        server.serve_forever()

if __name__ == "__main__":
    # Bootstrap the server
    server = ServerE.get_server_instance()

    # You can also include the Django management commands if needed
    execute_from_command_line(sys.argv)
