class UserInfo:
    @staticmethod
    def get_username():
        with open("top_secret.txt") as f:
            line = ""
            for _ in range(2):
                line = f.readline()
            return line

    @staticmethod
    def get_password():
        with open("top_secret.txt") as f:
            line = ""
            for _ in range(3):
                line = f.readline()
            return line
