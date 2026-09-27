package org.example;
import org.example.model.v1.Banco;
import org.example.model.v1.Cliente;
import org.example.model.v1.Conta;

public class TesteBancoV1 {
    public static void main(String[] args) {
        Banco banco = new Banco();

        // Criação Clientes
        Cliente messi = new Cliente("Lionel","Messi");
        Cliente neymar = new Cliente("Neymar","Junior");
        Cliente suarez = new Cliente("Luiz","Suarez");

        // Adicionando ao Banco
        banco.adicionarCliente(messi);
        banco.adicionarCliente(neymar);
        banco.adicionarCliente(suarez);

        // Adicionando saldo as contas
        banco.getCliente(0).setConta(new Conta(100000));
        banco.getCliente(1).setConta(new Conta(110000));
        banco.getCliente(2).setConta(new Conta(90000));

        // Impressão
        for(int i = 0;i < banco.getNumeroDeClientes();i++){
            Cliente tmp = banco.getCliente(i);
            System.out.println("Cliente ["+ (i + 1) + "] :"+tmp.getNome() + " " + tmp.getSobrenome()+". Saldo R$:"+tmp.getConta().getSaldo());
        }

    }
}