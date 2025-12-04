import requests

def test_api():
    url = "http://127.0.0.1:8000/tea-gardens?page=1&size=100"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Total: {data['total']}")
            print(f"List length: {len(data['list'])}")
            for item in data['list']:
                print(f"ID: {item['id']}, Name: {item['name']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_api()
