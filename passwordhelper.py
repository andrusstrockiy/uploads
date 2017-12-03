import hashlib
import os
import base64


class PasswordHelper:
    def get_hash(self, plain):
        hash = hashlib.sha512()
        hash.update(('%s%s' % (self.get_salt(), plain)).encode('utf-8'))
        return hash.hexdigest()

    def get_salt(self):
        password_salt = os.urandom(32).hex()
        return password_salt
        # return base64.b64encode(os.urandom(20))

    def validate_password(self, plain, salt, expected):
        print(plain, salt, expected)
        return self.get_hash(plain + salt) == expected
