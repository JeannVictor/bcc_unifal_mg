package org.example.model.v2;

import java.util.ArrayList;

public class Banco {
    private ArrayList<Cliente> clientes;

    public Banco() {
        this.clientes = new ArrayList<>();

    }

    public void adicionarCliente(Cliente cliente) {
        this.clientes.add(cliente);
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
