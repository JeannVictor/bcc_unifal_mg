package org.example.model;

public class Conta {
    private double saldo;

    public Conta(double saldoInicial){
        this.saldo = saldoInicial;
    }

    public double getSaldo() {
        return saldo;
    }

    public double depositar(double valor){
        saldo = saldo + valor;
        return saldo;
    }

    public double sacar(double ammount){
        if(ammount > saldo){
            System.out.println("Não foi possivel sacar R$ " + ammount + " ,pois sua conta possui saldo de apenas R$ " + getSaldo());
            return saldo;
        }else{
            saldo = saldo - ammount;
            return saldo;
        }
    }

}
