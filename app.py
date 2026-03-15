from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            with open("Data_Management_Project/project_assignment.html", "rb") as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())


    def do_POST(self):

        if self.path == "/submit_profile":

            length = int(self.headers["Content-Length"])
            data = self.rfile.read(length).decode()

            form = urllib.parse.parse_qs(data)

            full_name = form.get("full_name", [""])[0]
            email = form.get("email", [""])[0]
            experience = form.get("experience", [""])[0]
            tech_stack = form.get("tech_stack", [""])[0]
            duration = form.get("duration", [""])[0]
            skills = form.get("skills", [""])[0]
            projects = form.get("projects", [])
            availability = form.get("availability", ["no"])[0]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Profile saved")


server = HTTPServer(("localhost", 8000), Server)

#print("Server running: http://localhost:8000")

server.serve_forever()