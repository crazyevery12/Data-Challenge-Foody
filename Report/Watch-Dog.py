import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import papermill as pm
import subprocess
import pyodbc
import pandas as pd


# folder_path = 'C:\\Users\\tranv\\Desktop\\Python Project\\Data Challenge 1\\foody\\Report'
folder_path = ''


class Watcher:
    DIRECTORY_TO_WATCH = folder_path

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
            file_name = path.split('\\')[-1]
            if file_name.endswith('.csv'):
                time.sleep(1)
                generate_report(file_name)
                to_sql(file_name)
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


def to_sql(csv_file):
    # Import CSV
    data = pd.read_csv (csv_file)
    df = pd.DataFrame(data, columns= ['Name','Position','Price','Quality','Service','Space','ZAvg_Score'])

    # Connect to SQL Server
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-718QBB9\SQLEXPRESS;'
                          'Database=FoodyDB;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    # Create Table
    cursor.execute('CREATE TABLE foody_info (Name nvarchar(50),Position nvarchar(50), Price int(2), Quality int(2),Service int(2), Space int(2), ZAvg_Score int(2) )')

    # Insert DataFrame to Table
    for row in df.itertuples():
        cursor.execute('''
                    INSERT INTO TestDB.dbo.people_info (Name,Position,Price,Quality,Service,Space,ZAvg_Score)
                    VALUES (?,?,?)
                    ''',
                    row.Name,
                    row.Position,
                    row.Price,
                    row.Quality,
                    row.Service,
                    row.Space,
                    row.ZAvg_Score
                    )
    conn.commit()


if __name__ == '__main__':
    w = Watcher()
    w.run()
