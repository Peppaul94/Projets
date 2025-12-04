import threading
import time
#import socket
import random
import string


## Function to print Time in Tasks (debug only)
def print_time(threadName, delay):
   while 1:
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))


## Structure for each Task
class MyThread(threading.Thread):
    def __init__(self, thread_id, password, stop_event, used_strings, lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id  # Store the thread ID
        self.password = password
        self.length = len(password)
        self.stop_event = stop_event
        self.used_strings = used_strings  # Shared set
        self.lock = lock
    """
    def scan_port(self, ip_address, ports, end_of_ip, vulnerable_ip):
        for port in ports:
            while end_of_ip <= 254:
                ip = str(ip_address + "." + str(end_of_ip))
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        print("Checking: " + str(ip))
                        s.settimeout(1)  # Set timeout for the connection attempt
                        result = s.connect_ex((ip, port))
                        if result == 0:
                            print(f"The port {port} of {ip} is open")
                            vulnerable_ip.append(ip)
                        else:
                            print(f"The port {port} of {ip} is closed or filtered (Result: {result})")
                except Exception as e:
                    print(f"Error: {e}")
                end_of_ip += 1
            print("All the IPs with port " + str(port) + " open: " + str(vulnerable_ip))
            vulnerable_ip = []
    """
    def brute_force(self, length):
        characters =  string.ascii_lowercase + string.ascii_uppercase # string.digits # + string.ascii_lowercase  # + string.punctuation  # Letters and digits
        while True:
            random_string = ''.join(random.choice(characters) for _ in range(length))
            print(random_string)
            
            with self.lock:  # Ensure thread-safe access to shared set
                if random_string not in self.used_strings:
                    self.used_strings.add(random_string)
                    return random_string


    def find_matching_string(self, stop_event):
        start_time = time.time()
        attempts = 0  # Counter to track the number of attempts
        while not stop_event.is_set():  # Check if another thread has stopped
            random_string = self.brute_force(self.length)
            attempts += 1
            #print(f"{self.name}: Attempt {attempts}: {random_string}")
            if random_string == self.password:
                end_time = time.time()  # Record the end time
                duration = end_time - start_time  # Calculate the duration
                print(f"{self.name}: Match found after {attempts} attempts: {random_string}")
                print(f"{self.name}: Time taken: {duration:.2f} seconds")
                stop_event.set()  # Signal other threads to stop
                break
        #else:
            #print(f"{self.name}: Stopping as another thread found the password.")


    def run(self):
        self.find_matching_string(stop_event)


# Create new threads
file_path = input("Enter the path to your file: ")
password="Admin"


def dictionary_attack(file_path, password, stop_event):
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            for i, line in enumerate(file):  # Iterate through the file lines
                word = line.strip()
                if word == password:
                    print(f"Password '{password}' found on line {i + 1}")
                    stop_event.set()
                    return
            print(f"Password '{password}' not found in the file.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")


used_strings = set()
lock = threading.Lock()
stop_event = threading.Event()


# Start dictionary attack
dictionary_attack(file_path, password, stop_event)


threads = []
num_threads = 278


if not stop_event.is_set():
    for i in range(num_threads):
        thread = MyThread(i, password, stop_event, used_strings, lock)
        threads.append(thread)
        thread.start()


# Wait for all threads to complete
for thread in threads:
    thread.join()