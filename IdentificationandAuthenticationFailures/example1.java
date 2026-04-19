// if (inputPassword.equals(user.getPassword())) { 
//     // Login success
// }
import org.mindrot.jbcrypt.BCrypt;
public class AuthService {
    public boolean login(String inputPassword, User user) {
        if (inputPassword == null || inputPassword.isBlank()) {
            return false;
        }
        if (user == null || user.getPasswordHash() == null) {
            return false;
        }
        return BCrypt.checkpw(inputPassword, user.getPasswordHash());
    }
}