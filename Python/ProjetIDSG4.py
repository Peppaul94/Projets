import os  # Gestion des chemins et dossiers
import csv  # Écriture/lecture de dataset CSV
import random  # Génération de données synthétiques
import pickle  # Sauvegarde/chargement des modèles

SKLEARN_AVAILABLE = True  # Indique si scikit-learn est disponible
try:
    from sklearn.ensemble import IsolationForest  # Modèle d’isolation pour anomalies
    from sklearn.svm import OneClassSVM  # SVM une classe pour anomalies
except Exception:
    SKLEARN_AVAILABLE = False  # Fallback si scikit-learn absent

class ZScoreOneClass:  # Classifieur simple basé sur z-score (fallback)
    def __init__(self, z=3.0):  # Seuil z au-delà duquel on considère anomalie
        self.z = z  # Valeur de seuil
        self.means = None  # Moyennes par feature
        self.stds = None  # Écarts-types par feature

    def fit(self, X):  # Apprend moyennes et écarts-types sur données normales
        n = len(X[0])  # Nombre de features
        sums = [0.0] * n  # Sommes par feature
        for row in X:  # Parcourt lignes
            for i, v in enumerate(row):  # Accumule valeurs par colonne
                sums[i] += v
        self.means = [s / len(X) for s in sums]  # Moyennes
        var = [0.0] * n  # Variances non normalisées
        for row in X:  # Calcule variance
            for i, v in enumerate(row):
                d = v - self.means[i]  # Écart à la moyenne
                var[i] += d * d  # Somme des carrés
        self.stds = [((v / max(len(X) - 1, 1)) ** 0.5) or 1.0 for v in var]  # Écart-type (évite 0)
        return self  # Retourne le modèle

    def predict(self, X):  # Prédit anomalies: -1 anomalie, 1 normal
        out = []  # Résultats
        for row in X:  # Parcourt les échantillons
            flag = 1  # Par défaut normal
            for i, v in enumerate(row):  # Pour chaque feature
                z = abs((v - self.means[i]) / self.stds[i])  # z-score
                if z > self.z:  # Dépassement du seuil -> anomalie
                    flag = -1
                    break
            out.append(flag)  # Ajoute label
        return out  # Retourne prédictions

def gen_normal_sample():  # Génère un échantillon de trafic normal
    packet_size = max(64, min(1500, random.gauss(600, 60)))  # Taille proche de 600±60
    inter_arrival_ms = max(1, random.gauss(100, 20))  # Inter-arrivé 100±20 ms
    distinct_ports = max(0, int(random.gauss(3, 1)))  # Peu de ports distincts
    auth_failures = 0 if random.random() < 0.9 else 1  # Rare échec d’auth
    dns_label_len = random.randint(4, 20)  # Labels DNS courts
    tcp_flag_score = random.choice([0, 1, 2])  # Flags TCP bas
    return [packet_size, inter_arrival_ms, distinct_ports, auth_failures, dns_label_len, tcp_flag_score]  # Features

def gen_anomaly_sample():  # Génère un échantillon anormal
    packet_size = random.choice([random.uniform(1400, 3000), random.uniform(10, 100)])  # Extrêmes
    inter_arrival_ms = random.choice([random.uniform(0.1, 5), random.uniform(500, 2000)])  # Très court/long
    distinct_ports = random.randint(20, 200)  # Nombreux ports (scan)
    auth_failures = random.randint(5, 50)  # Échecs répétés (brute force)
    dns_label_len = random.randint(50, 120)  # Labels DNS très longs
    tcp_flag_score = random.randint(4, 6)  # Flags TCP atypiques
    return [packet_size, inter_arrival_ms, distinct_ports, auth_failures, dns_label_len, tcp_flag_score]  # Features

def build_dataset(n_normal=1000, n_anomaly=150, csv_path='Python/data/anomaly_dataset.csv'):  # Construit et sauvegarde dataset
    X_normal = [gen_normal_sample() for _ in range(n_normal)]  # Échantillons normaux
    X_anom = [gen_anomaly_sample() for _ in range(n_anomaly)]  # Échantillons anormaux
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)  # Crée dossier data
    with open(csv_path, 'w', newline='') as f:  # Écrit CSV
        w = csv.writer(f)  # Writer CSV
        w.writerow(['packet_size', 'inter_arrival_ms', 'distinct_ports', 'auth_failures', 'dns_label_len', 'tcp_flag_score', 'label'])  # En-têtes
        for r in X_normal:  # Ligne normale
            w.writerow(r + [0])  # Label 0
        for r in X_anom:  # Ligne anormale
            w.writerow(r + [1])  # Label 1
    return X_normal, X_anom  # Retourne datasets

