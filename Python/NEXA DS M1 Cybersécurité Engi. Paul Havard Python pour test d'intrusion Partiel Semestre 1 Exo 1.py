import socket

def scan_port(ip_address, vulnerable_ports, port):
    while port <= 1024:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Checking: "+str(ip_address)+":"+str(port))
                s.settimeout(5)  # Set timeout for the connection attempt
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    print(f"The port {port} of {ip_address} is open")
                    vulnerable_ports.append(port)
                else:
                    print(f"The port {port} of {ip_address} is closed or filtered (Result: {result})")
        except Exception as e:
            print(f"Error: {e}")
        port+=1
    print("All the IPs with port 22 open: "+str(vulnerable_ports))


ip_address = "35.175.136.38"
vulnerable_ports=[]
port=1
scan_port(ip_address, vulnerable_ports, port)