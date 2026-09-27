package episodio8;

public class TesteHospede {
    public static void main(String[] args){

        Hospede jeann = new Hospede("Jeann");
        jeann.setNome("Jeann");
        jeann.setSobrenome("Victor Batista");
        System.out.println("Nome: " +jeann.getNome() + "  Sobrenome: " +  jeann.getSobrenome());

        Hospede dalton = new Hospede("Dalton");
        dalton.setNome("Dalton");
        dalton.setSobrenome("D´Angelis Sacramento");
        System.out.println("Nome: " +dalton.getNome() + "  Sobrenome: " +  dalton.getSobrenome());

        Hospede francisco =  new Hospede("Franscisco");
        francisco.setNome("Francisco");
        francisco.setSobrenome("Melo");
        System.out.println("Nome: " +francisco.getNome() + "  Sobrenome: " +  francisco.getSobrenome());

        Hospede thiago = new Hospede("Thiago");
        thiago.setSobrenome("Pereira");
        System.out.println("Nome: " +thiago.getNome() + "  Sobrenome: " +  thiago.getSobrenome());

        Hospede julia = new Hospede("Julia","Silva");
        System.out.println("Nome: " +julia.getNome() + "  Sobrenome: " +  julia.getSobrenome());
    }
}
