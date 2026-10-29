"""Exporta Random Forest joblib confiável como model.json.gz para Flux Lab."""
import gzip
import hashlib
import json
import sys
from pathlib import Path
import joblib
import numpy as np

def exportar(origem, destino):
    original = Path(origem)
    target = Path(destino)
    model = joblib.load(original)  # ATENÇÃO: carregue apenas joblib de origem confiável
    if model.get("modelo") != "Random Forest":
        raise ValueError("Exportador suporta apenas Random Forest")
    pipeline = model["pipeline"]
    forest = pipeline.named_steps["modelo"]
    imputer = pipeline.named_steps["imputar"]
    columns = list(model["colunas"])
    if list(forest.classes_) != [0, 1] or len(columns) != forest.n_features_in_:
        raise ValueError("Classes ou características incompatíveis")
    if len(imputer.statistics_) != len(columns):
        raise ValueError("Imputador incompatível")
    trees = []
    for estimator in forest.estimators_:
        t = estimator.tree_
        values = t.value[:, 0, :]
        totals = values.sum(axis=1)
        if np.any(totals <= 0):
            raise ValueError("Contagem de folha inválida")
        trees.append({"f": t.feature.tolist(), "t": t.threshold.tolist(),
                      "l": t.children_left.tolist(), "r": t.children_right.tolist(),
                      "p": (values[:, 1] / totals).tolist()})
    result = {"columns": columns, "threshold": float(model["limiar"]),
              "imputer": imputer.statistics_.tolist(), "trees": trees}
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(result, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    with target.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as zipped:
            zipped.write(raw)
    manifest = {"model_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "joblib_sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
                "features": columns, "trees": len(trees),
                "threshold": result["threshold"], "seed": model.get("semente"),
                "note": "Modelo de pesquisa; scores não calibrados como probabilidades."}
    target.with_name("model.manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Exportado: {target} ({len(trees)} árvores)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Uso: python flux-lab/export_model.py modelo.joblib flux-lab/model.json.gz")
    exportar(sys.argv[1], sys.argv[2])
