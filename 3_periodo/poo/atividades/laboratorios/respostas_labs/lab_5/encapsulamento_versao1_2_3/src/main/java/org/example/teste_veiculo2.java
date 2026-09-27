package org.example;

import org.example.model.v2.Veiculo2;

public class TesteVeiculo2 {
    public static void main(String[] args) {

        Veiculo2 veiculo = new Veiculo2(10000);

        System.out.println("Criando um veículo com carga máxima de 10.000kg");
        System.out.println("Adicionando Caixa número 1 (500kg) : " + veiculo.adicionarCaixa(500));
        System.out.println("Adicionando Caixa número 2 (250kg) : " + veiculo.adicionarCaixa(250));
        System.out.println("Adicionando Caixa número 3 (5000kg) : " + veiculo.adicionarCaixa(5000));
        System.out.println("Adicionando Caixa número 4 (4000kg) : " + veiculo.adicionarCaixa(4000));
        System.out.println("Adicionando Caixa número 5 (300kg) : "+ veiculo.adicionarCaixa(300));

        System.out.println("A carga do veículo é : "+ veiculo.getCarga());

    }
}