package repl;

import java.util.Scanner;
import lexer.Lexer;
import token.Token;
public class REPL {

    private static final String PROMPT = ">> ";

    public static void start() {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print(PROMPT);

            if (!scanner.hasNextLine()) {
                scanner.close();
                return;
            }

            String line = scanner.nextLine();

            Lexer lexer = new Lexer(line);
            while (true) {
                Token x = lexer.nextToken();
                if (x.type.equals("EOF")) break;
                if (x.type.equals("ILLEGAL")) {
                    System.out.println("ILLEGAL token at: " + x.literal);
                    break;
                } else {
                    System.out.println(x.type + " " + x.literal);
                }
            }
        }
    }


    public static void main(String[] args) {
        start(); 
    }
}
