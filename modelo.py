# -*- coding: utf-8 -*-
# Modelo IA para clasificar señales de tránsito

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report

import numpy as np

# Simulamos el dataset: por ejemplo, 4 clases (Pare, Cruce, Semáforo Rojo, Semáforo Verde)
# Aquí usamos digits como ejemplo: tú usarás features de imágenes de tus señales
digits = datasets.load_digits()

# Tomemos solo 4 clases (0,1,2,3 para simplificar el ejemplo)
X = digits.data[digits.target < 4]
y = digits.target[digits.target < 4]

# División en train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamos un clasificador (SVM en este ejemplo)
clf = SVC(kernel='linear', probability=True)
clf.fit(X_train, y_train)

# Evaluación rápida
y_pred = clf.predict(X_test)
print("Reporte de clasificación:\n", classification_report(y_test, y_pred))

# Guardar modelo si deseas usarlo luego
import joblib
joblib.dump(clf, 'modelo_senales.pkl')
