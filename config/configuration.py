import configparser, logging, os, shutil, sys, pathlib

class Configuration:
    """
    Keeps access to config files
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = configparser.ConfigParser()
        self.path = pathlib.Path(__file__).parent.absolute()
        self.__check_config_file()


    def get_db_path(self):
        """
        Returns path to the database with data
        """
        return self.__get_path_to("paths", "db_path")


    def get_logs_path(self):
        """
        Returns path to the file with logs
        """
        return self.__get_path_to("paths", "logs_path")


    def get_token_pickle_path(self):
        """
        Return path to token.pickle
        """
        return self.__get_path_to("paths", "token_pickle_path")


    def __get_path_to(self, section, option):
        """
        Generic function to return config entry
        """
        try:
            relative_path = self.config.get(section, option).strip('"')
            path = os.path.join(self.path, relative_path)
            return os.path.abspath(path)
        except:
            raise Exception(f"No path to the database with {section} : {option}")

    
    def __check_config_file(self):
        """
        Checks existence of config.ini file. If file does not exist,
        following is being created using config_template.ini as example.
        """
        path_to_config = os.path.join(self.path, "config.ini")
        if os.path.isfile(path_to_config):
            self.logger.info("File with configuration exists")
        else:
            self.logger.warn("File with configuration does not exist")
            path_to_template = os.path.join(self.path, "config_template.ini")
            if os.path.isfile(path_to_template):
                shutil.copyfile(path_to_template, path_to_config)
                self.logger.warn("File with configuration created")
            else:
                raise Exception("No configuration file!")
        self.config.read(path_to_config)