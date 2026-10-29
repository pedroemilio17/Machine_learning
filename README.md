# Detecção de tráfego de rede com Machine Learning

Projeto acadêmico de análise de tráfego, agrupamento e classificação binária de possíveis ataques. Inclui uma simulação visual de rede para explicar o percurso dos fluxos e as decisões de uma Random Forest.

> **Pesquisa e demonstração.** O sistema não captura tráfego real, não bloqueia conexões e não foi validado como IDS de produção. Um fluxo não priorizado não é necessariamente seguro.

## Demonstração

[**Abrir o Flux Lab**](https://lab-rede-visual-pedro-ml.sharpglade17.chatgpt.site) — acesso atualmente privado ao proprietário. Pessoas sem permissão podem não conseguir abrir o link.

Para uma cópia local, veja a seção de execução abaixo. No simulador, clique em **Iniciar tour** para conhecer o percurso, ou abra **Controles** para definir a proporção e a quantidade de ataques. Os fluxos representam registros de exemplo; as conexões e dispositivos são uma animação.

## Organização

```text
.
├── 3_EDA_DOCUMENTADA.ipynb           # notebook anterior preservado
├── notebooks/
│   └── Modelo_Multibase_CIC_UNSW_IDS2017.ipynb
├── flux-lab/
│   ├── index.html                     # interface e topologia
│   ├── app.js                         # simulação e inferência no navegador
│   ├── tour.js                        # explicações do tour
│   ├── examples.json                  # exemplos de teste com rótulos de referência
│   ├── model.json.gz                  # árvores, características e limiar do modelo
│   └── export_model.py                # exporta o modelo joblib para a interface
└── README.md
```

## O problema

Analisar grandes volumes de conexões de rede é trabalhoso. O projeto investiga se perfis de conexões podem apoiar a triagem humana e quais são as limitações dessa abordagem. Agrupamento organiza conexões semelhantes; classificação binária estima se uma conexão deve ser encaminhada para revisão.

## Experimentos

O notebook anterior estuda o UNSW-NB15, com EDA, tratamento e comparação de K-Means, MiniBatch K-Means e DBSCAN. A regra inicial de escolher somente o cluster mais concentrado em ataques reportou 17 de 23.869 ataques em uma execução: precisão de 100% entre os escolhidos, mas recall de aproximadamente 0,071%.

O notebook multibase usa amostras de CIC-UNSW-NB15 e CIC-IDS2017, prepara características comuns e compara uma regra de agrupamento reconstruída com regressão logística e Random Forest. Escolhe o modelo e o limiar na validação e apresenta métricas no teste reservado, por fonte e categoria.

### Resultado de uma execução de referência

| Estratégia | Ataques no teste | Reportados | Não reportados | Normais reportados | Precisão | Recall |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest conjunta | 12.272 | 11.466 | 806 | 591 | 95,10% | 93,43% |
| Cluster reconstruído | 12.272 | 1.789 | 10.483 | 197 | 90,08% | 14,58% |
| Revisar tudo | 12.272 | 12.272 | 0 | 52.913 | 18,83% | 100% |

A execução usou uma amostra de 200.000 linhas do CIC-UNSW e até 30.000 por arquivo CIC-IDS2017, com divisão por grupos de características idênticas. O limiar foi selecionado no conjunto de validação. A comparação de clusters acima usa **as mesmas características e o mesmo teste do novo experimento**; não é uma reprodução exata da regra do notebook anterior.

Esses resultados dependem das amostras e não são garantia para outra rede. Foram observados grupos com rótulos conflitantes; a divisão não garante separação por sessão ou tempo. As definições e unidades das características comuns ainda devem ser verificadas. A amostragem por arquivo modifica a composição dos dados.

## Como executar a simulação

É necessário um navegador atualizado com suporte a `DecompressionStream` e um servidor HTTP local. Não abra o HTML diretamente pelo protocolo `file://`, pois o navegador precisa buscar o modelo e os exemplos.

```bash
git clone https://github.com/pedroemilio17/Machine_learning.git
cd Machine_learning/flux-lab
python -m http.server 8000
```

Abra `http://localhost:8000`. Escolha um cenário, monte um lote ou envie fluxos individuais. Os dispositivos podem ser arrastados. O painel de resultados mostra acertos e erros em relação ao rótulo de referência.

**Limitação dos exemplos:** a interface atual repete apenas dez registros com valores arredondados, todos acertados pelo modelo nessa pequena amostra. Portanto, os indicadores exibidos durante a animação não representam o teste completo nem o desempenho real. O rótulo conhecido é usado somente para comparação após a decisão; não entra nas 17 características de inferência. O score não é uma probabilidade calibrada e o modelo não prevê a categoria do ataque.

## Como executar o notebook multibase

1. Abra `notebooks/Modelo_Multibase_CIC_UNSW_IDS2017.ipynb` no Google Colab ou em um ambiente Jupyter compatível.
2. Execute as células em ordem. A primeira instala as bibliotecas. As demais baixam espelhos das bases ou permitem configurar caminhos de arquivos locais.
3. Verifique acesso, espaço em disco e memória. A configuração padrão usa amostras para viabilizar a execução; alterá-las muda os resultados e o custo computacional.
4. O notebook salva métricas em CSV e um modelo experimental em `/content/resultados_modelo_multibase`. Copie os arquivos que deseja manter antes de encerrar a sessão.

[Notebook multibase no Colab](https://colab.research.google.com/drive/191SwdYmhNPwsby9cwJIQxZRaRJLGUSil) · [Notebook anterior no Colab](https://colab.research.google.com/drive/1JRCE9k63ddXNC6eVKcDS-G6-blNgfdx4). O acesso aos notebooks depende das permissões do Google Drive.

### Exportar um modelo novo para o simulador

O notebook salva `modelo_binario_pesquisa.joblib`. A partir da pasta `flux-lab`, gere o arquivo usado pelo navegador:

```bash
python export_model.py /caminho/modelo_binario_pesquisa.joblib model.json.gz
```

Use o mesmo ambiente e as mesmas versões de bibliotecas do treinamento. O exportador espera o dicionário e o pipeline produzidos pelo notebook. **Carregue somente arquivos `joblib` confiáveis:** esse formato pode executar código durante a desserialização. Depois de substituir o modelo, confira a equivalência das previsões e ajuste os exemplos antes de apresentar.

## Dados e referências

- [UNSW-NB15 — UNSW](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
- [CIC-UNSW-NB15 — Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/cic-unsw-nb15.html)
- [CIC-IDS2017 — Canadian Institute for Cybersecurity](https://www.unb.ca/cic/datasets/ids-2017.html)
- [Espelho CIC-UNSW-NB15](https://huggingface.co/datasets/bencorn/CIC-UNSW-NB15) e [espelho CIC-IDS2017](https://huggingface.co/datasets/bvsam/cic-ids-2017)

As fontes oficiais indicam os trabalhos a citar. Confira os termos de uso, versões e integridade dos arquivos antes de redistribuir os datasets. Os datasets completos não estão incluídos neste repositório.

## Próximos passos

- Verificar unidades e definições das características das duas fontes.
- Investigar registros com características iguais e rótulos conflitantes.
- Testar divisão por tempo ou sessão e dados externos independentes.
- Substituir os dez exemplos da interface por uma amostra de teste mais representativa, incluindo falsos positivos e falsos negativos, sem selecionar resultados para favorecer o modelo.
- Avaliar capacidade de revisão e, se necessário, desenvolver uma tarefa multiclasse separada para estimar categorias de ataque.

Projeto desenvolvido com apoio de ferramentas de IA. A equipe deve revisar, executar e compreender o código e as conclusões.
