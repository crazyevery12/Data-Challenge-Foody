import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import papermill as pm
import subprocess


class Watcher:
    DIRECTORY_TO_WATCH = 'C:\\Users\\tranv\\Desktop\\Python Project\\Data Challenge 1\\foody\\Report'
    def __init__(self):
        self.observer = Observer()

    def run(self):

        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
        print('Error')

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):

        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            path = event.src_path
            filename = path.split('\\')[-1]
            if filename.endswith('.csv'):
                time.sleep(1)
                generate_report(filename)
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)


def run_jupyter(csv, rp_template):
   csv_name =csv.split(".")[0]
   pm.execute_notebook(
      rp_template,
      f"{csv_name}.ipynb",
      parameters=dict(filename=csv)
   )
   return csv_name


def generate_pdf(jupyter_file):
   generate = subprocess.run(
      [
         "jupyter",
         "nbconvert",
         jupyter_file,
         "--to=pdf",
      ]
   )
   return True


def generate_report(csv_file):
    clean_name = run_jupyter(csv_file, 'Template.ipynb')
    notebook_name = f"{clean_name}.ipynb"
    generate_pdf(notebook_name)
    pdf_report_name = f"{clean_name}.pdf"
    print(pdf_report_name)


if __name__ == '__main__':
    w = Watcher()
    w.run()
