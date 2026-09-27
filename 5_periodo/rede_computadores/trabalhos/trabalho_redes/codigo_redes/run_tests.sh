#!/bin/bash
ARQUIVO="${1:-woman.jpg}"
INPUT_DIR="input"
OUTPUT_DIR="output"
CSV_FILE="resultados.csv"
TIMEOUT_SEC=180

[ ! -f "$INPUT_DIR/$ARQUIVO" ] && echo "Erro: $INPUT_DIR/$ARQUIVO não encontrado." && exit 1
mkdir -p "$OUTPUT_DIR"
echo "arquivo,janela,prob,enviados,retrans,descartados,taxa_perda_efetiva,tempo_s,throughput_kbps,md5_ok" > "$CSV_FILE"

extract_num() {
    local keyword="$1"
    local file="${2:-/tmp/emissor_out.txt}"
    grep -E "$keyword" "$file" | tail -1 | sed 's/.*:[[:space:]]*//' | sed 's/,/./' | grep -oE '[0-9]+([.][0-9]+)?' | head -1
}

run_test() {
    local N=$1 PROB=$2
    local OUTFILE="$OUTPUT_DIR/test_${ARQUIVO%.*}_N${N}_P${PROB//./}.jpg"
    echo ">>> Teste: N=$N, prob=$PROB"
    pkill -f "gbn.Receptor" 2>/dev/null; sleep 0.4
    java -cp bin gbn.Receptor > /tmp/receptor_out.txt 2>&1 &
    RPID=$!; sleep 0.8
    timeout $TIMEOUT_SEC java -cp bin gbn.Emissor "$INPUT_DIR/$ARQUIVO" "127.0.0.1:$OUTFILE" "$N" "$PROB" > /tmp/emissor_out.txt 2>&1
    sleep 2; kill $RPID 2>/dev/null; wait $RPID 2>/dev/null

    ENVIADOS=$(extract_num "Pacotes Enviados")
    RETRANS=$(extract_num "Retransmiss")
    TEMPO=$(extract_num "Tempo total")
    DESCARTADOS=$(extract_num "Total de pacotes simulados como perda" /tmp/receptor_out.txt)
    TAXA=$(extract_num "Taxa de perda efetiva" /tmp/receptor_out.txt)
    MD5_OK=$(grep -c 'SUCESSO: Os hashes' /tmp/receptor_out.txt)

    [ -z "$ENVIADOS" ] && ENVIADOS="?"; [ -z "$RETRANS" ] && RETRANS="?"
    [ -z "$TEMPO" ] && TEMPO="?"; [ -z "$DESCARTADOS" ] && DESCARTADOS="?"
    [ -z "$TAXA" ] && TAXA="?"; [ -z "$MD5_OK" ] && MD5_OK=0

    TAMANHO_BYTES=$(stat -c%s "$INPUT_DIR/$ARQUIVO")
    if [ "$TEMPO" != "?" ] && [ "$(echo "$TEMPO > 0" | bc)" = "1" ]; then
        THROUGHPUT=$(echo "scale=0; ($TAMANHO_BYTES * 8) / ($TEMPO * 1000)" | bc 2>/dev/null)
    else
        THROUGHPUT="?"
    fi

    echo "$ARQUIVO,$N,$PROB,$ENVIADOS,$RETRANS,$DESCARTADOS,$TAXA,$TEMPO,$THROUGHPUT,$MD5_OK" >> "$CSV_FILE"
    echo "  -> Enviados=$ENVIADOS, Retrans=$RETRANS, Descartados=$DESCARTADOS, Tempo=$TEMPO, MD5=$MD5_OK"
}

# Bateria
for N in 1 2 4 8 16 32; do
    for PROB in 0.0 0.05 0.1 0.15; do
        run_test $N $PROB
    done
done

echo "Testes concluídos. Resultados em $CSV_FILE"