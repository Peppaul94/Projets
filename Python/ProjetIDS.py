import re  # Utilise les expressions régulières pour les signatures
import time  # Utilise le temps pour horodater les événements simulés

class DetectionEngine:  # Moteur de détection basé sur signatures et seuils
    def __init__(self, signatures=None, whitelist_ips=None, whitelist_paths=None, portscan_threshold=20, authfail_threshold=5):  # Initialise paramètres et états
        self.signatures = signatures or []  # Liste des signatures fournies ou vide
        self.compiled = []  # Cache des signatures compilées
        for s in self.signatures:  # Parcourt toutes les signatures
            if s.get('type', 'regex') == 'regex':  # Si signature de type regex
                self.compiled.append({**s, 'compiled': re.compile(s['pattern'])})  # Compile le motif regex pour performance
            else:  # Sinon (signature non-regex)
                self.compiled.append(s)  # Ajoute telle quelle
        self.whitelist_ips = set(whitelist_ips or [])  # Exclut les IP sûres pour éviter les faux positifs
        self.whitelist_paths = set(whitelist_paths or [])  # Exclut les chemins légitimes (réduction des faux positifs)
        self.portscan_threshold = portscan_threshold  # Seuil d'alerte scan de ports pour limiter les faux positifs
        self.authfail_threshold = authfail_threshold  # Seuil d'échecs d'authentification pour éviter des alertes ponctuelles
        self.portscan_map = {}  # Map IP -> ensemble de ports sondés
        self.portscan_alerted = set()  # IP déjà alertées pour scan de ports
        self.authfail_map = {}  # Compteur (IP,port) -> nb d'échecs d'auth
        self.authfail_alerted = set()  # Paires déjà alertées pour brute force

    def process_event(self, event):  # Traite un événement et retourne les alertes
        alerts = []  # Liste d’alertes produites
        src = event.get('src_ip')  # Utilisé pour filtrer via whitelist IP (anti faux positifs)
        if src in self.whitelist_ips:  # Ignore les événements provenant de sources approuvées
            return alerts  # Pas d'alerte pour sources whitelistes
        path = event.get('path', '')  # Utilisé pour whitelist de chemins (anti faux positifs)
        if path in self.whitelist_paths:  # Ignore les chemins connus légitimes
            return alerts  # Pas d'alerte pour chemins whitelistes
        for s in self.compiled:  # Parcourt toutes les signatures compilées
            t = s.get('type', 'regex')  # Type de signature (regex, dns_entropy, etc.)
            if t == 'regex':  # Gestion des signatures regex
                f = s['field']  # Champ de l'événement à vérifier
                v = str(event.get(f, ''))  # Valeur observée sous forme texte
                if s['compiled'].search(v):  # Correspondance au motif de la signature
                    alerts.append({'signature_id': s['id'], 'name': s['name'], 'severity': s['severity'], 'src_ip': src, 'details': v})  # Ajoute alerte détaillée
            elif t == 'dns_entropy':  # Heuristique sur la structure du nom DNS
                host = str(event.get('host', ''))  # Récupère l’hôte DNS
                sub = host.split('.')  # Sépare en labels
                sub0 = sub[0] if sub else ''  # Premier label
                if len(sub0) >= s.get('min_len', 50) and re.fullmatch(r'[A-Za-z0-9]+', sub0):  # Limite les faux positifs: longueur élevée + alphanum
                    alerts.append({'signature_id': s['id'], 'name': s['name'], 'severity': s['severity'], 'src_ip': src, 'details': host})  # Ajoute alerte DNS tunneling
        proto = event.get('protocol')  # Protocole réseau observé
        dport = event.get('dst_port')  # Port de destination
        if proto == 'TCP' and isinstance(dport, int):  # Suivi de scan de ports sur TCP
            ports = self.portscan_map.get(src)  # Récupère ensemble de ports sondés
            if ports is None:  # Si première observation pour cette IP
                ports = set()  # Crée ensemble des ports uniques
                self.portscan_map[src] = ports  # Enregistre ensemble
            ports.add(dport)  # Ajoute port observé
            if len(ports) >= self.portscan_threshold and src not in self.portscan_alerted:  # Seuil pour éviter de flagger un usage normal
                self.portscan_alerted.add(src)  # Marque IP comme déjà alertée
                alerts.append({'signature_id': 'PORT_SCAN', 'name': 'Port scan', 'severity': 'high', 'src_ip': src, 'details': f'{len(ports)} ports'})  # Alerte scan
        if event.get('auth_failure') is True and isinstance(dport, int):  # Comptage d'échecs d'authentification
            key = (src, dport)  # Clé d'agrégation IP/port
            cnt = self.authfail_map.get(key, 0) + 1  # Incrémente compteur
            self.authfail_map[key] = cnt  # Sauvegarde nouveau compteur
            if cnt >= self.authfail_threshold and key not in self.authfail_alerted:  # Seuil d'échecs pour éviter les faux positifs isolés
                self.authfail_alerted.add(key)  # Marque la paire comme alertée
                alerts.append({'signature_id': 'AUTH_BRUTE', 'name': 'Authentication brute force', 'severity': 'medium', 'src_ip': src, 'details': f'{cnt} failures on port {dport}'})  # Alerte brute force
        return alerts  # Retourne l’ensemble des alertes

