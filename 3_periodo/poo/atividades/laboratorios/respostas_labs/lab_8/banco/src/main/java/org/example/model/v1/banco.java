package org.example.model.v1;

import java.util.ArrayList;

public class Banco {
    private ArrayList<Cliente> clientes;
    private int numeroDeClientes;

    public Banco() {
        this.clientes = new ArrayList<>();
        this.numeroDeClientes = 0;
    }

    public void adicionarCliente(Cliente cliente) {
        this.clientes.add(cliente);
        numeroDeClientes++;
    }

    public Cliente getCliente(int indice) {
        if(indice >= 0 && indice < clientes.size()) {
            return clientes.get(indice);
        }
        return null;
    }

    public int getNumeroDeClientes() {
        return clientes.size();
    }

}
