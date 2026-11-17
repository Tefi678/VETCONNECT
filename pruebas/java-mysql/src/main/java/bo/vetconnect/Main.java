package bo.vetconnect;

import bo.vetconnect.config.Conexion;
import java.sql.Connection;
import java.sql.SQLException;

public class Main {
    public static void main(String[] args) {

        try (Connection conexion = Conexion.conectar()) {

            if (conexion.isValid(2)) {
                System.out.println(
                    "¡Conexión de Java con MySQL exitosa!"
                );
            }

        } catch (SQLException e) {

            System.out.println(
                "Error al conectar con MySQL: " + e.getMessage()
            );
        }
    }
}
