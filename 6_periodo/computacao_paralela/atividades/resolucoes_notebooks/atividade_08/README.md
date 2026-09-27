# Aula prática — Particionamento Customizado e Processamento de Streams (DCE540)

Quarta aula da sequência de Kafka: implementação de um particionador
customizado (kafka-python) e dos conceitos centrais do Kafka Streams
(KTable, agregação contínua, janelas de tempo, joins) implementados
manualmente em Python.

## Arquivos
- `docker-compose.yml` — Kafka (KRaft) + Kafka UI
- `aula4_particionamento_streams.ipynb` — notebook da aula
- `requirements.txt` — dependências Python (Jupyter, kafka-python)

## Pré-requisitos
- **VS Code**, com as extensões **Python** e **Jupyter** instaladas
- **Docker** e **Docker Compose** instalados e em execução
- **Python** instalado (no Windows, geralmente `python`; no Linux/Mac, `python3`)

## Atenção: conflito de portas com aulas anteriores

Este ambiente usa as mesmas portas das aulas anteriores (9092, 9094, 8080).
Se algum ambiente anterior ainda estiver rodando, pare-o primeiro:

```bash
# na pasta da aula anterior que ainda estiver de pé
docker compose down
```

## Como usar

1. Abra a pasta desta aula no VS Code (todos os arquivos devem estar juntos).
2. Em um terminal do VS Code, crie o ambiente virtual e instale as dependências:

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   ```

   > **Use sempre `python -m pip install ...`, nunca `pip install ...` sozinho** — evita que os pacotes sejam instalados no Python global em vez do venv.

3. Abra `aula4_particionamento_streams.ipynb` e selecione o kernel `venv`.
4. Suba o ambiente:

   ```bash
   docker compose up -d
   ```

5. (Opcional) Acompanhe em `http://localhost:8080` (Kafka UI) — útil para ver a distribuição de mensagens entre partições na Seção 2.
6. Execute as células em ordem (`Shift+Enter`).
7. Ao final da aula:

   ```bash
   docker compose down -v
   ```

## Observação sobre Kafka Streams

O Kafka Streams "oficial" é uma biblioteca Java. Esta aula reimplementa seus
conceitos centrais manualmente em Python (com `kafka-python`), para manter
consistência com as aulas anteriores. A Seção 6 do notebook (extra, após as
atividades) mostra o equivalente em Java e menciona a biblioteca `faust`
como alternativa que roda de fato em Python.
