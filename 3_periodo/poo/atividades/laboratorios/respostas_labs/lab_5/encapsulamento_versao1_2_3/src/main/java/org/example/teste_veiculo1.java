package org.example;

import org.example.model.v1.Veiculo;

public class TesteVeiculo1 {
    public static void main(String[] args) {

        Veiculo veiculo = new Veiculo(10000);

        System.out.println("Criando um veículo com carga máxima de 10.000kg");
        System.out.println("Adicionando Caixa número 1 (500kg)");
        veiculo.setCarga(500);

        System.out.println("Adicionando Caixa número 2 (250kg)");
        veiculo.setCarga(250);

        System.out.println("Adicionando Caixa número 3 (5000kg)");
        veiculo.setCarga(5000);

        System.out.println("Adicionando Caixa número 4 (4000kg)");
        veiculo.setCarga(4000);

        System.out.println("Adicionando Caixa número 5 (300kg)");
        veiculo.setCarga(300);

        System.out.println("A carga do veículo é :"+ veiculo.getCarga());

    }
}