def default_signatures():  # Définit la base de signatures par défaut
    return [  # Liste de signatures (dictionnaires)
        {'id': 'SQLI_BASIC', 'name': 'SQL injection', 'type': 'regex', 'field': 'query', 'pattern': r"(?i)(?:('|%27)\s*(?:or|and)\s*\d+\s*=\s*\d+)|(?:union\s+select)|(?:--|#|;\s*drop)", 'severity': 'high'},  # Injection SQL basique
        {'id': 'XSS_SCRIPT', 'name': 'XSS', 'type': 'regex', 'field': 'payload', 'pattern': r"(?i)<script[^>]*>", 'severity': 'high'},  # Script XSS
        {'id': 'DIR_TRAV', 'name': 'Directory traversal', 'type': 'regex', 'field': 'path', 'pattern': r"\.\./\.\./|%2e%2e%2f", 'severity': 'medium'},  # Traversée de répertoires
        {'id': 'CMD_INJ', 'name': 'Command injection', 'type': 'regex', 'field': 'payload', 'pattern': r"(?:;|&&|\|)\s*(?:cat|ls|wget|curl|nc)\b", 'severity': 'high'},  # Injection de commandes système
        {'id': 'SUS_UA', 'name': 'Suspicious user-agent', 'type': 'regex', 'field': 'user_agent', 'pattern': r"(?i)curl|wget|sqlmap|nikto|dirbuster", 'severity': 'low'},  # Agents utilisateurs suspects
        {'id': 'DNS_TUN', 'name': 'DNS tunneling pattern', 'type': 'dns_entropy', 'min_len': 50, 'severity': 'medium'}  # Patron de tunneling DNS
    ]  # Fin de la liste de signatures

def simulate_events():  # Génère des événements simulés d'attaque
    events = []  # Initialise la liste d'événements
    for p in [21,22,23,25,53,80,110,135,139,143,443,445,8080,3306,3389,5900,587,993,995,123,161,389,636]:  # Ports courants (FTP, SSH, HTTP, RDP, DB…)
        events.append({'timestamp': time.time(), 'src_ip': '10.0.0.8', 'dst_ip': '10.0.0.1', 'dst_port': p, 'protocol': 'TCP', 'payload': '', 'path': '/', 'query': ''})  # Événements de scan de ports
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.5', 'dst_ip': '10.0.0.1', 'dst_port': 443, 'protocol': 'TCP', 'payload': '', 'path': '/login', 'query': "username=admin'%20OR%201%3D1--&password=x", 'user_agent': 'Mozilla/5.0'})  # Événement SQLi
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.6', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': '<script>alert(1)</script>', 'path': '/search', 'query': 'q=test', 'user_agent': 'Mozilla/5.0'})  # Événement XSS
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.7', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': '', 'path': '/../../etc/passwd', 'query': '', 'user_agent': 'Mozilla/5.0'})  # Événement traversée répertoires
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.8', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': 'id; curl http://evil', 'path': '/cmd', 'query': ''})  # Événement injection commande
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.9', 'dst_ip': '10.0.0.1', 'dst_port': 80, 'protocol': 'TCP', 'payload': '', 'path': '/', 'query': '', 'user_agent': 'sqlmap/1.7'})  # Événement UA d’outil d’attaque
    longlabel = 'a'*60  # Génère un label DNS très long
    events.append({'timestamp': time.time(), 'src_ip': '192.168.1.10', 'dst_ip': '10.0.0.53', 'dst_port': 53, 'protocol': 'UDP', 'payload': '', 'path': '', 'query': '', 'host': longlabel + '.example.com'})  # Événement DNS tunneling
    for i in range(7):  # Génère plusieurs échecs d’auth sur SSH
        events.append({'timestamp': time.time(), 'src_ip': '10.0.0.9', 'dst_ip': '10.0.0.1', 'dst_port': 22, 'protocol': 'TCP', 'payload': '', 'path': '', 'query': '', 'auth_failure': True})  # Échec SSH
    for i in range(6):  # Génère plusieurs échecs d’auth sur RDP
        events.append({'timestamp': time.time(), 'src_ip': '10.0.0.11', 'dst_ip': '10.0.0.1', 'dst_port': 3389, 'protocol': 'TCP', 'payload': '', 'path': '', 'query': '', 'auth_failure': True})  # Échec RDP
    return events  # Retourne la liste d’événements

def run_demo():  # Lance la démo du moteur sur événements simulés
    engine = DetectionEngine(signatures=default_signatures())  # Instancie le moteur avec signatures par défaut
    events = simulate_events()  # Crée un flux d’événements
    detections = []  # Contiendra toutes les alertes
    for idx, ev in enumerate(events):  # Parcourt les événements avec index
        alerts = engine.process_event(ev)  # Produit les alertes pour l’événement
        for a in alerts:  # Parcourt les alertes produites
            a['event_index'] = idx  # Ajoute l’index d’événement pour la traçabilité
            detections.append(a)  # Stocke l’alerte
    for d in detections:  # Affiche chaque alerte produite
        print(f"[{d['severity']}] {d['name']} from {d['src_ip']} at event {d['event_index']} -> {d['signature_id']} | {d['details']}")  # Sortie formatée
    print(f"Total detections: {len(detections)}")  # Affiche le total d’alertes

if __name__ == '__main__':  # Point d'entrée du script
    run_demo()  # Exécute la démo si lancé directement