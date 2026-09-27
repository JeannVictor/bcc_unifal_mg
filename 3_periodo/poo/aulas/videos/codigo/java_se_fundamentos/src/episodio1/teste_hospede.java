package episodio1;

public class TesteHospede {
    public static void main(String[] args){

        Hospede jeann = new Hospede();
        jeann.setNome("Jeann");
        jeann.setSobrenome("Victor Batista");
        System.out.println("Nome: " +jeann.getNome() + "  Sobrenome: " +  jeann.getSobrenome());

        Hospede dalton = new Hospede();
        dalton.setNome("Dalton");
        dalton.setSobrenome("D´Angelis Sacramento");
        System.out.println("Nome: " +dalton.getNome() + "  Sobrenome: " +  dalton.getSobrenome());
    }
}
