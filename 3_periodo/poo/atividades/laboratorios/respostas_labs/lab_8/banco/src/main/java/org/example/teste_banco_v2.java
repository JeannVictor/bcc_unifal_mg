package org.example;

import org.example.model.v2.*;

public class TesteBancoV2 {

  public static void main(String[] args) {
    Banco banco = new Banco();
    Cliente cliente;

    // Cria vários clientes e suas respectivas contas
    Cliente brunoHenrique = new Cliente("Bruno", "Henrique");
    banco.adicionarCliente(brunoHenrique);
    cliente = banco.getCliente(0);
    cliente.adicionarConta(new ContaPoupanca(50000.00, 0.03));
    cliente.adicionarConta(new ContaCorrente(220000.00, 40000.00));

    Cliente evertonRibeiro = new Cliente("Everton", "Ribeiro");
    banco.adicionarCliente(evertonRibeiro);
    cliente = banco.getCliente(1);
    cliente.adicionarConta(new ContaCorrente(45000, 30000.00));

    Cliente filipeLuis = new Cliente("Filipe", "Luis");
    banco.adicionarCliente(filipeLuis);
    cliente = banco.getCliente(2);
    cliente.adicionarConta(new ContaPoupanca(150000.00, 0.03));
    cliente.adicionarConta(new ContaCorrente(70000));

    Cliente gabrielBarbosa = new Cliente("Gabriel", "Barbosa");
    banco.adicionarCliente(gabrielBarbosa);
    cliente = banco.getCliente(3);
    cliente.adicionarConta(banco.getCliente(2).getConta(1));
    cliente.adicionarConta(new ContaPoupanca(220000.00, 0.03));

      // Gera um Relatório
    System.out.println("\t\t\tRELATÓRIO DE CLIENTES");
    System.out.println("\t\t\t================");
    cliente = null;

    for (int i = 0; i < banco.getNumeroDeClientes(); i++ ){
      cliente = banco.getCliente(i);
      System.out.println();
      System.out.println("Cliente: " + cliente.getSobrenome() + ", "+ cliente.getNome());
      for (int j = 0; j < cliente.getNumeroDeContas(); j++ ) {
      	Conta conta = cliente.getConta(j);
	    String  tipoConta = "";
        if(conta instanceof ContaCorrente){
          tipoConta = "Conta Corrente";
        }else{
          tipoConta = "Conta Poupanca";
        }
        // Exibe o saldo da conta
        System.out.println("O saldo da " + tipoConta + " é de R$ " + conta.getSaldo());
      }
    }
  }
}