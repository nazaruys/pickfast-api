def is_valid_password(password):
            if type(password) != str:
                return False
            if len(password) < 8:
                return False
            if not any(char.isupper() for char in password):
                return False
            if not any(char.islower() for char in password):
                return False
            if not any(char.isdigit() for char in password):
                return False
            return True