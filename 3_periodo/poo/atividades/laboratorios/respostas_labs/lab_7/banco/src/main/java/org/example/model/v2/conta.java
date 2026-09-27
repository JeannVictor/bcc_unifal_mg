package org.example.model.v2;

public class Conta {
    private double saldo;

    public Conta(double saldoInicial){
        this.saldo = saldoInicial;
    }

    public double getSaldo() {
        return saldo;
    }

    public boolean depositar(double valor){
        if(valor > 0){
            this.saldo += valor;
            return true;
        }else{
            return false;
        }
    }

    public boolean sacar(double ammount){
        if(ammount > saldo || ammount < 0){
            return false;
        }else{
            saldo = saldo - ammount;
            return true;
        }
    }

}