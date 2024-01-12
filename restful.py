import argparse
import json
import csv
import requests

class RestClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"
    def __init__(self, method, endpoint, output_file):
        self.method = method
        self.endpoint = endpoint
        self.output_file = output_file
        
    def send_request(self):
        url = f"{self.BASE_URL}{self.endpoint}"
        response = None
        if self.method.lower() == "get":
            response = requests.get(url)
        elif self.method.lower() == "post":
            response = requests.post(url, json={})
        return response
    
    def process_response(self, response):
        print(f"HTTP Status Code: {response.status_code}")

        if not response.ok:
            print(f"Error: {response.text}")
            exit(1)
            if self.output_file:
                self.save_to_file(response.json())
        else:
            print(json.dumps(response.json(), indent=2))

    def save_to_file(self, data):
        if self.output_file.endswith(".json"):
            with open(self.output_file, "w") as json_file:
                json.dump(data, json_file, indent=2)
                print(f"Response saved to {self.output_file}")
        elif self.output_file.endswith(".csv"):
            with open(self.output_file, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                # Assuming data is a list of dictionaries
                csv_writer.writerows([data[0].keys()])  # write header
                csv_writer.writerows([d.values() for d in data])
                print(f"Response saved to {self.output_file}")

def main():
    parser = argparse.ArgumentParser(description="Simple command-line REST client.")
    parser.add_argument("METHOD", choices=["get", "post"], help="HTTP method: get or post")
    parser.add_argument("ENDPOINT", help="URI fragment, e.g., /posts/1")
    parser.add_argument("-o", "--output", help="Output file (JSON or CSV)")

    args = parser.parse_args()

    rest_client = RestClient(args.METHOD, args.ENDPOINT, args.output)
    response = rest_client.send_request()
    rest_client.process_response(response)

if __name__ == "__main__":
    main()