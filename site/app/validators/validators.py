from ..models.user import User
import bcrypt

class Validator():
    """ Validator class used to validate data """
    def validate_registration_data(self, user):
        """ validate user data before insert to database"""
        errors = []
        
        errors += self.__validate_str_input(user["first_name"], 2, 25, "First name")
        errors += self.__validate_str_input(user["last_name"], 2, 50, "Last name")
        errors += self.__validate_str_input(user["username"], 2, 50, "Username")
        errors += self.__validate_username(user["username"], "Username")
        errors += self.__validate_password(user["password"], user["password_to_match"], "Passwords")
        
        return errors
    
    def validate_login_data(self, username, password):
        """ validate user login data """
        errors = []
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(str(password).encode("utf-8"), str(user.password).encode("utf-8")):
                return errors
            else:
                errors.append("Wrong password.")
        else:
            errors.append("Wrong username.")
        
        return errors
            
    def __validate_str_input(self, input_data, min, max, message):
        """ validate string data with boundaries and other FUTURE solutions """
        errors = []
        data = str(input_data)
        
        if (len(data) < min):
            errors.append(f"{ message } to short.")
        if (len(data) > max):
            errors.append(f"{ message } to long.")
        
        return errors

    def __validate_username(self, username, message):
        """ validate username if exists in database """
        errors = []
        if (User.query.filter_by(username=username).first()):
            errors.append(f"{ message } \"{ username }\" is taken.")
        
        return errors
    
    def __validate_password(self, password, password_to_match, message):
        """ verify if given passwords match """
        errors = []
        
        if(str(password) != str(password_to_match)):
            errors.append(f"{ message } does not match.")
        
        return errors
