# Trabalho Final - Redes de Computadores

![Java](https://img.shields.io/badge/Java-GBN-orange)
![Python](https://img.shields.io/badge/Python-plots-blue)
![Shell](https://img.shields.io/badge/Shell-testes-4EAA25)

Implementação do protocolo Go-Back-N (GBN) para transferência confiável de arquivos (imagens) sobre uma rede simulada com perdas, com emissor e receptor rodando em processos separados.

---

## Organização

| Pasta/Arquivo | Descrição |
|---|---|
| `codigo_redes/src/main/java/gbn/` | Código-fonte Java (`Emissor.java`, `Receptor.java`, `PacoteGBN.java`) |
| `codigo_redes/input/` | Imagens usadas como entrada nos testes |
| `codigo_redes/output/` | Imagens de saída geradas pelos testes, com nomes indicando o tamanho da janela (N) e a probabilidade de perda (P) usados |
| `codigo_redes/run_tests.sh` | Script que roda a bateria de testes variando janela e probabilidade de perda, gerando `resultados.csv` |
| `codigo_redes/resultados.csv` | Resultados brutos coletados pelos testes |
| `codigo_redes/como_executar.txt` | Instruções detalhadas de compilação e execução manual do emissor/receptor |
| `testes/generate_plots.py` | Gera os gráficos (`.png`) e tabelas (`.tex`) a partir de `resultados.csv` |
| `relatorio_tecnico_redes.pdf` | Relatório técnico do trabalho |
| `trabalho_final_redes.pdf` | Enunciado do trabalho |

---

## Como rodar

Compilar (ver detalhes em `codigo_redes/como_executar.txt`):

```bash
cd codigo_redes
javac -d bin src/main/java/gbn/*.java
```

Em dois terminais separados:

```bash
java -cp bin gbn.Receptor
```

```bash
java -cp bin gbn.Emissor input/woman.jpg 127.0.0.1:output/woman.jpg 100 0.1
```

Para rodar a bateria de testes completa:

```bash
cd codigo_redes
./run_tests.sh woman.jpg
```

Para gerar os gráficos a partir dos resultados:

```bash
cd testes
python generate_plots.py
```
