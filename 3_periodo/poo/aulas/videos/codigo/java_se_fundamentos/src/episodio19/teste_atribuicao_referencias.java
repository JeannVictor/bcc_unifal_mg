package episodio19;

public class TesteAtribuicaoReferencias {
    public static void main(String[] args){
        Hospede h1 = new Hospede("Neymar","Junior");
        Hospede h2= new Hospede("Neymar","Junior");
        System.out.println("Exibindo os dados antes da alteração");
        System.out.println("Hospede h1...."+ h1.getNome()  + " "+ h1.getSobrenome());
        System.out.println("Hospede h2...."+ h2.getNome()  + " "+ h2.getSobrenome());

        System.out.println();

        System.out.println("Exibindo os dados depois da alteração");

        h1.setNome("Luiz");
        h1.setSobrenome("Suarez");
        System.out.println("Hospede h1...."+ h1.getNome()  + " "+ h1.getSobrenome());
        System.out.println("Hospede h2...."+ h2.getNome()  + " "+ h2.getSobrenome());

        System.out.println();

        mudaHospede(h1);
        System.out.println("Hospede modificado...."+ h1.getNome()  + " "+ h1.getSobrenome());
    }

    static void mudaHospede(Hospede h2) {
        h2.setNome("Meliodas");
        h2.setSobrenome("King");
    }
}
