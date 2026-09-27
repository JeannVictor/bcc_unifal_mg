# Aula prática — Apache Kafka (DCE540)

## Arquivos
- `docker-compose.yml` — sobe um broker Kafka local (modo KRaft, sem ZooKeeper) + Kafka UI
- `aula_kafka_dce540.ipynb` — notebook da aula (conceitos, definições, exemplos e atividades)
- `requirements.txt` — dependências Python (Jupyter + kafka-python)

## Pré-requisitos
- **VS Code**, com as extensões **Python** e **Jupyter** instaladas
- **Docker** e **Docker Compose** instalados e em execução
- **Python** instalado (no Windows, geralmente o comando é `python`; no Linux/Mac, `python3`)

## Como usar

1. Abra a pasta desta aula no VS Code (todos os arquivos devem estar juntos na mesma pasta).
2. Em um terminal do VS Code (**Terminal > New Terminal**), crie o ambiente virtual e instale as dependências:

   **Windows (PowerShell):**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   > Se `python -m venv venv` (Windows) der erro dizendo que o Python não foi encontrado, rode `python --version` primeiro para confirmar que ele está instalado e acessível nesse terminal.

3. Abra `aula_kafka_dce540.ipynb` (clique duas vezes no explorador de arquivos do VS Code) e selecione o kernel `venv` no canto superior direito do notebook.
4. No mesmo terminal, suba o ambiente Kafka:

   ```bash
   docker compose up -d
   ```

5. (Opcional) Acompanhe visualmente em `http://localhost:8080` (Kafka UI).
6. Execute as células do notebook em ordem (`Shift+Enter`). A Seção 0 do notebook repete este passo a passo.
7. Ao final da aula:

   ```bash
   docker compose down -v
   ```

## Observação sobre portas
O broker expõe dois listeners: `9092` (uso interno, entre containers) e `9094` (uso externo, para o notebook rodando no host, via `localhost:9094`). O notebook já está configurado para usar `localhost:9094`.
