package bo.vetconnect.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Conexion {
    private static final String URL =
        "jdbc:mysql://127.0.0.1:3306/vetconnect_db";

    private static final String USER = "root";

    private static final String PASSWORD = "admin1234";

    public static Connection conectar() throws SQLException {

        return DriverManager.getConnection(
            URL,
            USER,
            PASSWORD
        );
    }
}
