import socket
import sys
import threading
from queue import Queue
import argparse
import json 
import csv
import time


print_lock = threading.Lock() #lock object to prevent multiple threads from printing to the console at the same time, which can jumble the output



###function to scan all the open ports and adds them to the list of open ports###
def scan_port(host, port, timeout, open_ports, verbose, delay, s):
    """
    Scan a single port on the given host.

    :param host: The target host's IP or hostname.
    :param port: The port number to scan.
    :param timeout: Timeout for each port scan.
    :param open_ports: A list to hold the open ports.
    :param verbose: Flag to enable verbose output.
    :param delay: Delay between scans for rate limiting.
    :param s: Reusable socket object.
    """
    time.sleep(delay)
    try: 
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        if result == 0:
            with print_lock:
                open_ports.append(port)
                if verbose:
                    print(f"Port {port} is open on {host}.")
    except socket.error as e:
        if verbose:
            print(f"Error scanning port {port}: {str(e)}")

        
    
    
    
    
##this function works as a worker for the threading to continuously takes a port from the queue and uses scan_port to check if it's open##
def worker(host, port_queue, timeout, open_ports, verbose, delay):
    """
    Worker function for threading, pulls ports from queue and scans them.

    :param host: The target host's IP or hostname.
    :param port_queue: Queue of ports to scan.
    :param timeout: Timeout for each port scan.
    :param open_ports: A list to hold the open ports.
    :param verbose: Flag to enable verbose output.
    :param delay: Delay between scans for rate limiting.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(host, port, timeout, open_ports, verbose, delay, s)
        port_queue.task_done()
    s.close()
        
##this function sets up the queue, fills it with the range of ports to be scanned, creates a pool of worker threads, and starts them##

def port_scanner(host, start_port, end_port, timeout, max_threads, verbose, delay):
    """
    The main port scanning function using multithreading.

    :param host: The target host's IP or hostname.
    :param start_port: The starting port number.
    :param end_port: The ending port number.
    :param timeout: Timeout for each port scan.
    :param max_threads: The maximum number of threads to use.
    :param verbose: Flag to enable verbose output.
    :param delay: Delay between scans for rate limiting.
    :return: A list of open ports.
    """
    open_ports = []
    port_queue = Queue()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)
        
    
    threads = []
    for _ in range(min(max_threads, port_queue.qsize())):
        thread = threading.Thread(target=worker, args=(host, port_queue, timeout, open_ports, verbose, delay))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return open_ports

##A function to save the results to a specific file##
def save_results(host, open_ports, output_file, file_format):
    """
    Save the scan results to a file in JSON or CSV format.

    :param host: The target host's IP or hostname.
    :param open_ports: A list of open ports.
    :param output_file: The file path to save the results.
    :param file_format: The format of the output file ('json' or 'csv').
    """
    if file_format == 'json':
        with open(output_file, 'w') as f:
            json.dump({"host": host, "open_ports": open_ports}, f)
    elif file_format == 'csv':
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Host', 'Open Port'])
            for port in open_ports:
                writer.writerow([host, port])


def main():
    """
    Main function to handle argument parsing and initiate the port scanning.
    """
    parser = argparse.ArgumentParser(description="A simple multi-threaded port scanner.")
    parser.add_argument("host", help="Host to scan.")
    parser.add_argument("start_port", type=int, help="Start of the port range to scan.")
    parser.add_argument("end_port", type=int, help="End of the port range to scan.")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout per port in seconds.")
    parser.add_argument("--threads", type=int, default=100, help="Maximum number of threads to use.")
    parser.add_argument("--verbose", action="store_true", help="Increase output verbosity.")
    parser.add_argument("--output", type=str, help="Output file to save the scan results.")
    parser.add_argument("--format", type=str, choices=['json', 'csv'], help="Format of the output file (json or csv).")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between scans in seconds for rate limiting.")

    args = parser.parse_args()
    
    
    if args.start_port < 1 or args.end_port > 65535 or args.end_port < args.start_port:
        parser.error("Invalid port range. Ports should be between 1 and 65535, and start_port should be less than end_port.")
    
    open_ports = port_scanner(args.host, args.start_port, args.end_port, args.timeout, args.threads, args.verbose, args.delay)
    
    if args.output and args.format:
        save_results(args.host, open_ports, args.output, args.format)
    
    if args.verbose:
        if open_ports:
            print(f"\nOpen ports on {args.host}: {sorted(open_ports)}")
        else:
            print(f"\nNo open ports found on {args.host} within the range {args.start_port}-{args.end_port}.")

if __name__ == "__main__":
    main()