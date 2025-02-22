// lexer/Lexer.java
package lexer;

import token.Token;
import token.TokenType;

public class Lexer {
    private final String input;
    private int position = 0;
    private int readPosition = 0;
    private char ch;

    public Lexer(String input) {
        this.input = input;
        readChar();
    }

    private void readChar() {
        if (readPosition >= input.length()) {
            ch = 0; // ASCII code for NUL (EOF equivalent)
        } else {
            ch = input.charAt(readPosition);
        }
        position = readPosition;
        readPosition += 1;
    }

    public Token nextToken() {
        Token tok;
        switch (ch) {
            case '=':
                tok = new Token(TokenType.ASSIGN, String.valueOf(ch));
                break;
            case '+':
                tok = new Token(TokenType.PLUS, String.valueOf(ch));
                break;
            case '(':
                tok = new Token(TokenType.LPAREN, String.valueOf(ch));
                break;
            case ')':
                tok = new Token(TokenType.RPAREN, String.valueOf(ch));
                break;
            case '{':
                tok = new Token(TokenType.LBRACE, String.valueOf(ch));
                break;
            case '}':
                tok = new Token(TokenType.RBRACE, String.valueOf(ch));
                break;
            case ',':
                tok = new Token(TokenType.COMMA, String.valueOf(ch));
                break;
            case ';':
                tok = new Token(TokenType.SEMICOLON, String.valueOf(ch));
                break;
            case 0:
                tok = new Token(TokenType.EOF, "");
                break;
            default:
                tok = new Token(TokenType.ILLEGAL, String.valueOf(ch));
        }
        readChar();
        return tok;
    }
    public static void main(String[] args) {
        String input="=+(){},;";
        Lexer obj=new Lexer(input);
        for(int i=0;i<input.length();i++){
            Token x=obj.nextToken();
            if(x.type.equals("ILLEGAL")){
                System.out.println(i+" "+"wefneskjhgfishgkiebshkigbibrskdjgkdfjbgkdfnhbg");
            }else{

                System.out.println(x.type+" "+x.literal);
            }
        }
        System.out.println();
    }
   
}