def train_isolation_forest(X_train):  # Entraîne IsolationForest ou fallback
    if SKLEARN_AVAILABLE:  # Si sklearn dispo
        model = IsolationForest(n_estimators=200, contamination='auto', random_state=42)  # Paramètres de base
        model.fit(X_train)  # Apprentissage sur normal
        return model  # Modèle entraîné
    return ZScoreOneClass(z=3.0).fit(X_train)  # Fallback z-score

def train_oneclass_svm(X_train):  # Entraîne OneClassSVM ou fallback
    if SKLEARN_AVAILABLE:  # Si sklearn dispo
        model = OneClassSVM(kernel='rbf', gamma='scale', nu=0.1)  # Noyau RBF
        model.fit(X_train)  # Apprentissage sur normal
        return model  # Modèle entraîné
    return ZScoreOneClass(z=3.5).fit(X_train)  # Fallback z-score (plus strict)

def evaluate(model, X_test, y_test):  # Calcule métriques
    pred = model.predict(X_test)  # Prédictions modèle (-1 anomalie, 1 normal)
    y_pred = [1 if p == -1 else 0 for p in pred]  # Convertit en 0/1
    tp = sum(1 for t, p in zip(y_test, y_pred) if t == 1 and p == 1)  # Vrais positifs
    fp = sum(1 for t, p in zip(y_test, y_pred) if t == 0 and p == 1)  # Faux positifs
    fn = sum(1 for t, p in zip(y_test, y_pred) if t == 1 and p == 0)  # Faux négatifs
    tn = sum(1 for t, p in zip(y_test, y_pred) if t == 0 and p == 0)  # Vrais négatifs
    precision = tp / (tp + fp) if (tp + fp) else 0.0  # Précision
    recall = tp / (tp + fn) if (tp + fn) else 0.0  # Rappel
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0  # F1
    acc = (tp + tn) / len(y_test) if y_test else 0.0  # Exactitude
    return {'precision': precision, 'recall': recall, 'f1': f1, 'accuracy': acc, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn}  # Dictionnaire métriques

def save_model(model, path):  # Sauvegarde modèle au format pickle
    os.makedirs(os.path.dirname(path), exist_ok=True)  # Crée dossier si nécessaire
    with open(path, 'wb') as f:  # Ouvre fichier binaire
        pickle.dump(model, f)  # Sérialise modèle

def run_demo():  # Démo complète: dataset, entraînement, évaluation, sauvegarde
    Xn, Xa = build_dataset()  # Construit dataset synthétique
    split_n = int(len(Xn) * 0.7)  # Split 70/30 pour normal
    X_train = Xn[:split_n]  # Entraînement: normal
    X_test = Xn[split_n:] + Xa  # Test: normal restant + anomalies
    y_test = [0] * (len(Xn) - split_n) + [1] * len(Xa)  # Labels test
    iforest = train_isolation_forest(X_train)  # Modèle IsolationForest
    ocsvm = train_oneclass_svm(X_train)  # Modèle OneClassSVM
    m_if = evaluate(iforest, X_test, y_test)  # Métriques IF
    m_sv = evaluate(ocsvm, X_test, y_test)  # Métriques OCSVM
    save_model(iforest, 'Python/models/iforest.pkl')  # Sauvegarde IF
    save_model(ocsvm, 'Python/models/ocsvm.pkl')  # Sauvegarde OCSVM
    print('IsolationForest metrics:', m_if)  # Affiche métriques IF
    print('OneClassSVM metrics:', m_sv)  # Affiche métriques OCSVM
    sample_idx = [0, len(X_test) // 2, len(X_test) - 1]  # Indices d’exemples
    for i in sample_idx:  # Affiche prédictions exemplaires
        p_if = -1 if isinstance(iforest, ZScoreOneClass) and iforest.predict([X_test[i]])[0] == -1 else (iforest.predict([X_test[i]])[0])  # Prédiction IF
        p_sv = -1 if isinstance(ocsvm, ZScoreOneClass) and ocsvm.predict([X_test[i]])[0] == -1 else (ocsvm.predict([X_test[i]])[0])  # Prédiction OCSVM
        print('Sample', i, 'truth', y_test[i], 'IF', 1 if p_if == -1 else 0, 'OCSVM', 1 if p_sv == -1 else 0)  # Affichage formatté

if __name__ == '__main__':  # Point d’entrée
    run_demo()  # Lance la démo

