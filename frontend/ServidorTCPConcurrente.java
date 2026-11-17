import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ServidorTCPConcurrente {
    public static void main(String[] args) throws IOException {
        int puerto = 5000;
        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println("Servidor TCP escuchando en puerto " + puerto + "...");
            while (true) {
                Socket cliente = serverSocket.accept(); // Bloquea hasta nueva conexión
                System.out.println("Cliente conectado desde: " + cliente.getRemoteSocketAddress());
                new Thread(() -> manejarCliente(cliente)).start();
            }
        }
    }
    private static void manejarCliente(Socket socket) {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {
            String linea;
            while ((linea = in.readLine()) != null) {
                if ("SALIR".equalsIgnoreCase(linea.trim())) break;
                String respuesta = "[ECO_SERVIDOR " + Thread.currentThread().getName() + "]: " + linea.toUpperCase();
                out.println(respuesta);
            }
        } catch (IOException e) {
            System.err.println("Error con cliente: " + e.getMessage());
        }
    }
}
