package gbn;

import java.io.File;
import java.io.FileInputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.security.MessageDigest;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

public class Emissor {
    // =========================================================================
    // VARIÁVEIS DE ESTADO DO GBN (FSM)
    // =========================================================================
    private static int base = 1;
    private static int nextseqnum = 1;
    private static int N; // Tamanho da janela
    private static PacoteGBN[] bufferJanela; // Buffer Circular

    // Controle de Concorrência
    private static final Object lockFSM = new Object();

    // Temporizador
    private static ScheduledExecutorService timerExecutor = Executors.newSingleThreadScheduledExecutor();
    private static ScheduledFuture<?> temporizadorAtivo = null;
    private static final int TIMEOUT_MS = 1000; // 1 segundo de timeout

    // Rede e Arquivo
    private static DatagramSocket socket;
    private static InetAddress ipDestino;
    private static final int PORTA_DESTINO = 5000;
    private static volatile boolean transmissaoConcluida = false;

    // Estatísticas e Progresso
    private static int pacotesEnviados = 0;
    private static int acksRecebidos = 0;
    private static int retransmissoes = 0;
    private static long bytesTransferidos = 0;
    private static long startTimeStamp;

    public static void main(String[] args) {
        // Validação estrita dos argumentos
        if (args.length < 4) {
            System.out.println("Uso incorreto. Siga o formato:");
            System.out.println("java gbn/Emissor <arquivo_origem> <IP_destino>:<path_destino> <tamanho_janela> <prob_perda>");
            System.out.println("Exemplo: java gbn/Emissor /home/alice/foto.jpg 127.0.0.1:/tmp/foto_recebida.jpg 8 0.10");
            return;
        }

        try {
            // 1. Parsing dos argumentos
            String pathOrigem = args[0];
            String[] destinoStr = args[1].split(":");
            ipDestino = InetAddress.getByName(destinoStr[0]);
            String pathDestino = destinoStr[1];
            N = Integer.parseInt(args[2]);
            double probPerda = Double.parseDouble(args[3]);

            if (N <= 0) {
                System.err.println("Erro: O tamanho da janela deve ser um inteiro positivo.");
                return;
            }
            if (probPerda < 0 || probPerda > 1) {
                System.err.println("Erro: A probabilidade de perda deve ser um valor entre 0 e 1.");
                return;
            }

            bufferJanela = new PacoteGBN[N];
            File arquivoOrigem = new File(pathOrigem);

            if (!arquivoOrigem.exists()) {
                System.err.println("Erro: Arquivo de origem não encontrado.");
                return;
            }

            // 2. Cálculo do Hash MD5 antes de iniciar (Requisito Desejável)
            System.out.println("Calculando MD5 do arquivo original...");
            String hashMD5 = calcularHashMD5(pathOrigem);
            
            socket = new DatagramSocket();

            // 3. Fase de HANDSHAKE (Garante que o Receptor está pronto)
            realizarHandshake(probPerda, pathDestino, hashMD5);

            startTimeStamp = System.currentTimeMillis();

            // 4. Iniciar Thread Paralela para Receber ACKs (FSM do Emissor)
            Thread threadAcks = new Thread(Emissor::receberAcks);
            threadAcks.start();

            // 5. Iniciar Leitura e Envio de Dados (Main Thread = rdt_send)
            enviarArquivo(arquivoOrigem);

            // 6. Aguarda todos os pacotes serem confirmados
            synchronized (lockFSM) {
                while (base < nextseqnum) {
                    lockFSM.wait();
                }
                transmissaoConcluida = true;
            }

            // Espera a thread de recepção de ACKs encerrar completamente
            threadAcks.join(); 
            
            // Restaura o timeout maior para garantir o encerramento seguro
            socket.setSoTimeout(2000); 

            // 7. Encerramento (FIN)
            realizarFin();

            // Exibir estatísticas finais
            System.out.println("\n\n==================================================");
            System.out.println(" TRANSFERÊNCIA CONCLUÍDA COM SUCESSO ");
            System.out.println("==================================================");
            System.out.printf(" Tempo total       : %f s\n", (System.currentTimeMillis() - startTimeStamp)/1000.0f);
            System.out.println(" Pacotes Enviados  : " + pacotesEnviados);
            System.out.println(" ACKs Recebidos    : " + acksRecebidos);
            System.out.println(" Retransmissões    : " + retransmissoes);
            System.out.println("==================================================");

            System.exit(0); // Força o encerramento da JVM (mata a thread do timer)

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // =========================================================================
    // LÓGICA DA FSM: ENVIO DE DADOS (rdt_send)
    // =========================================================================
    private static void enviarArquivo(File arquivo) throws Exception {
        try (FileInputStream fis = new FileInputStream(arquivo)) {
            byte[] bufferLeitura = new byte[PacoteGBN.MAX_PAYLOAD];
            int bytesLidos;

            while ((bytesLidos = fis.read(bufferLeitura)) != -1) {
                // Cria um array do tamanho exato lido
                byte[] payload = new byte[bytesLidos];
                System.arraycopy(bufferLeitura, 0, payload, 0, bytesLidos);

                synchronized (lockFSM) {
                    // CONDIÇÃO: Espera enquanto a janela estiver cheia (nextseqnum >= base + N)
                    while (nextseqnum >= base + N) {
                        lockFSM.wait(); 
                    }

                    // AÇÃO: Cria pacote, envia e adiciona ao buffer circular
                    PacoteGBN pacote = new PacoteGBN(PacoteGBN.TYPE_DATA, nextseqnum, 0, payload);
                    
                    // Buffer Circular: Mapeia o número de sequência para um índice fixo do array [0, N-1]
                    bufferJanela[nextseqnum % N] = pacote;
                    
                    enviarPacoteFisico(pacote);
                    pacotesEnviados++;
                    bytesTransferidos += bytesLidos;

                    // Controle do Temporizador: Inicia se for o pacote mais antigo da janela
                    if (base == nextseqnum) {
                        iniciarTemporizador();
                    }

                    nextseqnum++;
                    atualizarProgressoRealTime();
                }
            }
        }
    }

    // =========================================================================
    // LÓGICA DA FSM: RECEPÇÃO DE ACKs (rdt_rcv)
    // =========================================================================
    private static void receberAcks() {
        byte[] buffer = new byte[PacoteGBN.HEADER_SIZE];

        while (!transmissaoConcluida) {
            try {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                PacoteGBN pacoteRecebido = PacoteGBN.deBytes(packet.getData(), packet.getLength());

                if (pacoteRecebido.getTipo() == PacoteGBN.TYPE_ACK) {
                    int ackNum = pacoteRecebido.getNumAck();
                    acksRecebidos++;

                    synchronized (lockFSM) {
                        // CASO 1: ACK Válido e cumulativo (avança a base)
                        if (ackNum >= base) {
                            base = ackNum + 1;

                            // Se a base alcançou o nextseqnum (janela vazia), para o temporizador.
                            if (base == nextseqnum) {
                                pararTemporizador();
                            } else {
                                // Caso contrário, reinicia (ainda há pacotes não confirmados)
                                iniciarTemporizador();
                            }

                            // Acorda a thread principal que pode estar bloqueada esperando a janela abrir
                            lockFSM.notifyAll();
                        }
                        atualizarProgressoRealTime();
                    }
                }
            } catch (SocketTimeoutException e) {
                // Serve para o socket.receive() destravar 
                // e o while reavaliar se transmissaoConcluida virou true.
            } catch (Exception e) {
                if (!transmissaoConcluida) {
                    System.err.println("\nErro na recepção de ACK: " + e.getMessage());
                }
            }
        }
    }

    // =========================================================================
    // LÓGICA DA FSM: ESTOURO DO TEMPORIZADOR (timeout)
    // =========================================================================
    private static void lidarComTimeout() {
        synchronized (lockFSM) {
            // AÇÃO: Retransmite TODOS os pacotes de base até nextseqnum - 1
            for (int i = base; i < nextseqnum; i++) {
                try {
                    enviarPacoteFisico(bufferJanela[i % N]);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                retransmissoes++;
            }
            // Reinicia o temporizador após o envio em lote
            iniciarTemporizador();
            atualizarProgressoRealTime();
        }
    }

    // =========================================================================
    // MÉTODOS DE CONTROLE DO TEMPORIZADOR
    // =========================================================================
    private static void iniciarTemporizador() {
        pararTemporizador();
        temporizadorAtivo = timerExecutor.schedule(Emissor::lidarComTimeout, TIMEOUT_MS, TimeUnit.MILLISECONDS);
    }

    private static void pararTemporizador() {
        if (temporizadorAtivo != null && !temporizadorAtivo.isDone()) {
            temporizadorAtivo.cancel(false);
        }
    }

    // =========================================================================
    // MÉTODOS AUXILIARES E DE REDE
    // =========================================================================
    private static void enviarPacoteFisico(PacoteGBN pacote) throws Exception {
        byte[] bytes = pacote.paraBytes();
        DatagramPacket packet = new DatagramPacket(bytes, bytes.length, ipDestino, PORTA_DESTINO);
        socket.send(packet);
    }

    private static void realizarHandshake(double probPerda, String pathDestino, String hashMD5) throws Exception {
        System.out.print("Sincronizando sessão com o Receptor...");
        String payload = probPerda + ";" + pathDestino + ";" + hashMD5;
        PacoteGBN handshake = new PacoteGBN(PacoteGBN.TYPE_HANDSHAKE, 0, 0, payload.getBytes());
        
        socket.setSoTimeout(2000); // Timeout de 2s específico para o Handshake
        byte[] bufferAck = new byte[PacoteGBN.HEADER_SIZE];
        
        while (true) {
            try {
                enviarPacoteFisico(handshake);
                DatagramPacket ackPacket = new DatagramPacket(bufferAck, bufferAck.length);
                socket.receive(ackPacket);
                PacoteGBN pacote = PacoteGBN.deBytes(ackPacket.getData(), ackPacket.getLength());
                
                if (pacote.getTipo() == PacoteGBN.TYPE_ACK) {
                    System.out.println(" [OK]");
                    break;
                }
            } catch (SocketTimeoutException e) {
                System.out.print("."); // Tenta novamente caso perca o Handshake inicial
            }
        }
        socket.setSoTimeout(500); // Acorda a thread de ACKs a cada 500ms
    }

    private static void realizarFin() throws Exception {
        System.out.print("\nFinalizando transferência...");
        PacoteGBN fin = new PacoteGBN(PacoteGBN.TYPE_FIN, nextseqnum, 0, null);
        
        byte[] bufferAck = new byte[PacoteGBN.HEADER_SIZE];
        
        while (true) {
            try {
                // Envia o pacote FIN e aguarda o ACK correspondente
                enviarPacoteFisico(fin);
                DatagramPacket ackPacket = new DatagramPacket(bufferAck, bufferAck.length);
                socket.receive(ackPacket);
                
                PacoteGBN pacote = PacoteGBN.deBytes(ackPacket.getData(), ackPacket.getLength());
                
                if (pacote.getTipo() == PacoteGBN.TYPE_ACK && pacote.getNumAck() == nextseqnum) {
                    System.out.println(" [OK]");
                    break;
                }
            } catch (SocketTimeoutException e) {
                System.out.print(".");
            }
        }
    }

    private static void atualizarProgressoRealTime() {
        long tempoDecorridoS = (System.currentTimeMillis() - startTimeStamp) / 1000;
        if (tempoDecorridoS == 0) tempoDecorridoS = 1; // Evita divisão por zero
        
        long kbps = (bytesTransferidos*8) / (1000*tempoDecorridoS);
        
        System.out.print(String.format("\rProgresso -> Enviados: %d | Base/ACK: %d | Retransmissões: %d | Throughput: %d Kb/s", 
                                        pacotesEnviados, base, retransmissoes, kbps));
    }

    private static String calcularHashMD5(String pathArquivo) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (FileInputStream fis = new FileInputStream(pathArquivo)) {
            byte[] buffer = new byte[8192];
            int bytesLidos;
            while ((bytesLidos = fis.read(buffer)) != -1) {
                md.update(buffer, 0, bytesLidos);
            }
        }
        byte[] hashBytes = md.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b : hashBytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}