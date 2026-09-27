package org.example;

import org.example.model.Ponto;

public class TestePonto {
    public static void main(String[] args) {
        Ponto p1 = new Ponto(200,200);
        Ponto p2 = new Ponto(430,230);

        System.out.println("Coordenadas do primeiro ponto (x,y): (" + p1.getX() + ", " + p1.getY() +")");
        System.out.println("Coordenadas do segundo ponto (x,y): (" + p2.getX() + ", " + p2.getY() +")\n");

        System.out.println("Criação de uma segunda referência,chamada refp2");
        Ponto refp2 = p2;

        System.out.println("Coordenadas do primeiro ponto (x,y): (" + p1.getX() + ", " + p1.getY() +")");
        System.out.println("Coordenadas do segundo ponto (x,y): (" + p2.getX() + ", " + p2.getY() +")\n");
        System.out.println("Coordenadas do objeto apontado pela referência refp2 (x,y): (" + refp2.getX() + ", " + refp2.getY() +")\n");

        System.out.println("Alterando as coordenadas do segundo ponto para (840,350)\n");
        refp2.setX(840);
        refp2.setY(350);

        System.out.println("Coordenadas do primeiro ponto (x,y): (" + p1.getX() + ", " + p1.getY() +")");
        System.out.println("Coordenadas do segundo ponto (x,y): (" + p2.getX() + ", " + p2.getY() +")");
        System.out.println("Coordenadas do objeto apontado pela referência refp2 (x,y): (" + refp2.getX() + ", " + refp2.getY() +")");

    }
}