const test = require('node:test');
const assert = require('node:assert/strict');
const {validateModel, normalizeRow, predictScore} = require('../flux-lab/predict_core.js');
const m = {columns: ['x'], threshold: .5, imputer: [.25],
  trees: [{f:[0,-2,-2],t:[.5,-2,-2],l:[1,-1,-1],r:[2,-1,-1],p:[.5,.1,.9]}]};
test('schema e limiar', () => {
  assert.equal(validateModel(m), m);
  assert.throws(() => validateModel({...m, trees:[]}), /inválido/);
  assert.throws(() => validateModel({...m, threshold:2}), /inválido/);
});
test('decisões determinísticas', () => {
  assert.equal(predictScore(m,[0]), .1);
  assert.equal(predictScore(m,[1]), .9);
});
test('imputação e float32', () => {
  for (const v of [null, NaN, Infinity, -Infinity, 'errado']) {
    assert.deepEqual(normalizeRow(m,[v]), [Math.fround(.25)]);
    assert.equal(predictScore(m,[v]), .1);
  }
  assert.equal(normalizeRow(m,[.1])[0], Math.fround(.1));
});
test('dados malformados', () => {
  assert.throws(() => predictScore(m,[]), /Quantidade/);
  const broken = {...m, trees:[{...m.trees[0],l:[100,-1,-1]}]};
  assert.throws(() => predictScore(broken,[0]), /corrompida/);
});
