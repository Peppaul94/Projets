import os
import csv
import random
import pickle

SKLEARN_AVAILABLE = True
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.svm import OneClassSVM
except Exception:
    SKLEARN_AVAILABLE = False

class ZScoreOneClass:
    def __init__(self, z=3.0):
        self.z = z
        self.means = None
        self.stds = None

    def fit(self, X):
        n = len(X[0])
        sums = [0.0] * n
        for row in X:
            for i, v in enumerate(row):
                sums[i] += v
        self.means = [s / len(X) for s in sums]
        var = [0.0] * n
        for row in X:
            for i, v in enumerate(row):
                d = v - self.means[i]
                var[i] += d * d
        self.stds = [((v / max(len(X) - 1, 1)) ** 0.5) or 1.0 for v in var]
        return self

    def predict(self, X):
        out = []
        for row in X:
            flag = 1
            for i, v in enumerate(row):
                z = abs((v - self.means[i]) / self.stds[i])
                if z > self.z:
                    flag = -1
                    break
            out.append(flag)
        return out

def gen_normal_sample():
    packet_size = max(64, min(1500, random.gauss(600, 60)))
    inter_arrival_ms = max(1, random.gauss(100, 20))
    distinct_ports = max(0, int(random.gauss(3, 1)))
    auth_failures = 0 if random.random() < 0.9 else 1
    dns_label_len = random.randint(4, 20)
    tcp_flag_score = random.choice([0, 1, 2])
    return [packet_size, inter_arrival_ms, distinct_ports, auth_failures, dns_label_len, tcp_flag_score]

def gen_anomaly_sample():
    packet_size = random.choice([random.uniform(1400, 3000), random.uniform(10, 100)])
    inter_arrival_ms = random.choice([random.uniform(0.1, 5), random.uniform(500, 2000)])
    distinct_ports = random.randint(20, 200)
    auth_failures = random.randint(5, 50)
    dns_label_len = random.randint(50, 120)
    tcp_flag_score = random.randint(4, 6)
    return [packet_size, inter_arrival_ms, distinct_ports, auth_failures, dns_label_len, tcp_flag_score]

def build_dataset(n_normal=1000, n_anomaly=150, csv_path='Python/data/anomaly_dataset.csv'):
    X_normal = [gen_normal_sample() for _ in range(n_normal)]
    X_anom = [gen_anomaly_sample() for _ in range(n_anomaly)]
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['packet_size', 'inter_arrival_ms', 'distinct_ports', 'auth_failures', 'dns_label_len', 'tcp_flag_score', 'label'])
        for r in X_normal:
            w.writerow(r + [0])
        for r in X_anom:
            w.writerow(r + [1])
    return X_normal, X_anom

def train_isolation_forest(X_train):
    if SKLEARN_AVAILABLE:
        model = IsolationForest(n_estimators=200, contamination='auto', random_state=42)
        model.fit(X_train)
        return model
    return ZScoreOneClass(z=3.0).fit(X_train)

def train_oneclass_svm(X_train):
    if SKLEARN_AVAILABLE:
        model = OneClassSVM(kernel='rbf', gamma='scale', nu=0.1)
        model.fit(X_train)
        return model
    return ZScoreOneClass(z=3.5).fit(X_train)

def evaluate(model, X_test, y_test):
    pred = model.predict(X_test)
    y_pred = [1 if p == -1 else 0 for p in pred]
    tp = sum(1 for t, p in zip(y_test, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_test, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_test, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_test, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0
    acc = (tp + tn) / len(y_test) if y_test else 0.0
    return {'precision': precision, 'recall': recall, 'f1': f1, 'accuracy': acc, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn}

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def run_demo():
    Xn, Xa = build_dataset()
    split_n = int(len(Xn) * 0.7)
    X_train = Xn[:split_n]
    X_test = Xn[split_n:] + Xa
    y_test = [0] * (len(Xn) - split_n) + [1] * len(Xa)
    iforest = train_isolation_forest(X_train)
    ocsvm = train_oneclass_svm(X_train)
    m_if = evaluate(iforest, X_test, y_test)
    m_sv = evaluate(ocsvm, X_test, y_test)
    save_model(iforest, 'Python/models/iforest.pkl')
    save_model(ocsvm, 'Python/models/ocsvm.pkl')
    print('IsolationForest metrics:', m_if)
    print('OneClassSVM metrics:', m_sv)
    sample_idx = [0, len(X_test) // 2, len(X_test) - 1]
    for i in sample_idx:
        p_if = -1 if isinstance(iforest, ZScoreOneClass) and iforest.predict([X_test[i]])[0] == -1 else (iforest.predict([X_test[i]])[0])
        p_sv = -1 if isinstance(ocsvm, ZScoreOneClass) and ocsvm.predict([X_test[i]])[0] == -1 else (ocsvm.predict([X_test[i]])[0])
        print('Sample', i, 'truth', y_test[i], 'IF', 1 if p_if == -1 else 0, 'OCSVM', 1 if p_sv == -1 else 0)

if __name__ == '__main__':
    run_demo()

