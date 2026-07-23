
class Request:
    def __init__(self, client_connection):
        raw_text = client_connection.recv(4096).decode("utf-8")
        lines = raw_text.split("\r\n")
        self.parse_request(lines)
        self.parsed_request = {
            'method': self.method,
            'uri': self.path,
            'version': self.version
        }

    def parse_request(self, lines):
        # Get the first line of the request, which contains the method, path, and version
        request_line = lines[0]
        # Split the request line into its components (method, path, version)
        request_parts = request_line.split()
        # print("Request line:", request_line)
        self.method = request_parts[0]  # Get the HTTP method.
        # print("Method:", self.method)
        self.path = request_parts[1]  # Get the path from the request line.
        # print("Path:", self.path)
        # Get the HTTP version from the request line.
        self.version = request_parts[2]
        # print("Version:", self.version)
