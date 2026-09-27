public class TestGreeting {
    public static void main(String[] args) {
        Greeting mensagem = new Greeting(); // Cria uma instância da classe Greeting
        String message = mensagem.message(); // Chama o método message()
        System.out.println(message); // Imprime a mensagem
    }
}
