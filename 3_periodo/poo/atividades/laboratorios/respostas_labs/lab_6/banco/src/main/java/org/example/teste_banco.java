package org.example;

import org.example.model.Cliente;
import org.example.model.Conta;

public class TesteBanco {
    public static void main(String[] args) {

        Cliente messi = new Cliente("Lionel","Messi");
        System.out.println("Criando o cliente " +messi.getNome() +  " " +messi.getSobrenome());

        Conta messic = new Conta(50000);
        System.out.println("Criando uma conta com o saldo de R$ 50.000,00  para o cliente " +messi.getNome() +  " " +messi.getSobrenome());

        System.out.println("Sacando  R$ 1200,00:" + messic.sacar(1200));
        System.out.println("Depositando  R$ 8525,00:" + messic.depositar(8525));
        System.out.println("Sacando  R$ 12.800,00:" + messic.sacar(12800));
        System.out.println("Sacando  R$ 50.000,00:"+messic.sacar(50000));

        System.out.println("O saldo da conta é: R$ " + messic.getSaldo());


    }
}