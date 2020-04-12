import erepdb


class ErepUtils:
    def __init__(self):
        super(ErepUtils, self).__init__()
        self.db = erepdb.ErepDB()

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def get_country_id(self, country_name):
        country_name = (
            country_name.replace("_", "\_")
            .replace("%", "\%")
            .replace("?", "\?")
            .replace("*", "\*")
        )
        data = self.db.queryone(
            "SELECT id FROM countries WHERE name LIKE ? ESCAPE '\\'",
            ["%" + country_name + "%"],
        )
        return int(data[0])

    def get_country_name(self, country_id):
        data = self.db.queryone(
            "SELECT name FROM countries WHERE id == ?", [country_id]
        )
        return data[0]

    def get_country_flag(self, country_id):
        data = self.db.queryone(
            "SELECT flag FROM countries WHERE id == ?", [country_id]
        )
        return data[0]

    def get_user(self, username):
        username = (
            username.replace("_", "\_")
            .replace("%", "\%")
            .replace("?", "\?")
            .replace("*", "\*")
        )
        data = self.db.queryall(
            "SELECT * FROM users WHERE username LIKE ? ESCAPE '\\'", [username + "%"]
        )
        return data

    def get_user_id(self, id):
        data = self.db.queryall("SELECT * FROM users WHERE id = ?", [id])
        if not data:
            raise Exception("User not found")
        return data
