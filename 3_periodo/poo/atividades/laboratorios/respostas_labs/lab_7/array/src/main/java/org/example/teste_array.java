package org.example;

import java.util.Arrays;

public class TesteArray {
    public static void main(String[] args) {

    // Arrays Simples
        int[] array1 = {2,3,5,7,11,13,17,19};
        exibirArray(array1);
        System.out.println();

        int[] array2 = array1;
        for (int i = 0; i < array2.length; i++) {
            if( i % 2 == 0)
                array2[i] = i;
        }
        exibirArray(array1);
        System.out.println();

    // Arrays Multidimensionais
        int[][] matriz = new int[5][];
        for (int i = 0; i < matriz.length; i++) {
            matriz[i] = new int[i];
            for (int j = 0; j < matriz[i].length; j++) {
                matriz[i][j] = i*j;
            }
            exibirArray(matriz[i]);
            System.out.println();
        }
        System.out.println();

    // Classe java.util.Arrays
        System.out.println("Impressão do Array1: "+ Arrays.toString(array1));
        System.out.println("Impressão do Array2: "+ Arrays.toString(array2));
        System.out.println("Impressão da Matriz: "+ Arrays.deepToString(matriz));

    }

    public static void exibirArray(int[] array) {
        System.out.print("<");
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i]);
            if ((i+1) < array.length) {
                System.out.print(", ");
            }
        }
        System.out.print(">");
    }

}