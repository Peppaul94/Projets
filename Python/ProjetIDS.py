import re
import time

class DetectionEngine:
    def __init__(self, signatures=None, whitelist_ips=None, whitelist_paths=None, portscan_threshold=20, authfail_threshold=5):
        self.signatures = signatures or []
        self.compiled = []
        for s in self.signatures:
            if s.get('type', 'regex') == 'regex':
                self.compiled.append({**s, 'compiled': re.compile(s['pattern'])})
            else:
                self.compiled.append(s)
        self.whitelist_ips = set(whitelist_ips or [])
        self.whitelist_paths = set(whitelist_paths or [])
        self.portscan_threshold = portscan_threshold
        self.authfail_threshold = authfail_threshold
        self.portscan_map = {}
        self.portscan_alerted = set()
        self.authfail_map = {}
        self.authfail_alerted = set()

    def process_event(self, event):
        alerts = []
        src = event.get('src_ip')
        if src in self.whitelist_ips:
            return alerts
        path = event.get('path', '')
        if path in self.whitelist_paths:
            return alerts
        for s in self.compiled:
            t = s.get('type', 'regex')
            if t == 'regex':
                f = s['field']
                v = str(event.get(f, ''))
                if s['compiled'].search(v):
                    alerts.append({'signature_id': s['id'], 'name': s['name'], 'severity': s['severity'], 'src_ip': src, 'details': v})
            elif t == 'dns_entropy':
                host = str(event.get('host', ''))
                sub = host.split('.')
                sub0 = sub[0] if sub else ''
                if len(sub0) >= s.get('min_len', 50) and re.fullmatch(r'[A-Za-z0-9]+', sub0):
                    alerts.append({'signature_id': s['id'], 'name': s['name'], 'severity': s['severity'], 'src_ip': src, 'details': host})
        proto = event.get('protocol')
        dport = event.get('dst_port')
        if proto == 'TCP' and isinstance(dport, int):
            ports = self.portscan_map.get(src)
            if ports is None:
                ports = set()
                self.portscan_map[src] = ports
            ports.add(dport)
            if len(ports) >= self.portscan_threshold and src not in self.portscan_alerted:
                self.portscan_alerted.add(src)
                alerts.append({'signature_id': 'PORT_SCAN', 'name': 'Port scan', 'severity': 'high', 'src_ip': src, 'details': f'{len(ports)} ports'})
        if event.get('auth_failure') is True and isinstance(dport, int):
            key = (src, dport)
            cnt = self.authfail_map.get(key, 0) + 1
            self.authfail_map[key] = cnt
            if cnt >= self.authfail_threshold and key not in self.authfail_alerted:
                self.authfail_alerted.add(key)
                alerts.append({'signature_id': 'AUTH_BRUTE', 'name': 'Authentication brute force', 'severity': 'medium', 'src_ip': src, 'details': f'{cnt} failures on port {dport}'})
        return alerts

def default_signatures():
    return [
        {'id': 'SQLI_BASIC', 'name': 'SQL injection', 'type': 'regex', 'field': 'query', 'pattern': r"(?i)(?:('|%27)\s*(?:or|and)\s*\d+\s*=\s*\d+)|(?:union\s+select)|(?:--|#|;\s*drop)", 'severity': 'high'},
        {'id': 'XSS_SCRIPT', 'name': 'XSS', 'type': 'regex', 'field': 'payload', 'pattern': r"(?i)<script[^>]*>", 'severity': 'high'},
        {'id': 'DIR_TRAV', 'name': 'Directory traversal', 'type': 'regex', 'field': 'path', 'pattern': r"\.\./\.\./|%2e%2e%2f", 'severity': 'medium'},
        {'id': 'CMD_INJ', 'name': 'Command injection', 'type': 'regex', 'field': 'payload', 'pattern': r"(?:;|&&|\|)\s*(?:cat|ls|wget|curl|nc)\b", 'severity': 'high'},
        {'id': 'SUS_UA', 'name': 'Suspicious user-agent', 'type': 'regex', 'field': 'user_agent', 'pattern': r"(?i)curl|wget|sqlmap|nikto|dirbuster", 'severity': 'low'},
        {'id': 'DNS_TUN', 'name': 'DNS tunneling pattern', 'type': 'dns_entropy', 'min_len': 50, 'severity': 'medium'}
    ]

def simulate_events():
    events = []
    for p in [21,22,23,25,53,80,110,135,139,143,443,445,8080,3306,3389,5900,587,993,995,123,161,389,636]:
        events.append({'timestamp': time.time(), 'src_ip': '10.0.0.8', 'dst_ip': '10.0.0.1', 'dst_port': p, 'protocol': 'TCP', 'payload': '', 'path': '/', 'query': ''})
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.5', 'dst_ip': '10.0.0.1', 'dst_port': 443, 'protocol': 'TCP', 'payload': '', 'path': '/login', 'query': "username=admin'%20OR%201%3D1--&password=x", 'user_agent': 'Mozilla/5.0'})
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.6', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': '<script>alert(1)</script>', 'path': '/search', 'query': 'q=test', 'user_agent': 'Mozilla/5.0'})
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.7', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': '', 'path': '/../../etc/passwd', 'query': '', 'user_agent': 'Mozilla/5.0'})
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.8', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': 'id; curl http://evil', 'path': '/cmd', 'query': ''})
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.9', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': '', 'path': '/', 'query': '', 'user_agent': 'sqlmap/1.7'})
    longlabel = 'a'*60
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.10', 'dst_ip': '10.0.0.53', 'dst_port': 53, 'protocol': 'UDP', 'payload': '', 'path': '', 'query': '', 'host': longlabel + '.example.com'})
    for i in range(7):
        events.append({'timestamp': time.time(), 'src_ip': '10.0.0.9', 'dst_ip': '10.0.0.1', 'dst_port': 22, 'protocol': 'TCP', 'payload': '', 'path': '', 'query': '', 'auth_failure': True})
    for i in range(6):
        events.append({'timestamp': time.time(), 'src_ip': '10.0.0.11', 'dst_ip': '10.0.0.1', 'dst_port': 3389, 'protocol': 'TCP', 'payload': '', 'path': '', 'query': '', 'auth_failure': True})
    return events

def run_demo():
    engine = DetectionEngine(signatures=default_signatures())
    events = simulate_events()
    detections = []
    for idx, ev in enumerate(events):
        alerts = engine.process_event(ev)
        for a in alerts:
            a['event_index'] = idx
            detections.append(a)
    for d in detections:
        print(f"[{d['severity']}] {d['name']} from {d['src_ip']} at event {d['event_index']} -> {d['signature_id']} | {d['details']}")
    print(f"Total detections: {len(detections)}")

if __name__ == '__main__':
    run_demo()

