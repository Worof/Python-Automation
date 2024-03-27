import unittest
from unittest.mock import patch
import socket
from port_scanner import scan_port, port_scanner

class TestPortScanner(unittest.TestCase):
    def test_scan_port_open(self):
        """Test scanning an open port."""
        with patch('socket.socket.connect_ex', return_value=0):
            open_ports = []
            scan_port('127.0.0.1', 80, 1, open_ports, False, 0, socket.socket())
            self.assertIn(80, open_ports)

    def test_scan_port_closed(self):
        """Test scanning a closed port."""
        with patch('socket.socket.connect_ex', return_value=1):
            open_ports = []
            scan_port('127.0.0.1', 80, 1, open_ports, False, 0, socket.socket())
            self.assertNotIn(80, open_ports)

    def test_port_scanner(self):
        """Test the port scanner function."""
        # Mocking the scan_port function to simulate open ports
        with patch('port_scanner.scan_port', side_effect=lambda host, port, timeout, open_ports, verbose, delay, _: open_ports.append(port)):
            open_ports = port_scanner('127.0.0.1', 1, 100, 1, 10, False, 0)
            self.assertEqual(len(open_ports), 100)  # Expecting 100 open ports from 1 to 100

# More tests can be added for other functions and edge cases.

if __name__ == '__main__':
    unittest.main()
