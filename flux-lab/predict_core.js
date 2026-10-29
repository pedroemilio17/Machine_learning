/* Motor de inferência compartilhado entre navegador e Node. */
(function (root) {
  "use strict";
  function validateModel(m) {
    if (!m || !Array.isArray(m.columns) || m.columns.length === 0 ||
        !Array.isArray(m.imputer) || m.imputer.length !== m.columns.length ||
        !Array.isArray(m.trees) || m.trees.length === 0 ||
        !Number.isFinite(m.threshold) || m.threshold < 0 || m.threshold > 1) {
      throw new Error("Modelo inválido: metadados incompatíveis");
    }
    for (const t of m.trees) {
      if (!t || !Array.isArray(t.f) || !t.f.length ||
          !["t","l","r","p"].every(k => Array.isArray(t[k]) && t[k].length === t.f.length)) {
        throw new Error("Modelo inválido: árvore inconsistente");
      }
    }
    return m;
  }
  function normalizeRow(m, values) {
    if (!Array.isArray(values) || values.length !== m.columns.length)
      throw new Error("Quantidade de características incorreta");
    return values.map((v, i) => {
      const n = v === null || v === "" ? NaN : Number(v);
      const clean = Number.isFinite(n) ? n : m.imputer[i];
      if (!Number.isFinite(clean)) throw new Error("Imputação inválida");
      return Math.fround(clean);
    });
  }
  function predictScore(m, values) {
    const row = normalizeRow(m, values);
    let sum = 0;
    for (const t of m.trees) {
      let node = 0, steps = 0;
      while (t.f[node] !== -2) {
        const col = t.f[node];
        if (!Number.isInteger(col) || col < 0 || col >= row.length || ++steps > t.f.length)
          throw new Error("Árvore corrompida");
        node = row[col] <= t.t[node] ? t.l[node] : t.r[node];
        if (!Number.isInteger(node) || node < 0 || node >= t.f.length)
          throw new Error("Árvore corrompida: índice");
      }
      if (!Number.isFinite(t.p[node])) throw new Error("Folha inválida");
      sum += t.p[node];
    }
    return sum / m.trees.length;
  }
  const api = Object.freeze({validateModel, normalizeRow, predictScore});
  root.FluxML = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(globalThis);
