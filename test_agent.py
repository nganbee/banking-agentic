import json
import requests

def run_tests():
    
    with open('examples/sample_requests.json', 'r', encoding='utf-8') as f:
        test_cases = json.load(f)

    url = "http://localhost:8000/chat"
    
    for i, case in enumerate(test_cases):
        payload = {"message": case["message"]}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"User Message: {case["message"]}")
            print(f"ID: {result.get('request_id')}")
            print(f"Response: {result.get('response')}")
            print(f"Decision: {result.get('decision')}")
        else:
            print(f"Error: {response.text}")
            

if __name__ == "__main__":
    run_tests()