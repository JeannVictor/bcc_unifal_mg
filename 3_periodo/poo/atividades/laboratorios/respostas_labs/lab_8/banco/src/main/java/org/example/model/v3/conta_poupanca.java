package org.example.model.v3;

public class ContaPoupanca extends Conta {
    double taxaRendimento;

    public ContaPoupanca(double saldoInicial, double taxaRendimento) {
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
