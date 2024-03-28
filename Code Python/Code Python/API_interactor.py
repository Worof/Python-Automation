import requests
import argparse

def send_request(url, method='get', data=None, headers=None, auth=None):
    """
    Send a request to the specified API endpoint.
    
    :param url: API endpoint URL.
    :param method: HTTP method (get, post, put, delete).
    :param data: Data to send in the request body (for POST, PUT).
    :param headers: HTTP headers.
    :param auth: Authentication tuple or object.
    :return: Response object.
    """
    methods = {
        'get': requests.get,
        'post': requests.post,
        'put': requests.put,
        'delete': requests.delete
    }
    
    response = methods[method](url, json=data, headers=headers, auth=auth)
    return response

def main():
    parser = argparse.ArgumentParser(description='API Interactor Tool')
    parser.add_argument('url', type=str, help='API endpoint URL')
    parser.add_argument('--method', type=str, default='get', choices=['get', 'post', 'put', 'delete'], help='HTTP method')
    parser.add_argument('--data', type=str, help='Data to send with the request')
    parser.add_argument('--header', action='append', help='HTTP header (can specify multiple)')
    
    args = parser.parse_args()
    
    # Convert header arguments from list of strings to dictionary
    headers = {k: v for k, v in (h.split(':') for h in args.header)} if args.header else None
    
    # Convert data string to dictionary
    data = eval(args.data) if args.data else None
    
    response = send_request(args.url, method=args.method, data=data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print('Response:')
    print(response.json())

if __name__ == '__main__':
    main()
