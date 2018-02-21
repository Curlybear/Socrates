import dbmanager
import logging

module_logger = logging.getLogger('Socrates.'+__name__)


class ErepUtils:
    def __init__(self):
        super(ErepUtils, self).__init__()
        self.logger = logging.getLogger('Socrates.'+__name__)
        self.db = dbmanager.DbManager()

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def get_country_id(self, country_name):
        country_name = country_name.replace('_', '\_').replace('%', '\%').replace('?', '\?').replace('*', '\*')
        data = self.db.queryone("SELECT id FROM countries WHERE lower(name) LIKE lower(%s) ESCAPE '\\'", ['%'+country_name+'%'])
        return int(data[0])

    def get_country_name(self, country_id):
        data = self.db.queryone("SELECT name FROM countries WHERE id = %s", [country_id])
        return data[0]

    def get_country_flag(self, country_id):
        data = self.db.queryone("SELECT flag FROM countries WHERE id = %s", [country_id])
        return data[0]

    def get_user(self, username):
        username = username.replace('_', '\_').replace('%', '\%').replace('?', '\?').replace('*', '\*')
        data = self.db.queryall("SELECT username, id, discordusername FROM users WHERE lower(username) LIKE lower(%s) ESCAPE '\\'", [username+'%'])
        return data

    def get_user_id(self, id):
        data = self.db.queryall("SELECT username, id, discordusername FROM users WHERE id = %s", [id])
        if not data:
            raise Exception('User not found')
        return data

    def search_wiki(self, query):
        query = query.replace('_', '\_').replace('%', '\%').replace('?', '\?').replace('*', '\*')
        data = self.db.queryall("SELECT * FROM wiki WHERE lower(tag) LIKE lower(%s) ESCAPE '\\'", ['%'+query+'%'])
        return data

    def get_wiki_categories(self):
        data = self.db.queryall("SELECT DISTINCT category FROM wiki", [])
        return data

    def get_wiki_entries_for_category(self, category):
        category = category.replace('_', '\_').replace('%', '\%').replace('?', '\?').replace('*', '\*')
        data = self.db.queryall("SELECT DISTINCT tag FROM wiki WHERE lower(category) LIKE lower(%s) ESCAPE '\\'", [category+'%'])
        return data
