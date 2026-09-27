package org.example;
import org.example.model.v1.Banco;
import org.example.model.v1.Cliente;
import org.example.model.v1.ContaCorrente;
import org.example.model.v1.ContaPoupanca;

public class TesteBancoV1 {
    public static void main(String[] args) {

        Banco banco = new Banco();

        // Criação Clientes
        Cliente bruno = new Cliente("Bruno","Henrique");
        Cliente everton = new Cliente("Everton","Ribeiro");
        Cliente filipe = new Cliente("Filipe","Luiz");
        Cliente gabriel = new Cliente("Gabriel","Barbosa");
        Cliente diego = new Cliente("Diego","Alves");
        Cliente lorena = new Cliente("Lorena","Lara");

        // Adicionando ao Banco
        banco.adicionarCliente(bruno);
        banco.adicionarCliente(everton);
        banco.adicionarCliente(filipe);
        banco.adicionarCliente(gabriel);
        banco.adicionarCliente(diego);
        banco.adicionarCliente(lorena);

        // Adicionando saldo as contas
        banco.getCliente(0).setConta(new ContaPoupanca( 50000,3));
        banco.getCliente(1).setConta(new ContaCorrente(45000,30000));
        banco.getCliente(2).setConta(new ContaCorrente(70000,0));
        banco.getCliente(3).setConta(new ContaPoupanca(220000,3));
        banco.getCliente(4).setConta(new ContaCorrente(50000,0));

        System.out.println("----------------- CRIAÇÃO DE CONTAS BANCÁRIAS -------------------");
        System.out.println("Criando uma conta poupança para o cliente Bruno Henrique com saldo de R$ 50.000,00 e taxa de rendimentos de 3%");
        System.out.println("Criando uma conta corrente para o cliente Everton Ribeiro com saldo de R$ 45.000,00 e cheque especial de R$ 30.000,00");
        System.out.println("Criando uma conta corrente para o cliente Filipe Luis com saldo de R$ 70.000,00 e sem cheque especial.");
        System.out.println("Criando uma conta poupança para o cliente Gabriel Barbosa com saldo de R$ 220.000,00 e taxa de rendimentos de 3%");
        System.out.println("Criando uma conta corrente para o cliente Diego Alves com saldo de R$ 50.000,00 e sem cheque especial.\n");

        System.out.println("----------------- RELATÓRIO DE TRANSAÇÕES -------------------");
        System.out.println("Recuperando o cliente " + banco.getCliente(0).getNome() +" "+banco.getCliente(0).getSobrenome());
        System.out.println("Sacando R$ 1.200,00: " + banco.getCliente(0).getConta().sacar(1200));
        System.out.println("Depositando R$ 8.525,00: " + banco.getCliente(0).getConta().depositar(8525));
        System.out.println("Sacando R$ 12.800,00: " + banco.getCliente(0).getConta().sacar(12800));
        System.out.println("Sacando R$ 50.000,00: " + banco.getCliente(0).getConta().sacar(50000));
        System.out.println("Cliente [" + banco.getCliente(0).getNome() +" "+banco.getCliente(0).getSobrenome()+"] tem o saldo de R$ " + banco.getCliente(0).getConta().getSaldo());
        System.out.println();

        System.out.println("Recuperando o cliente " + banco.getCliente(1).getNome() +" "+banco.getCliente(1).getSobrenome());
        System.out.println("Sacando R$ 12.500,00: " + banco.getCliente(1).getConta().sacar(12500));
        System.out.println("Sacando R$ 18.500,00: " + banco.getCliente(1).getConta().sacar(18500));
        System.out.println("Depositando R$ 3.500,00: " + banco.getCliente(1).getConta().depositar(3500));
        System.out.println("Sacando R$ 17.000,00: " + banco.getCliente(1).getConta().sacar(17000));
        System.out.println("Sacando R$ 25.000,00: " + banco.getCliente(1).getConta().sacar(25000));
        System.out.println("Cliente [" + banco.getCliente(1).getNome() +" "+banco.getCliente(1).getSobrenome()+"] tem o saldo de R$ " + banco.getCliente(1).getConta().getSaldo());
        System.out.println();

        System.out.println("Recuperando o cliente " + banco.getCliente(2).getNome() +" "+banco.getCliente(2).getSobrenome());
        System.out.println("Sacando R$ 25.500,00: " + banco.getCliente(2).getConta().sacar(25500));
        System.out.println("Depositando R$ 2.000,00: " + banco.getCliente(2).getConta().depositar(2000));
        System.out.println("Sacando R$ 37.200,00: " + banco.getCliente(2).getConta().sacar(37200));
        System.out.println("Sacando R$ 15.000,00: " + banco.getCliente(2).getConta().sacar(15000));
        System.out.println("Cliente [" + banco.getCliente(2).getNome() +" "+banco.getCliente(2).getSobrenome()+"] tem o saldo de R$ " + banco.getCliente(2).getConta().getSaldo());
        System.out.println();

        System.out.println("Recuperando o cliente " + banco.getCliente(3).getNome() +" "+banco.getCliente(3).getSobrenome());
        System.out.println("Sacando R$ 15.500,00: " + banco.getCliente(3).getConta().sacar(15500));
        System.out.println("Depositando R$ 3.000,00: " + banco.getCliente(3).getConta().depositar(3000));
        System.out.println("Sacando R$ 23.400,00: " + banco.getCliente(3).getConta().sacar(23400));
        System.out.println("Sacando R$ 17.000,00: " + banco.getCliente(3).getConta().sacar(17000));
        System.out.println("Cliente [" + banco.getCliente(3).getNome() +" "+banco.getCliente(3).getSobrenome()+"] tem o saldo de R$ " + banco.getCliente(3).getConta().getSaldo());
        System.out.println();

        System.out.println("Recuperando o cliente " + banco.getCliente(4).getNome() +" "+banco.getCliente(4).getSobrenome());
        System.out.println("Sacando R$ 28.000,00: " + banco.getCliente(4).getConta().sacar(28000));
        System.out.println("Depositando R$ 3.000,00: " + banco.getCliente(4).getConta().depositar(3000));
        System.out.println("Sacando R$ 17.000,00: " + banco.getCliente(4).getConta().sacar(17000));
        System.out.println("Cliente [" + banco.getCliente(4).getNome() +" "+banco.getCliente(4).getSobrenome()+"] tem o saldo de R$ " + banco.getCliente(4).getConta().getSaldo());
        System.out.println();

        System.out.println("Recuperando o cliente " + banco.getCliente(5).getNome() +" "+banco.getCliente(5).getSobrenome());
        System.out.println("Sacando R$ 32.000,00: " + banco.getCliente(4).getConta().sacar(32000));
        System.out.println("Depositando R$ 13.000,00: " + banco.getCliente(4).getConta().depositar(13000));
        System.out.println("Sacando R$ 16.600,00: " + banco.getCliente(4).getConta().sacar(16600));
        System.out.println("Cliente [" + banco.getCliente(5).getNome() +" "+banco.getCliente(5).getSobrenome()+"] tem o saldo de R$ " + banco.getCliente(4).getConta().getSaldo());

    }
}