import java.io.IOException;
import java.util.Scanner;
import repl.REPL;
public class Main {

    public static void main(String[] args) {
        String userName = System.getProperty("user.name");

        System.out.printf("Hello %s! This is the Monkey programming language!\n", userName);
        System.out.println("Feel free to type in commands");

        REPL.start();
    }
}
