package org.example;

import org.example.model.v4.Banco;
import org.example.model.v4.Cliente;
import org.example.model.v4.ContaCorrente;
import org.example.model.v4.ContaPoupanca;
import org.example.model.v4.Conta;

public class TesteBancoV4 {

    public static void main(String[] args) {
        TesteBancoV4 testeBanco = new TesteBancoV4();
        Banco banco = new Banco();
        ContaPoupanca poupanca;
        ContaCorrente corrente;

        // Cria vários clientes e suas respectivas contas
        System.out.println("\nCriando uma conta conta poupança com saldo de R$ 50.000,00 " +
                "para o cliente Bruno Henrique.");
        Cliente brunoHenrique = new Cliente("Bruno", "Henrique");
        poupanca = new ContaPoupanca(50000.00, 0.03);

        System.out.println("\nCriando uma conta corrente com saldo de R$ 220.000,00" +
                " para o cliente Bruno Henrique.");
        corrente = new ContaCorrente(220000.00, poupanca);

        banco.adicionarCliente(brunoHenrique);
        Cliente cliente = banco.getCliente(0); // Demonstrando que após adicionado, podemos obter o cliente
        // caso saibamos o indice dele lista de clientes do banco

        cliente.setContaPoupanca(poupanca);
        cliente.setContaCorrente(corrente);

        // Criação do cliente Diego Alves e sua respectiva conta corrente sem proteção de conta poupança
        System.out.println("\nCriando uma conta corrente com saldo de R$ 50.000,00 para o cliente Diego Alves, sem conta poupança de proteção ");
        Cliente diegoAlves = new Cliente("Diego", "Alves");
        corrente = new ContaCorrente(50000.0);
        diegoAlves.setContaCorrente(corrente);
        banco.adicionarCliente(diegoAlves);

        System.out.println("\nContas criadas com sucesso");

        // Demonstração do comportamento dos vários tipos de conta
        System.out.println("\n------------------ RELATÓRIO DE TRANSAÇÕES -------------------");

        System.out.println("Recuperando o cliente Bruno Henrique");
        cliente = banco.getCliente(0);
        Conta contaCorrente = cliente.getContaCorrente();
        Conta contaPoupanca = cliente.getContaCorrente();

        // Executa algumas transações na conta
        System.out.println("Sacando R$ 230.000,00: " + contaCorrente.sacar(230000));
        System.out.println("Depositando R$ 8.525,00: " + contaCorrente.depositar(8525));
        System.out.println("Sacando R$ 12.800,00: " + contaCorrente.sacar(12800) );
        System.out.println("Sacando R$ 40.000,00: " + contaCorrente.sacar(40000) );
        testeBanco.exibirContasDoCliente(cliente);

        // Testando uma conta corrente sem conta poupança de proteção
        System.out.println("Recuperando o cliente Diego Alves");
        cliente = banco.getCliente(1);
        contaCorrente = cliente.getContaCorrente();

        // Executa algumas transações
        System.out.println("Saque de R$ 12.500,00: " + contaCorrente.sacar(12500.00));
        System.out.println("Saque de R$ 18.500,00: " + contaCorrente.sacar(18500.00));
        System.out.println("deposito de R$ 3.500,00: " + contaCorrente.depositar(3500.00));
        System.out.println("Saque de R$ 17.000,00: " + contaCorrente.sacar(17000.00));
        System.out.println("Saque de R$ 25.000,00: " + contaCorrente.sacar(25000.00));
        testeBanco.exibirContasDoCliente(cliente);
    }

    private void exibirContasDoCliente(Cliente cliente) {
        ContaCorrente contaCorrente = cliente.getContaCorrente();
        ContaPoupanca contaPoupanca = cliente.getContaPoupanca();

        String resultado = "Cliente [" + cliente.getNome()
                + ", " + cliente.getSobrenome()
                + "]";
        if (contaCorrente != null)
            resultado += " tem uma conta corrente com saldo R$ " + cliente.getContaCorrente().getSaldo();
        if (contaPoupanca != null)
            resultado += " \ne uma proteção em conta poupança com saldo R$ " + cliente.getContaPoupanca().getSaldo();

        System.out.println(resultado);
    }
}


