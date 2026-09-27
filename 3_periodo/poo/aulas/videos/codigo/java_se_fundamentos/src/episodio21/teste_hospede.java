package episodio21;

public class TesteHospede {
    public static void main(String[] args) {

        endereco end1 = new endereco("Rua Salinas",549,"A");

        // Hospede Jeann
        Hospede jeann = criarHospede("Jeann","Victor Batista");
        jeann.setEnd(end1);
        exibirDados(jeann);
        // Hospede Dalton
        Hospede dalton = criarHospede("Dalton","D`Angelis Sacramento");
        exibirDados(dalton);
        // Hospede Nicolau
        Hospede nicolau = criarHospede("Nicolas","RTO");
        exibirDados(nicolau);
        // Hospede Messi
        Hospede messi = criarHospede("Lionel","Messi");
        exibirDados(messi);
    }

    public static Hospede criarHospede(String nome, String sobrenome){
        return new Hospede(nome,sobrenome);
    }

    public static void exibirDados(Hospede x){
        System.out.println("Nome: " + x.getNome() + "  Sobrenome: " + x.getSobrenome());
        System.out.println("Endereço: "+x.getEnd());
    }

}
