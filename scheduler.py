import schedule, shutil, time
import controller

def offers_check():
    handler = controller.Controller()
    handler.usual_update()
    handler.sites_check()


def database_backup():
    pass


if __name__ == "__main__":

    schedule.every(12).hour.do(offers_check)
    schedule.every(24).hour.do(database_backup)

    while True:
        schedule.run_pending()
        seconds_to_sleep = 60 * 30
        time.sleep(seconds_to_sleep)