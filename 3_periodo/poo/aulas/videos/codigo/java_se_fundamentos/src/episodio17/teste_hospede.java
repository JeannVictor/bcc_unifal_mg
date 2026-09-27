package episodio17;

public class TesteHospede {
    public static void main(String[] args) {

        Hospede jeann = new Hospede("Jeann");
        jeann.setNome("Jeann");
        jeann.setSobrenome("Victor Batista");
        System.out.println("Nome: " + jeann.getNome() + "  Sobrenome: " + jeann.getSobrenome());

        Hospede dalton = new Hospede("Dalton");
        dalton.setNome("Dalton");
        dalton.setSobrenome("D´Angelis Sacramento");
        System.out.println("Nome: " + dalton.getNome() + "  Sobrenome: " + dalton.getSobrenome());

        Hospede francisco = new Hospede("Franscisco");
        francisco.setNome("Francisco");
        francisco.setSobrenome("Melo");
        System.out.println("Nome: " + francisco.getNome() + "  Sobrenome: " + francisco.getSobrenome());

        Hospede thiago = new Hospede("Thiago");
        thiago.setSobrenome("Pereira");
        System.out.println("Nome: " + thiago.getNome() + "  Sobrenome: " + thiago.getSobrenome());

        Hospede julia = new Hospede("Julia", "Silva");
        System.out.println("Nome: " + julia.getNome() + "  Sobrenome: " + julia.getSobrenome());

        Hospede nicolau = new Hospede("Nicolas", "RTO");
        System.out.println("Nome: " + nicolau.getNome() + "  Sobrenome: " + nicolau.getSobrenome());
        // Versão mais clara do que é feito, vantagem de reuso....
        String nomeRetornado = nicolau.getNome();
        String sobrenomeRetornado = nicolau.getSobrenome();
        System.out.println("Nome: " + nomeRetornado + "  Sobrenome: " + sobrenomeRetornado);

        String nome = "Messi";
        System.out.println(nome.toUpperCase()); // Retorna a String em MAIUSCULO
        int retorno = nome.length(); // Retorna o tamanho da String
        System.out.println(retorno);

        Integer numero19 = new Integer(19);
        System.out.println(numero19.MIN_VALUE);

        Hospede lamine = null;
        System.out.println(lamine.getNome());

    }
}
