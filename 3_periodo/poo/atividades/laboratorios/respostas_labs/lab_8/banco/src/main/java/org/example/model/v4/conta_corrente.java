package org.example.model.v4;

public class ContaCorrente extends Conta {
    private ContaPoupanca protecaoContaPoupanca;

    public ContaCorrente(Double saldoInicial,ContaPoupanca protecao) {
        super(saldoInicial);
        this.protecaoContaPoupanca = protecao;
    }
    public ContaCorrente(Double saldoInicial) {
        super(saldoInicial);
    }
    @Override
    public boolean sacar(double valor) {
        if (valor <= this.getSaldo()) {
            this.saldo -= valor;
            return true;
        }else if(protecaoContaPoupanca != null && valor <= (this.getSaldo() + protecaoContaPoupanca.getSaldo())){
            double resto = valor - this.getSaldo();
            this.saldo = 0;
            protecaoContaPoupanca.sacar(resto);
            return true;
        }else{
            return false;
        }
    }
    public ContaPoupanca getContaPoupanca() {
        return protecaoContaPoupanca;
    }
    public void setContaPoupanca(ContaPoupanca contaPoupanca) {
        this.protecaoContaPoupanca = contaPoupanca;
    }

}

