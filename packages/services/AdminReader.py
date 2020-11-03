
class AdminReader:
    def __init__(self, admins):
        self.admins = admins

    def get_admins(self):
        #Check if is admin in admins file
        with open(self.admins, 'r') as admin_file:
            return admin_file.read().splitlines()
        return ''
