import socket

def scan_port(ip_address, port, end_of_ip, vulnerable_ip):
    while end_of_ip <= 254:
        ip=str(ip_address+"."+str(end_of_ip))
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Checking: "+str(ip))
                s.settimeout(10)  # Set timeout for the connection attempt
                result = s.connect_ex((ip, port))
                if result == 0:
                    print(f"The port {port} of {ip} is open")
                    vulnerable_ip.append(ip)
                else:
                    print(f"The port {port} of {ip} is closed or filtered (Result: {result})")
        except Exception as e:
            print(f"Error: {e}")
        end_of_ip+=1
    print("All the IPs with port 22 open: "+str(vulnerable_ip))


ip_address = "192.168.74"
port = 22
end_of_ip = 1
vulnerable_ip=[]
scan_port(ip_address, port, end_of_ip, vulnerable_ip)