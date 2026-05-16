# MLP para Previsão de Carga de Ruptura em Vigas de Concreto Armado

**Trabalho do Problema 4 — Disciplina: Introdução à Modelagem Computacional**
**PPGMCS — Universidade Estadual de Montes Claros (UNIMONTES)**
**III MCSM – Modelagem Computacional do Sertão Mineiro, ago/2026**

---

## Descrição

Aplicação de uma rede neural **Multilayer Perceptron (MLP)** para prever a carga
máxima de ruptura (P, em kN) de vigas de concreto armado a partir de:

| Variável | Descrição | Faixa |
|----------|-----------|-------|
| `fc` | Resistência à compressão do concreto (MPa) | 25 – 50 |
| `ρ`  | Razão aço/concreto (%) | 0,5 – 2,5 |
| `d`  | Altura útil da viga (cm) | 30 – 60 |

A relação analítica simulada é:

```
P = 0,35·fc + 12·ρ + 2,1·d − 0,02·fc·d + ε,   ε ~ N(0; 1,5)
```

## Arquitetura da MLP

```
Entrada (3) → Camada Oculta 1 [16 neurônios, tanh]
            → Camada Oculta 2 [8  neurônios, tanh]
            → Saída linear (1)
```

- Normalização: Min-Max em todas as entradas e saída
- Otimizador: Adam (η = 0,01)
- Épocas: 1.000

## Resultados

| Métrica | Valor |
|---------|-------|
| R²      | 0,9998 |
| RMSE    | 0,54 kN |
| MAE     | 0,44 kN |
| Erro % máx. | < 1% |

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `problema4_mlp.py` | Treinamento da MLP e impressão das métricas |
| `visualizacoes_p4.py` | Geração de 6 figuras (curva de treino, real vs. previsto, sensibilidade, superfície 3D, resíduos, painel) |
| `gerar_word_artigo.py` | Geração do artigo completo em `.docx` |
| `artigo_problema4.tex` | Artigo em LaTeX (template III MCSM) |
| `artigo_problema4.docx` | Artigo Word com figuras e apêndices de código |

## Como executar

```bash
# Instalar dependências (se necessário)
pip install numpy matplotlib scikit-learn tensorflow python-docx

# 1. Treinar o modelo e ver métricas
python problema4_mlp.py

# 2. Gerar todas as visualizações (fig1 a fig6)
python visualizacoes_p4.py

# 3. Gerar o artigo Word completo
python gerar_word_artigo.py
```

## Dependências

- Python 3.9+
- TensorFlow / Keras
- scikit-learn
- NumPy / Matplotlib
- python-docx

## Autoras

- Jordana [Sobrenome] — jordana.funai@gmail.com
- Maria Luiz [Sobrenome]
- Rayre [Sobrenome]

PPGMCS/UNIMONTES — Montes Claros, MG, Brasil

## Referências

- GAMIL, Y. Machine learning in concrete technology. *Frontiers in Built Environment*, v. 9, 2023. DOI: 10.3389/fbuil.2023.1145591
- KHAN, M. et al. Intelligent prediction modeling for flexural capacity of FRP-strengthened RC beams. *Heliyon*, v. 10, e23375, 2023. DOI: 10.1016/j.heliyon.2023.e23375
- ÖZYÜKSEL ÇIFTÇIOĞLU, A. et al. ML based shear strength prediction in RC beams using Levy flight. *Scientific Reports*, v. 15, 2025. DOI: 10.1038/s41598-025-12359-y
- YASEEN, Z. M. Machine learning models for shear strength prediction of RC beam. *Scientific Reports*, v. 13, 2023. DOI: 10.1038/s41598-023-27613-4
