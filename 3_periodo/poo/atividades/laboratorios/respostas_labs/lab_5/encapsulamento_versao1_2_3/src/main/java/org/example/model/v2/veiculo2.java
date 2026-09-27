package org.example.model.v2;

public class Veiculo2 {
    public double carga;
    public double cargaMaxima;

    public Veiculo2(double cargaMaxima){
        this.cargaMaxima = cargaMaxima;
    }

    public double getCarga() {
        return carga;
    }

    public void setCarga(double carga) {
        this.carga += carga;
    }

    public double getCargaMaxima() {
        return cargaMaxima;
    }

    public void setCargaMaxima(double cargaMaxima) {
        this.cargaMaxima = cargaMaxima;
    }

    public boolean adicionarCaixa(double peso){
        if((peso + carga) > cargaMaxima){
            return false;
        }else{
            carga = carga + peso;
            return true;
        }
    }

}