# Aula prática — Semânticas de Entrega no Kafka (DCE540)

Continuação da aula introdutória de Apache Kafka, focada em **at-most-once**,
**at-least-once** e **exactly-once**.

## Arquivos
- `docker-compose.yml` — sobe um broker Kafka local (modo KRaft) + Kafka UI, próprio desta aula
- `aula2_semanticas_entrega.ipynb` — notebook da aula
- `requirements.txt` — dependências Python (Jupyter + kafka-python)

## Pré-requisitos
- **VS Code**, com as extensões **Python** e **Jupyter** instaladas
- **Docker** e **Docker Compose** instalados e em execução
- **Python** instalado (no Windows, geralmente o comando é `python`; no Linux/Mac, `python3`)

## Atenção: conflito de portas com a Aula 1

Este ambiente usa as mesmas portas da aula anterior (9092, 9094, 8080). Se os
containers da Aula 1 (`kafka-aula`, `kafka-ui-aula`) ainda estiverem rodando,
pare-os antes de subir este ambiente:

```bash
# na pasta da Aula 1
docker compose down
```

> **Use sempre `python -m pip install ...`, nunca `pip install ...` sozinho.** Em pastas dentro do OneDrive/Google Drive, o `pip.exe` isolado pode acabar sendo o do Python global do sistema em vez do `venv` — mesmo com o prompt mostrando `(venv)` — e os pacotes vão parar no lugar errado sem erro nenhum, só um aviso fácil de passar despercebido (`Defaulting to user installation...`).

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

3. Abra `aula2_semanticas_entrega.ipynb` e selecione o kernel `venv`.
4. Suba o ambiente Kafka:

   ```bash
   docker compose up -d
   ```

5. (Opcional) Acompanhe em `http://localhost:8080` (Kafka UI).
6. Execute as células em ordem (`Shift+Enter`). A Seção 0 do notebook repete este passo a passo.
7. Ao final da aula:

   ```bash
   docker compose down -v
   ```

## Observação sobre portas
O broker expõe dois listeners: `9092` (uso interno, entre containers) e `9094`
(uso externo, para o notebook rodando no host, via `localhost:9094`).

## Observação sobre transações
Esta aula usa transações Kafka (`init_transactions`, `begin_transaction`,
`commit_transaction`, `abort_transaction`) para demonstrar exactly-once. O
`docker-compose.yml` já está configurado com fator de replicação 1 para o log
de estado de transações, compatível com o cluster de broker único usado em
sala de aula.
