"""Exporta a Random Forest do notebook para uso no navegador.

Use exclusivamente arquivos joblib de fontes confiáveis.
"""
import gzip
import json
import sys
from pathlib import Path
import joblib

if len(sys.argv) != 3:
    raise SystemExit('Uso: python export_model.py modelo.joblib model.json.gz')
model = joblib.load(sys.argv[1])
pipeline = model['pipeline']
forest = pipeline.named_steps['modelo']
imputer = pipeline.named_steps['imputar']
if list(forest.classes_) != [0, 1]:
    raise ValueError('O exportador requer classes binárias ordenadas como [0, 1].')
trees = []
for estimator in forest.estimators_:
    tree = estimator.tree_
    values = tree.value[:, 0, :]
    probability = values[:, 1] / values.sum(axis=1)
    trees.append({'f': tree.feature.tolist(), 't': tree.threshold.tolist(),
                  'l': tree.children_left.tolist(), 'r': tree.children_right.tolist(),
                  'p': probability.tolist()})
output = {'columns': model['colunas'], 'threshold': float(model['limiar']),
          'imputer': imputer.statistics_.tolist(), 'trees': trees}
with gzip.open(Path(sys.argv[2]), 'wt', encoding='utf-8', compresslevel=9) as file:
    json.dump(output, file, separators=(',', ':'))
print('Modelo exportado:', sys.argv[2])
