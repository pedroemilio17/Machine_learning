"""Compara sklearn e JavaScript, inclusive entradas ausentes. Requer Node 18+."""
import json
import subprocess
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
def main(path):
    model = joblib.load(path)  # Apenas arquivo confiável
    rows = [x["v"] for x in json.loads((ROOT/"flux-lab/examples.json").read_text())]
    rows.extend([[None]*len(model["colunas"]), [0]*len(model["colunas"])])
    frame = pd.DataFrame(rows, columns=model["colunas"])
    expected = model["pipeline"].predict_proba(frame)[:,1]
    js = """
const fs=require('fs'),z=require('zlib');
const core=require('./flux-lab/predict_core.js');
const m=core.validateModel(JSON.parse(z.gunzipSync(fs.readFileSync('flux-lab/model.json.gz'))));
const rows=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(rows.map(x=>core.predictScore(m,x))));
"""
    output = subprocess.run(["node","-e",js],cwd=ROOT,input=json.dumps(rows),
                            text=True,capture_output=True,check=True)
    actual = np.array(json.loads(output.stdout))
    maxdiff = float(np.max(np.abs(expected-actual)))
    diverge = int(np.count_nonzero((expected>=model["limiar"]) != (actual>=model["limiar"])))
    print("casos:",len(rows),"diferença máxima:",maxdiff,"decisões divergentes:",diverge)
    if maxdiff>1e-6 or diverge:
        raise SystemExit("FALHA: inferência web divergente")
    print("PASSOU: teste de paridade nos casos registrados; não substitui validação científica")
if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Uso: python scripts/verify_parity.py modelo.joblib")
    main(Path(sys.argv[1]))
