import rumps
import subprocess

def sendNotification(title, subtitle, message):
  bashCommand = ['osascript -e \'display notification "{0}" with title "{1}" subtitle "{2}" sound name "NAME"\''.format(message, title, subtitle)]
  process = subprocess.run(bashCommand, shell=True)
  print('sent')


class ScreentimeApp(object):
    def __init__(self):
        self.config = {
            "app_name": "202020",
            "start": "Start Timer",
            "stop": "Stop Timer",
            "break_message": "Time to rest your eyes, look at a point 20ft away for 20 seconds",
            "break_done_message": "Time up!",
            "default_time":"00:00",
            "interval":  20*60 # every 20 minutes
        }
        self.app = rumps.App(self.config["app_name"])
        self.countdown_timer = rumps.Timer(self.on_countdown_tick, 1)
        self.interval = self.config["interval"]
        self.time_left = 0
        self.set_up_menu()
        self.start_button = rumps.MenuItem(title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(title=self.config["stop"], callback=None)
        self.app.menu = [self.start_button, self.stop_button]

    def set_up_menu(self):
        self.countdown_timer.stop()
        self.countdown_timer.count = 0
        self.app.title = "🖥"

    def on_countdown_tick(self,sender):
        print(self.time_left)
        if self.time_left <= 0:
            sendNotification(self.config["app_name"], subtitle="Eye Rest Reminder", message=self.config["break_message"])
            self.timer_done()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.time_left -= 1
  

    def start_timer(self, sender):
      print('start')
      self.reset_timer()

    def reset_timer(self):
      self.time_left = self.interval
      self.countdown_timer.start()
      self.start_button.set_callback(None)

    def stop_timer(self,sender):
      self.set_up_menu()
      self.stop_button.set_callback(None)
      self.start_button.set_callback(self.start_timer)


    def timer_done(self):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_button.title = self.config["start"]
        self.reset_timer()
        

    def run(self):
        self.app.run()

if __name__ == '__main__':
    app = ScreentimeApp()
    app.run()
