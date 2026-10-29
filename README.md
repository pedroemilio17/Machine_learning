# Detecção de tráfego de rede com Machine Learning

Projeto acadêmico de agrupamento e classificação binária (normal × possível ataque) em amostras CIC-UNSW-NB15 e CIC-IDS2017. O **Flux Lab** é uma demonstração animada: não captura pacotes, não bloqueia conexões, não identifica categorias de ataque e não é um IDS validado para produção.

## Status
- Notebook multibase e EDA anterior disponíveis.
- Código do simulador, motor JS, testes de unidade e CI publicados.
- **Para usar o simulador é necessário gerar `flux-lab/model.json.gz`** a partir do arquivo treinado e confiável `modelo_binario_pesquisa.joblib`. O arquivo binário exportado ainda não faz parte deste repositório. Se estiver ausente, a interface deve informar a indisponibilidade.
- Os resultados científicos são de uma execução de referência, não foram reexecutados pelo CI. Veja `docs/VALIDACAO.md`.

## Arquivos relevantes
- `3_EDA_DOCUMENTADA.ipynb`: estudo anterior de agrupamento.
- `notebooks/Modelo_Multibase_CIC_UNSW_IDS2017.ipynb`: teste multibase.
- `flux-lab/index.html`, `app.js`, `tour.js`: interface e animação.
- `flux-lab/predict_core.js`: motor de inferência reutilizável e testável.
- `flux-lab/export_model.py`: exportação real da Random Forest.
- `flux-lab/examples.json`: dez registros arredondados apenas para demonstração.
- `scripts/verify_parity.py`: comparação Python × JavaScript.
- `tests/`: testes JavaScript e smoke de modelo.
- `docs/VALIDACAO.md`: metodologia, limites e pendências científicas.

## Executar localmente

Requisitos: Python, Node.js >=18 e navegador moderno com `DecompressionStream`. O `joblib` pode executar código ao carregar: use **somente arquivo de origem confiável**.

```bash
git clone https://github.com/pedroemilio17/Machine_learning.git
cd Machine_learning
python -m pip install -r requirements.txt
python flux-lab/export_model.py /caminho/modelo_binario_pesquisa.joblib flux-lab/model.json.gz
node --test tests/test_predict_core.cjs
node tests/verify_web_model.cjs
python scripts/verify_parity.py /caminho/modelo_binario_pesquisa.joblib
cd flux-lab && python -m http.server 8000
```

Abra `http://localhost:8000` (não `file://`). O exportador gera um manifesto SHA-256. A instalação limpa **não** funcionará como classificador enquanto o gzip do modelo não estiver publicado. O site visual anteriormente compartilhado tem hospedagem e permissões independentes da branch principal.

## Resultados de referência
Na execução anterior com 65.185 registros de teste, incluindo 12.272 ataques, Random Forest reportou 11.466 TP, 591 FP e 806 FN (precisão 95,10%; recall 93,43%). A regra reconstruída de cluster reportou 1.789 TP, 197 FP e 10.483 FN (precisão 90,08%; recall 14,58%). O experimento anterior, de cluster único, reportou 17/23.869 ataques, mas **não é comparação direta**.

Essas métricas dependem da amostragem e não comprovam generalização; 17 nomes de características comuns ainda exigem auditoria de definições/unidades. Amostras demonstrativas pequenas não devem ser usadas para inferir desempenho real. Scores não são probabilidades calibradas.

## Fontes e continuidade
- [CIC-UNSW-NB15](https://www.unb.ca/cic/datasets/cic-unsw-nb15.html)
- [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
- [UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
- [Notebook multibase Colab](https://colab.research.google.com/drive/191SwdYmhNPwsby9cwJIQxZRaRJLGUSil)
- [Notebook anterior Colab](https://colab.research.google.com/drive/1JRCE9k63ddXNC6eVKcDS-G6-blNgfdx4)

Próximo passo científico: examinar conflitos de rótulos, controlar grupos por sessão/tempo e validar em dados externos. Desenvolvido com apoio de IA: requer execução e revisão humana.
