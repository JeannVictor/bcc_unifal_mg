package episodio19;

import java.util.Date;

public class Hospede {

    private String nome;
    private String sobrenome;
    private double salario;

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

    /**
     * Este método é crucial para a estabilidade da classe hóspede
     * Caso queira entender com maiores detalhes sua logica de implementação
     * consulte o documento de espercificação de requisitos do sistema
     * @param numeroGrande de acordo com a espercificação IEEE para números flutuantes
     * @deprecated Favor utilizar este metodo somente em ultima instancia
     * prefira o método metodoMUitoComplexoAtualizado
     *
     */
    public void metodoMuitoComplexo(double numeroGrande) {
        Date hoje = new Date();
    }
}
