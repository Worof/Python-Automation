import requests
import argparse
import json
from datetime import datetime

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
    parser.add_argument('url', type=str, nargs = '?', help='API endpoint URL')
    parser.add_argument('--method', type=str, default='get', choices=['get', 'post', 'put', 'delete'], help='HTTP method')
    parser.add_argument('--data', type=str, help='Data to send with the request')
    parser.add_argument('--header', action='append', help='HTTP header (can specify multiple)')
    
    args = parser.parse_args()
    
    if not args.url:
        args.url = input('Enter the API endpoint URL: ')
        args.method = input('Enter the HTTP method (get, post, put, delete): ').lower()
        data_input = input('Enter the data to send with the request (in dictionary format), or press enter to skip: ')
        args.data = data_input if data_input else None
        header_input = input('Enter HTTP headers (in key:value format, separated by commas), or press enter to skip: ')
        
        if header_input:
            args.header = header_input.split(',')
        else:
            args.header = None
    
    # Convert header arguments from list of strings to dictionary
    headers = {k.strip(): v.strip() for k, v in (h.split(':') for h in args.header)} if args.header else None
    
    # Convert data string to dictionary
    data = eval(args.data) if args.data else None
    
    response = send_request(args.url, method=args.method, data=data, headers=headers)
    print(f'Status Code: {response.status_code}')
    
    filename = f"response_{datetime.now().strftime('%Y%m%d_%H%M')}"

    if 'application/json' in response.headers.get('Content-Type', ''):
        content = response.json()
        filename += '.json'
        with open(filename, 'w') as f:
            json.dump(content, f, indent=4)
    else:
        content = response.text
        filename += '.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f'Response saved to {filename}')

if __name__ == '__main__':
    main()