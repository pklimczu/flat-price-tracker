import datetime, os, schedule, shutil, time
import controller
from config.configuration import Configuration

def offers_check():
    """
    Checks the offer
    """
    handler = controller.Controller()
    handler.usual_update()
    handler.sites_check()


def database_backup():
    """
    Copies db.json from current path to the archieve
    one with prepending current datetime
    """
    config = Configuration()
    today = datetime.datetime.today().isoformat()
    path_to_db = config.get_db_path()
    path_to_db_without_filename = os.path.dirname(path_to_db)
    path_to_copy = os.path.join(path_to_db_without_filename,
                                "arch", today + "_db.json")                             
    os.makedirs(os.path.dirname(path_to_copy))
    shutil.copy(path_to_db, path_to_copy)


if __name__ == "__main__":

    schedule.every(12).hour.do(offers_check)
    schedule.every(24).hour.do(database_backup)

    while True:
        schedule.run_pending()
        seconds_to_sleep = 60 * 30
        time.sleep(seconds_to_sleep)