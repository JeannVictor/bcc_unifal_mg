package episodio18;

public class TesteIniciacaoVariaveis {
    byte vb;
    short vs;
    int vi;
    long vl;
    String vString;
    float vFloat;
    double vDouble;
    char vChar;

    void metodo1(){
        boolean vBoolean;
        System.out.println("Valor inicial byte: " +vb);
        System.out.println("Valor inicial short: " +vs);
        System.out.println("Valor inicial int: " +vi);
        System.out.println("Valor inicial long: " +vl);
        System.out.println("Valor inicial String: " +vString);
        System.out.println("Valor inicial float: " +vFloat);
        System.out.println("Valor inicial double: " +vDouble);
        System.out.println("Valor inicial char: " +vChar);

    }

    public static void main(String[] args){
        TesteIniciacaoVariaveis teste = new TesteIniciacaoVariaveis();
        teste.metodo1();
    }

}
