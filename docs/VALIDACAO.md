# Protocolo científico e limitações

Escopo: classificação binária (normal × possível ataque para revisão), NÃO um IDS operacional. Sem captura de pacotes ou bloqueio.

## Métricas da execução de referência
Amostragem: 200.000 linhas CIC-UNSW + até 30.000 por arquivo CIC-IDS2017. Teste de 65.185 fluxos, contendo 12.272 ataques. Limiar Random Forest = 0.7935749955639356; semente = 42.

| Estratégia | TP | FP | FN | TN | Precisão | Recall |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest conjunta | 11466 | 591 | 806 | 52322 | 95,10% | 93,43% |
| Cluster reconstruído | 1789 | 197 | 10483 | 52716 | 90,08% | 14,58% |

Os números são da execução anterior, não de nova validação. O agrupamento reconstruído usa novas características e dados, portanto não replica o experimento anterior.

## Riscos ainda não resolvidos
1. **Equivalência semântica:** nomes iguais nas 17 características não provam unidades iguais entre bases. Auditar exportadores, duração, taxas e sentidos de tráfego antes de afirmar portabilidade.
2. **Vazamento:** divisão por grupos de características idênticas diminui duplicatas exatas, mas não garante independência temporal, por sessão, host ou campanha.
3. **Rótulos contraditórios:** existem grupos de características iguais com classificações divergentes; investigar origem e impacto.
4. **Amostragem:** limite por arquivo altera distribuição de classes e prevalência; métricas não representam redes reais.
5. **Categorias difíceis:** Bot (14/37), SSH-Patator (27/70), Web Attack Brute Force (2/58), SQL Injection (0/2), XSS (0/19) tiveram baixo recall em referência. Denominadores muito pequenos para conclusões confiáveis.
6. **Interface:** os dez exemplos arredondados e repetidos são didáticos. Não representam o teste multibase nem capturam FN/FP representativos.

## Próximos experimentos
- Auditar todas as 17 colunas, definição, unidade e comparabilidade; documentar mapeamento explícito.
- Auditar grupos com rótulos contraditórios.
- Executar separações por sessão e tempo, além de teste externo em fonte/campanha nunca vista.
- Reportar intervalos de confiança, recall por classe/categoria e capacidade operacional de triagem.
- Selecionar exemplos representativos e não apenas acertos para a interface.

## Testes de engenharia
Execute os testes Node de unidade, exporte modelo real, rode teste smoke e paridade Python-JS. Esses testes garantem consistência de implementação nos casos analisados, não validade científica externa.
