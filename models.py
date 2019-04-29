class User:
    def __init__(self, username="", password="", real_name="", email="", is_admin=False):
        self.username = username
        self.password = password
        self.real_name = real_name
        self.email = email
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.__class__}: username={self.username}, " \
               f"real_name={self.real_name}, email={self.email}"


if __name__ == "__main__":
    user = User(username="admin")
    print(user)
