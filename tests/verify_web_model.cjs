const fs = require('node:fs');
const zlib = require('node:zlib');
const assert = require('node:assert/strict');
const {validateModel,predictScore} = require('../flux-lab/predict_core.js');
const file = 'flux-lab/model.json.gz';
if (!fs.existsSync(file)) {
  console.error('model.json.gz ausente: exporte o joblib treinado antes do teste');
  process.exit(2);
}
const m = validateModel(JSON.parse(zlib.gunzipSync(fs.readFileSync(file)).toString('utf8')));
const rows = JSON.parse(fs.readFileSync('flux-lab/examples.json','utf8'));
assert.ok(rows.length > 0);
for (const row of rows) {
  assert.ok([0,1].includes(row.truth));
  const score=predictScore(m,row.v);
  assert.ok(Number.isFinite(score) && score >= 0 && score <= 1);
}
console.log('PASSOU:',m.trees.length,'árvores;',m.columns.length,'características;',rows.length,'exemplos');
