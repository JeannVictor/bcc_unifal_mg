package gbn;

import java.nio.ByteBuffer;

public class PacoteGBN {
    // Tipos de pacotes (1 byte cada)
    public static final byte TYPE_DATA = 0;
    public static final byte TYPE_ACK = 1;
    public static final byte TYPE_HANDSHAKE = 2;
    public static final byte TYPE_FIN = 3;
    
    // Tamanhos definidos (11 bytes de cabeçalho no total)
    // 1 (tipo) + 4 (numSeq) + 4 (numAck) + 2 (tamanhoDados) = 11 bytes
    public static final int HEADER_SIZE = 11; 
    public static final int MAX_PAYLOAD = 1024; // Tamanho máximo dos dados do ficheiro

    // Campos do cabeçalho
    private byte tipo;
    private int numSeq;
    private int numAck;
    private short tamanhoDados;
    
    // Payload (dados da aplicação)
    private byte[] dados;

    /**
     * Construtor principal para criar um novo pacote a ser enviado.
     */
    public PacoteGBN(byte tipo, int numSeq, int numAck, byte[] dados) {
        this.tipo = tipo;
        this.numSeq = numSeq;
        this.numAck = numAck;
        
        if (dados != null) {
            // Garante que não excedemos o tamanho máximo do payload
            if (dados.length > MAX_PAYLOAD) {
                throw new IllegalArgumentException("O payload excede o tamanho máximo de " + MAX_PAYLOAD + " bytes.");
            }
            this.dados = dados;
            this.tamanhoDados = (short) dados.length;
        } else {
            this.dados = new byte[0];
            this.tamanhoDados = 0;
        }
    }

    /**
     * Serializa o objeto PacoteGBN num array de bytes para ser enviado via UDP.
     */
    public byte[] paraBytes() {
        // Aloca o buffer com o tamanho exato: Cabeçalho + Dados
        ByteBuffer buffer = ByteBuffer.allocate(HEADER_SIZE + this.tamanhoDados);
        
        // Insere os campos do cabeçalho na ordem correta
        buffer.put(tipo);          // 1 byte
        buffer.putInt(numSeq);     // 4 bytes
        buffer.putInt(numAck);     // 4 bytes
        buffer.putShort(tamanhoDados); // 2 bytes
        
        // Insere o payload (se houver)
        if (this.tamanhoDados > 0) {
            buffer.put(dados);
        }
        
        return buffer.array(); // Retorna o array de bytes pronto para o DatagramPacket
    }

    /**
     * Desserializa um array de bytes recebido via UDP e reconstrói o objeto PacoteGBN.
     */
    public static PacoteGBN deBytes(byte[] bytes, int comprimento) {
        // Envolve o array de bytes recebido num ByteBuffer
        ByteBuffer buffer = ByteBuffer.wrap(bytes, 0, comprimento);
        
        // Lê os campos do cabeçalho na mesma ordem em que foram escritos
        byte tipo = buffer.get();
        int numSeq = buffer.getInt();
        int numAck = buffer.getInt();
        short tamanhoDados = buffer.getShort();
        
        // Lê o payload, se existir
        byte[] dados = null;
        if (tamanhoDados > 0) {
            dados = new byte[tamanhoDados];
            buffer.get(dados); // Copia os bytes do buffer para o array 'dados'
        }
        
        return new PacoteGBN(tipo, numSeq, numAck, dados);
    }

    public byte getTipo() { return tipo; }
    public int getNumSeq() { return numSeq; }
    public int getNumAck() { return numAck; }
    public short getTamanhoDados() { return tamanhoDados; }
    public byte[] getDados() { return dados; }
}