#!python3
#encoding:utf-8
import subprocess
import shlex
import os.path
import getpass
import license.insert.Main
class InitializeMasterDbCreator:
    def __init__(self, db_dir_path):
        self.db_dir_path = db_dir_path
        self.db_file_names = {
            'Languages': 'GitHub.Languages.sqlite3',
            'License': 'GitHub.Licenses.sqlite3',
            'Accounts': 'GitHub.Accounts.sqlite3',
            'License': 'GitHub.Repositories.{user}.sqlite3',
            'OtherRepository': 'GitHub.Repositories.__other__.sqlite3',
            'GnuLicense': 'GNU.Licenses.sqlite3',
            'Api': 'GitHub.Api.sqlite3',
        }
        self.db_files = {
#            'GitHub.Languages.sqlite3': CreateLanguage,
#            'GitHub.Licenses.sqlite3': self.CreateLicenses,
            'License': {'FileName': 'GitHub.Licenses.sqlite3', 'Creator': self.__CreateLicenses, 'Inserter': self.__InsertLicenses},
#            'GitHub.Accounts.sqlite3': CreateAccounts,
#            'GitHub.Repositories.{user}.sqlite3': CreateRepositories,
#            'GitHub.Repositories.__other__.sqlite3': CreateOtherRepositories,
#            'GNU.Licenses.sqlite3': CreateGnuLicenses,
#            'GitHub.Api.sqlite3': CreateApi
        }

    def Run(self):
        if not(os.path.isdir(self.db_dir_path)):
            print('DBディレクトリを作る----------------')
            os.mkdir(self.db_dir_path)
        for db in self.db_files.keys():
            db_path = os.path.join(self.db_dir_path, db)
            if not(os.path.isfile(db_path)):
                print('DBファイルを作る: {0} ----------------'.format(db_path))
                self.db_files[db]['Creator'](db_path)
#                self.db_files[db]['Inserter'](db_path)
                self.db_files[db]['Inserter']()

    def __CreateLicenses(self, db_path):
        subprocess.call(shlex.split("bash ./license/create/Create.sh \"{0}\"".format(db_path)))
        
    def __InsertLicenses(self):
        creator_license = self.__LicenseCreator()
        creator_license.Initialize()
        
    def __LicenseCreator(self):
        github_user_name = 'ytyaru'
        os_user_name = getpass.getuser()
        device_name = '85f78c06-a96e-4020-ac36-9419b7e456db'
        path_db_base = 'mint/root/db/Account/GitHub'
        path_db_account = '/media/{0}/{1}/{2}/private/v0/GitHub.Accounts.sqlite3'.format(os_user_name, device_name, path_db_base)
        path_db_repo = '/media/{0}/{1}/{2}/public/v0/GitHub.Repositories.{3}.sqlite3'.format(os_user_name, device_name, path_db_base, github_user_name)
#        path_db_license = '/media/{0}/{1}/{2}/public/v0/GitHub.Licenses.sqlite3'.format(os_user_name, device_name, path_db_base)
        path_db_license = '../res/db/GitHub.Licenses.sqlite3'.format(os_user_name, device_name, path_db_base)
        return license.insert.Main.Main(github_user_name, path_db_account, path_db_repo, path_db_license)

