# Aula prática — Schema e Evolução de Dados no Kafka (DCE540)

Terceira aula da sequência de Kafka: Avro, Schema Registry, e um cenário com
múltiplos produtores e múltiplos consumidores evoluindo de forma
independente.

## Arquivos
- `docker-compose.yml` — Kafka (KRaft) + Kafka UI + Schema Registry
- `aula3_schema_evolucao.ipynb` — notebook da aula
- `requirements.txt` — dependências Python (Jupyter, kafka-python, requests, fastavro)

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

   > **Use sempre `python -m pip install ...`, nunca `pip install ...` sozinho** — evita que os pacotes sejam instalados no Python global em vez do venv (comum em pastas dentro do OneDrive/Google Drive).

3. Abra `aula3_schema_evolucao.ipynb` e selecione o kernel `venv`.
4. Suba o ambiente (3 serviços — pode demorar um pouco mais que nas aulas anteriores):

   ```bash
   docker compose up -d
   ```

5. Confirme que o Schema Registry está de pé antes de rodar o notebook:

   ```bash
   curl http://localhost:8081/subjects
   ```

   Deve retornar `[]`. Se der erro de conexão, aguarde mais 20-30 segundos.

6. (Opcional) Acompanhe em `http://localhost:8080` (Kafka UI).
7. Execute as células em ordem (`Shift+Enter`).
8. Ao final da aula:

   ```bash
   docker compose down -v
   ```

## Observação sobre a biblioteca usada

O conteúdo principal desta aula mantém `kafka-python` (consistência com as
aulas anteriores) e implementa a comunicação com o Schema Registry
manualmente, via `requests` + `fastavro`. A Seção 6 do notebook (ao final,
depois das atividades) mostra como o mesmo cenário ficaria usando a
biblioteca `confluent-kafka`, que tem um cliente de Schema Registry embutido
— apresentada como material de comparação, sem necessidade de instalar nada
extra para esta aula.
