import erepdb
import logging

module_logger = logging.getLogger('Socrates.'+__name__)


class ErepUtils:
    def __init__(self):
        super(ErepUtils, self).__init__()
        self.logger = logging.getLogger('Socrates.'+__name__)
        self.db = erepdb.ErepDB()

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def get_country_id(self, country_name):
        data = self.db.queryone("SELECT id FROM countries WHERE name LIKE ?", ['%'+country_name+'%'])
        return int(data[0])

    def get_country_name(self, country_id):
        data = self.db.queryone("SELECT name FROM countries WHERE id == ?", [country_id])
        return data[0]

    def get_country_flag(self, country_id):
        data = self.db.queryone("SELECT flag FROM countries WHERE id == ?", [country_id])
        return data[0]

    def get_user(self, username):
        data = self.db.queryall("SELECT * FROM users WHERE username LIKE ?", [username+'%'])
        return data

    def get_user_id(self, id):
        data = self.db.queryall("SELECT * FROM users WHERE id = ?", [id])
        return data
