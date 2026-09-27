package org.example.model.v4;

public class Conta {
    protected double saldo;

    public Conta(double saldoInicial) {
        this.saldo = saldoInicial;
    }
    public double getSaldo() {
        return saldo;
    }
    public boolean sacar(double valor) {
        if (valor <= this.saldo) {
            this.saldo -= valor;
            return true;
        }
        return false;
    }

    public boolean depositar(double valor) {
        if(valor > 0 ){
            this.saldo += valor;
            return true;
        }
        return false;
    }

}
