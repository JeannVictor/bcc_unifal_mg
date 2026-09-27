package episodio21;

import java.util.Date;

public class Hospede {

    private String nome;
    private String sobrenome;
    private double salario;
    private endereco end;

    public endereco getEnd() {
        return end;
    }

    public void setEnd(endereco end) {
        this.end = end;
    }

    public Hospede() {
    }

    public Hospede(String nome) {
        this.nome = nome;
    }

    public Hospede(String nome, String sobrenome) {
        this.nome = nome;
        this.sobrenome = sobrenome;
    }

    public String getNome() {
        int idade = 10; // Variavel local ao bloco
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


}
