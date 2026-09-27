package org.example.model.v2;

public class ContaCorrente extends Conta {
    private double chequeEspecial;
    public ContaCorrente(double saldoInicial, double chequeEspecial) {
        super(saldoInicial);
        this.chequeEspecial = chequeEspecial;
    }

    public ContaCorrente(double saldoInicial) {
        super(saldoInicial);
    }

    public double getChequeEspecial() {
        return chequeEspecial;
    }
    public void setChequeEspecial(double chequeEspecial) {
        this.chequeEspecial = chequeEspecial;
    }

    public boolean sacar(double valor) {
        if(valor > chequeEspecial + saldo) {
            return false;
        }
        saldo -= valor;
        return true;
    }
}
