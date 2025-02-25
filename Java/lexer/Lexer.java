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

    private String readWord(){
        int pos=position;
       
            while(isLetterOrDigit(ch)){
                readChar();
            }
        

        return input.substring(pos,position);
    }

    public void skipWhitespace(){
        while(ch == ' ' || ch == '\n' || ch == '\r' || ch == '\t'){
            readChar();
        }
    }
    public boolean isLetterOrDigit(char ch){
        if((ch >= 'a' && ch <= 'z')||(ch >='A' && ch <= 'Z')|| isDigit(ch) || ch == '_'){
            return true;
        }else{
            return false;
        }
    }
    public boolean isDigit(char ch){
        if(ch >= '0' && ch <= '9'){
            return true;
        }else{
            return false;
        }
    }
    // public char peek(){
    //     if(readPosition >= input.length()) return 0;
    //     return input.charAt(readPosition);
    // }
    public boolean isNumber(String s){
        for(int i=0;i<s.length();i++){
            if(!isDigit(s.charAt(i))){
                return false;
            }
        }
        return true;
    }
    public Token nextToken() {
        Token tok;
        skipWhitespace();
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
                if(isLetterOrDigit(ch)){
                    String word=readWord();
                    // System.out.println(word);
                    if(isNumber(word)){
                       tok=new Token(TokenType.INT,word); 
                    }else if(isDigit(word.charAt(0))){
                        tok=new Token(TokenType.ILLEGAL,word);
                    }else{
                        tok=new Token(TokenType.getIdentType(word),word);
                    }
                }else{
                    tok = new Token(TokenType.ILLEGAL, String.valueOf(ch));
                }
                return tok;
        }
            readChar();
            return tok;
        }

    public static void main(String[] args) {
        String input="let five = 5 ; (* ";
        Lexer obj=new Lexer(input);
        while (true) {
            Token x = obj.nextToken();
            if (x.type.equals("EOF")) break;
            if (x.type.equals("ILLEGAL")) {
                System.out.println("ILLEGAL token at: " + x.literal);
                break;
            } else {
                System.out.println(x.type + " " + x.literal);
            }
        }
        System.out.println();
    }
   
}
