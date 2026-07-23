import socket
import datetime
import json
from request import Request
import csv

PORT = 9292

users = []  # List to store user data from the CSV file
with open('users.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        users.append(row)


class Response:  # Response class to build HTTP responses
    def __init__(self, status_code: str, status_message: str, content_type: str, body: str):
        self.status_code = status_code
        self.status_message = status_message
        self.content_type = content_type
        self.body = body
        # Calculate the length of the body in bytes by encoding it to bytes and getting its length
        self.body_length = len(body.encode())
        # Build the full HTTP response string with the status line, headers, and body
        self.raw_response = f"HTTP/1.1 {self.status_code} {self.status_message}\r\nContent-Type:{self.content_type}\r\nContent-Length:{self.body_length}\r\n\r\n{self.body}"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# so you don't have to change ports when restarting
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', PORT))


while True:  # Wait for incoming connections in an infinite loop
    server.listen()
    print(f"waiting for a request on localhost:{PORT}")
    # Accept an incoming connection and unpack the tuple returned by accept() into client_connection and _client_address
    client_connection, _client_address = server.accept()
    print(f"Connection from {_client_address} has been established!")
    # Create a Request object to parse the incoming request
    client_request = Request(client_connection)

    # If the HTTP method is not GET, return a 405 Method Not Allowed response
    if client_request.parsed_request['method'] != 'GET':
        response = Response(
            # Build the response for the 405 Method Not Allowed case
            status_code="405", status_message="Method Not Allowed", content_type="text/html", body='Method Not Allowed'
        )
        # Send the response back to the client by encoding it to bytes and sending it through the connection
        client_connection.send(response.raw_response.encode())

    else:  # If the HTTP method is GET, check the requested URI and respond accordingly
        if client_request.parsed_request['uri'] == '/':
            html_body = "<h1>Hello, World!</h1>"
            response = Response(
                status_code="200", status_message="OK", content_type="text/html", body=html_body
            )
            # Print the response for debugging purposes
            print("Response:", response.raw_response)
            client_connection.send(response.raw_response.encode())

        # If the requested URI is /time, return the current time in JSON format
        elif client_request.parsed_request['uri'] == '/time':
            current_time_data = {"current_time": str(datetime.datetime.now())}
            response = Response(
                status_code="200", status_message="OK", content_type="application/json", body=json.dumps(current_time_data)
            )
            # Print the response for debugging purposes
            print("Response:", response.raw_response)
            client_connection.send(response.raw_response.encode())

        # If the requested URI is /users, return the user data from the CSV file in JSON format
        elif client_request.parsed_request['uri'] == '/users':
            current_user_data = {"users": users}
            response = Response(
                status_code="200", status_message="OK", content_type="application/json", body=json.dumps(current_user_data)
            )
            # Print the response for debugging purposes
            print("Response:", response.raw_response)
            client_connection.send(response.raw_response.encode())

        else:  # If the requested URI does not match any of the above, return a 404 Not Found response
            response = Response(
                status_code="404", status_message="Not Found", content_type="text/html", body='Not Found'
            )
            client_connection.send(response.raw_response.encode())

    client_connection.close()


# Test: curl http://localhost:9292/
# Test: curl http://localhost:9292/time
# Test: curl http://localhost:9292/users
# Test: curl http://localhost:9292/nonsense
# Test: curl -v -X POST http://localhost:9292/time
