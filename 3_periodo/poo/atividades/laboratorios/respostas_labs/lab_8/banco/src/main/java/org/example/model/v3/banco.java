package org.example.model.v3;

import java.util.ArrayList;

public class Banco {
    private ArrayList<Cliente> clientes;

    public Banco() {
        this.clientes = new ArrayList<>();

    }

    public void adicionarCliente(Cliente cliente) {
        this.clientes.add(cliente);
    }

    public ArrayList<Cliente> getCliente(String nome, String sobrenome) {
        ArrayList<Cliente> encontrados = new ArrayList<>();
        for (int i = 0; i < clientes.size(); i++) {
            Cliente c = clientes.get(i);
            if (c.getNome().equals(nome) && c.getSobrenome().equals(sobrenome)) {
                encontrados.add(c);
            }
        }
        return encontrados;
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
