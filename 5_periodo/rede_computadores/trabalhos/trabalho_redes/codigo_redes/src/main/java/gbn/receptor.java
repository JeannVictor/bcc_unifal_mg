package gbn;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketAddress;
import java.security.MessageDigest;
import java.util.Random;

public class Receptor {
    // =========================================================================
    // VARIÁVEIS DE ESTADO E SESSÃO (FSM GBN)
    // =========================================================================
    private static int expectedseqnum = 1;       // Número de sequência esperado
    private static PacoteGBN ultimoAckEnviado;  // Guarda o último ACK válido para reenvio
    private static Random random = new Random();
    private static boolean sessaoAtiva = false;
    private static FileOutputStream fileOutputStream = null;

    // Parâmetros de configuração da sessão (vindos do Handshake)
    private static double probPerdaConfigurada = 0.0;
    private static String pathDestino;
    private static String hashOriginalMD5 = ""; // Guardará o hash enviado pelo Emissor

    // Contadores para estatísticas
    private static int totalPacotesRecebidos = 0;
    private static int totalPacotesDescartados = 0;

    // =========================================================================
    // MÉTODO PRINCIPAL (LOOP DE ESCUTA UDP)
    // =========================================================================
    public static void main(String[] args) {
        int porta = 5000; // Porta padrão sugerida
        
        if (args.length > 0) {
            try {
                porta = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                System.out.println("Porta inválida. Utilizando a porta padrão 5000.");
            }
        }

        System.out.println("==================================================");
        System.out.println(" Receptor GBN inicializado. Aguardando na porta " + porta);
        System.out.println("==================================================");

        // Inicialização padrão da FSM: ACK inicial fictício com número 0
        ultimoAckEnviado = new PacoteGBN(PacoteGBN.TYPE_ACK, 0, 0, null);

        // Uso exclusivo de sockets UDP nativos (Requisito R2)
        try (DatagramSocket socket = new DatagramSocket(porta)) {
            byte[] bufferRecebimento = new byte[PacoteGBN.HEADER_SIZE + PacoteGBN.MAX_PAYLOAD];

            while (true) {
                DatagramPacket datagramPacket = new DatagramPacket(bufferRecebimento, bufferRecebimento.length);
                socket.receive(datagramPacket); // Bloqueia aguardando datagrama

                SocketAddress enderecoEmissor = datagramPacket.getSocketAddress();
                PacoteGBN pacote = PacoteGBN.deBytes(datagramPacket.getData(), datagramPacket.getLength());

                // Redireciona o pacote para a função específica baseada no seu tipo
                switch (pacote.getTipo()) {
                    case PacoteGBN.TYPE_HANDSHAKE:
                        tratarHandshake(pacote, socket, enderecoEmissor);
                        break;
                    case PacoteGBN.TYPE_DATA:
                        tratarData(pacote, socket, enderecoEmissor);
                        break;
                    case PacoteGBN.TYPE_FIN:
                        tratarFin(pacote, socket, enderecoEmissor);
                        break;
                    default:
                        System.out.println("[AVISO] Tipo de pacote desconhecido ignorado.");
                        break;
                }
            }
        } catch (Exception e) {
            System.err.println("Erro crítico no loop de execução do Receptor: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // Garante que o arquivo seja fechado em caso de falhas inesperadas
            if (fileOutputStream != null) {
                try {
                    fileOutputStream.close();
                } catch (IOException e) {
                    System.err.println("Erro ao fechar o arquivo de saída: " + e.getMessage());
                }
            }
        }
    }

    // =========================================================================
    // FUNÇÕES ESPECÍFICAS DE TRATAMENTO DE PACOTES
    // =========================================================================

    /**
     * Trata o pacote inicial de controle (Handshake), extraindo metadados e abrindo o arquivo.
     */
    private static void tratarHandshake(PacoteGBN pacote, DatagramSocket socket, SocketAddress enderecoEmissor) throws IOException {
        if (sessaoAtiva) {
            // Se uma sessão já está ativa, apenas reenvia a confirmação do Handshake caso o Emissor tenha perdido o ACK anterior
            enviarAckGenerico(socket, enderecoEmissor, 0);
            return;
        }

        // Extrai a string de payload e faz o parse dos 3 parâmetros esperados
        // probPerda;pathDestino;hashMD5
        String dadosHandshake = new String(pacote.getDados());
        String[] parametros = dadosHandshake.split(";");

        if (parametros.length < 3) {
            System.err.println("[ERRO HANDSHAKE] Dados de handshake malformados. Abortando.");
            return;
        }

        probPerdaConfigurada = Double.parseDouble(parametros[0]);
        pathDestino = parametros[1];
        hashOriginalMD5 = parametros[2]; // Guarda o hash original enviado pelo Emissor

        System.out.println("\n[HANDSHAKE] Nova sessão de transferência configurada");
        System.out.println("-> Salvando em: " + pathDestino);
        System.out.println("-> Hash MD5 original: " + hashOriginalMD5);
        System.out.printf("-> Probabilidade de perda simulada: %.1f%%\n\n", (probPerdaConfigurada * 100));

        // Cria/Sobrescreve o arquivo no path absoluto de destino
        fileOutputStream = new FileOutputStream(pathDestino);
        
        // --- LIMPEZA DE ESTADO CORRETA AQUI ---
        sessaoAtiva = true;
        expectedseqnum = 1; 
        totalPacotesRecebidos = 0;
        totalPacotesDescartados = 0;
        
        // Zera o último ACK enviado para não mandar resquícios da sessão anterior!
        ultimoAckEnviado = new PacoteGBN(PacoteGBN.TYPE_ACK, 0, 0, null);

        // Responde ao Emissor confirmando o estabelecimento da sessão
        enviarAckGenerico(socket, enderecoEmissor, 0);
    }

    /**
     * Trata a chegada de um pacote contendo dados binários do arquivo.
     */
    private static void tratarData(PacoteGBN pacote, DatagramSocket socket, SocketAddress enderecoEmissor) throws IOException {
        
        if (!sessaoAtiva) {
            // Se a sessão já fechou, apenas ignora dados perdidos que chegaram com atraso na rede
            return;
        }       

        // FSM do GBN: Aceita apenas o pacote estritamente esperado na ordem sequencial
        if (pacote.getNumSeq() == expectedseqnum) {
            
            totalPacotesRecebidos++;
            
            // Simulação de perda aleatória agindo SOMENTE sobre pacotes em ordem
            if (random.nextDouble() < probPerdaConfigurada) { //
                totalPacotesDescartados++;
                return; // Corta a execução: não grava e não envia ACK, forçando timeout no Emissor
            }

            // Pacote válido e aceito
            fileOutputStream.write(pacote.getDados());
            System.out.print("\r[RECEBIDO] Pacote DATA #" + pacote.getNumSeq() + " processado e escrito            ");

            // Atualiza o último ACK cumulativo bem-sucedido
            ultimoAckEnviado = new PacoteGBN(PacoteGBN.TYPE_ACK, 0, expectedseqnum, null);
            expectedseqnum++; // Avança a janela do receptor para o próximo da fila
            
        } else {
            // Pacote duplicado ou fora de ordem: descarta os dados mas reenvia o último ACK cumulativo válido
            System.out.print("\r[FORA DE ORDEM] Pacote DATA #" + pacote.getNumSeq() + " ignorado. Esperava #" + expectedseqnum);
        }

        // Transmite o ACK (seja o novo cumulativo ou o duplicado)
        byte[] bytesAck = ultimoAckEnviado.paraBytes();
        socket.send(new DatagramPacket(bytesAck, bytesAck.length, enderecoEmissor));
    }

    /**
     * Trata o sinalizador de término (FIN), finaliza o arquivo, faz a checagem hash e exibe estatísticas.
     */
    private static void tratarFin(PacoteGBN pacote, DatagramSocket socket, SocketAddress enderecoEmissor) throws IOException {
        if (!sessaoAtiva) {
            // Se recebermos um FIN e a sessão JÁ ESTÁ INATIVA, significa que o nosso ACK anterior se perdeu.
            // Precisamos reenviar o ACK do FIN para que o Emissor saia do loop de espera e encerre.
            PacoteGBN ackFin = new PacoteGBN(PacoteGBN.TYPE_ACK, 0, pacote.getNumSeq(), null);
            byte[] bytesAck = ackFin.paraBytes();
            socket.send(new DatagramPacket(bytesAck, bytesAck.length, enderecoEmissor));
            return;
        }

        System.out.println("\n[FIN] Sinal de encerramento recebido. Finalizando gravações...");
        
        fileOutputStream.close(); // Fecha o arquivo garantindo a gravação de todos os buffers do SO
        
        sessaoAtiva = false; // Desativa a sessão
        
        // Envia o ACK de encerramento para liberar a thread do Emissor
        PacoteGBN ackFin = new PacoteGBN(PacoteGBN.TYPE_ACK, 0, pacote.getNumSeq(), null);
        byte[] bytesAck = ackFin.paraBytes();
        socket.send(new DatagramPacket(bytesAck, bytesAck.length, enderecoEmissor));
        
        expectedseqnum = 1;

        // ----------------------------------------------------
        // VALIDAÇÃO DE INTEGRIDADE (Requisito Desejável R9)
        // ----------------------------------------------------
        try {
            System.out.println("[INTEGRIDADE] Calculando hash MD5 do arquivo final...");
            String hashCalculado = calcularHashMD5(pathDestino);
            System.out.println("-> Hash Calculado : " + hashCalculado);
            System.out.println("-> Hash Original   : " + hashOriginalMD5);

            if (hashCalculado.equalsIgnoreCase(hashOriginalMD5)) {
                System.out.println("[INTEGRIDADE] SUCESSO: Os hashes são idênticos. Arquivo transferido perfeitamente");
            } else {
                System.out.println("[INTEGRIDADE] ERRO: Os hashes diferem! O arquivo pode estar corrompido.");
            }
        } catch (Exception e) {
            System.err.println("[INTEGRIDADE] Não foi possível calcular o MD5: " + e.getMessage());
        }

        // Exibe o relatório de encerramento
        exibirEstatisticas();
    }

    // =========================================================================
    // MÉTODOS AUXILIARES (ESTATÍSTICAS, AUXILIARES E HASH)
    // =========================================================================

    /**
     * Envia um pacote ACK simples contendo apenas o número de confirmação especificado.
     */
    private static void enviarAckGenerico(DatagramSocket socket, SocketAddress endereco, int ackNum) throws IOException {
        PacoteGBN ack = new PacoteGBN(PacoteGBN.TYPE_ACK, 0, ackNum, null);
        byte[] bytes = ack.paraBytes();
        socket.send(new DatagramPacket(bytes, bytes.length, endereco));
    }

    /**
     * Calcula o hash MD5 de um arquivo em disco de forma eficiente.
     */
    public static String calcularHashMD5(String pathArquivo) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        try (FileInputStream fis = new FileInputStream(pathArquivo)) {
            byte[] buffer = new byte[8192]; // Buffer de leitura otimizado de 8KB
            int bytesLidos;
            while ((bytesLidos = fis.read(buffer)) != -1) {
                md.update(buffer, 0, bytesLidos);
            }
        }
        
        // Converte o array de bytes do resumo criptográfico para representação hexadecimal
        byte[] hashBytes = md.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b : hashBytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    /**
     * Renderiza o painel final com as estatísticas exigidas pelo projeto.
     */
    private static void exibirEstatisticas() {
        double taxaPerdaEfetiva = 0.0;
        if (totalPacotesRecebidos > 0) {
            taxaPerdaEfetiva = ((double) totalPacotesDescartados / totalPacotesRecebidos) * 100;
        }

        System.out.println("\n==================================================");
        System.out.println("         ESTATÍSTICAS FINAIS DA TRANSFERÊNCIA     ");
        System.out.println("==================================================");
        System.out.println(" Total de pacotes de dados processados : " + totalPacotesRecebidos);
        System.out.println(" Total de pacotes simulados como perda: " + totalPacotesDescartados);
        System.out.printf(" Taxa de perda efetiva na sessão       : %.2f%%\n", taxaPerdaEfetiva); 
        System.out.println("==================================================\n");
    }
}