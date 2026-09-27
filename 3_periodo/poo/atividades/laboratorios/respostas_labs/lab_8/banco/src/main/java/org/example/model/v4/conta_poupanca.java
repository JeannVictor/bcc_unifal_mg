package org.example.model.v4;

public class ContaPoupanca extends Conta {
    private double taxaRendimento;

    public ContaPoupanca(double taxaRendimento,double saldoInicial) {
        super(saldoInicial);
        this.taxaRendimento = taxaRendimento;
    }
    public double getTaxaRendimento() {
        return taxaRendimento;
    }
    public void setTaxaRendimento(double taxaRendimento) {
        this.taxaRendimento = taxaRendimento;
    }
}
