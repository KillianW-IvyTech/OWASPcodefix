/*String username = request.getParameter("username");
  String query = "SELECT * FROM users WHERE username = '" + username + "'";
  Statement stmt = connection.createStatement();
  ResultSet rs = stmt.executeQuery(query); */
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class UserRepository {
    private final Connection connection;
    public UserRepository(Connection connection) {
        this.connection = connection;
    }
    public User findByUsername(String username) throws SQLException {
        if (username == null || username.isBlank()) {
            throw new IllegalArgumentException("Username must not be null or empty");
        }
        if (username.length() > 50) {
            throw new IllegalArgumentException("Username exceeds maximum allowed length");
        }
        String query = "SELECT id, username, email, created_at FROM users WHERE username = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, username);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapRow(rs);
                }
                return null;
            }
        }
    }
    private User mapRow(ResultSet rs) throws SQLException {
        User user = new User();
        user.setId(rs.getLong("id"));
        user.setUsername(rs.getString("username"));
        user.setEmail(rs.getString("email"));
        user.setCreatedAt(rs.getTimestamp("created_at").toLocalDateTime());
        return user;
    }
}