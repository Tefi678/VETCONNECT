import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ClienteTCP {
    public static void main(String[] args) {
        try (Socket socket = new Socket("127.0.0.1", 5000);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             Scanner scanner = new Scanner(System.in)) {

            System.out.println("Conectado al servidor TCP. Escribe mensajes (o SALIR):");
            while (true) {
                System.out.print("> ");
                String msg = scanner.nextLine();
                out.println(msg);
                if ("SALIR".equalsIgnoreCase(msg.trim())) break;
                System.out.println(in.readLine());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
