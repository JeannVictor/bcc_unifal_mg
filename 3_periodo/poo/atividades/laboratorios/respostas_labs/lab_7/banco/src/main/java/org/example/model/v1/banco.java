package org.example.model.v1;

public class Banco {
    private Cliente[] clientes;
    private int numeroDeClientes;

    public Banco() {
        this.clientes = new Cliente[3];
        this.numeroDeClientes = 0;
    }

    public void adicionarCliente(Cliente cliente) {
        if(numeroDeClientes < clientes.length) {
            this.clientes[numeroDeClientes] = cliente;
        }
        numeroDeClientes++;
    }

    public Cliente getCliente(int indice) {
        if(indice >= 0 && indice < clientes.length) {
            return clientes[indice];
        }else{
            return null;
        }
    }

    public int getNumeroDeClientes() {
        return numeroDeClientes;
    }

}
