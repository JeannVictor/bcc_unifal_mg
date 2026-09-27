package org.example.banco;

import java.util.ArrayList;

public class Cliente {
    private String nome;
    private String sobrenome;
    private ArrayList<Conta> contas;

    public Cliente(String nome, String sobrenome) {
        this.nome = nome;
        this.sobrenome = sobrenome;
        this.contas = new ArrayList<>();
    }

    public String getNome() {
        return nome;
    }
    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getSobrenome() {
        return sobrenome;
    }

    public void setSobrenome(String sobrenome) {
        this.sobrenome = sobrenome;
    }

    public void adicionarConta(Conta conta) {
        this.contas.add(conta);

    }

    public Conta getConta(int id) {
        for(int i = 0; i < contas.size(); i++){
            if(i == id){
                return contas.get(i);
            }
        }
        return null;
    }

    public int getNumeroDeContas() {
        return contas.size();
    }
}