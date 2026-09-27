package org.example.model.v3;

public class Veiculo3 {
    public double carga;
    public double cargaMaxima;

    public Veiculo3(double cargaMaxima){
        this.cargaMaxima = quilosParaNewtons(cargaMaxima);
    }

    public double getCarga() {
        return newtonsParaQuilos(carga);
    }

    public double getCargaMaxima() {
        return quilosParaNewtons(cargaMaxima);
    }

    public boolean adicionarCaixa(double peso){
        if((quilosParaNewtons(peso) + carga) > cargaMaxima){
            return false;
        }else{
            carga = carga + quilosParaNewtons(peso);
            return true;
        }
    }

    public double newtonsParaQuilos (double peso){
        peso = peso / 9.8;
        return peso;
    }

    public double quilosParaNewtons(double peso){
        peso = peso * 9.8;
        return peso;
    }

}