package episodio21;

public class endereco {
    private String rua;
    private int numero;
    private String complemento;
    private String cep;
    private String bairro;
    private String cidade;

    public endereco(String rua,int numero,String complemento,String cep,String bairro,String cidade) {
        this.rua = rua;
        this.numero = numero;
        this.complemento = complemento;
        this.cep = cep;
        this.bairro = bairro;
        this.cidade = cidade;

    }

    public endereco(String rua,int numero,String complemento) {
        this.rua = rua;
        this.numero = numero;
        this.complemento = complemento;
    }


}
