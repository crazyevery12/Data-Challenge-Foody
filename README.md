# Data-Challenge-Foody
Crawl data taken from foody.vn from 3 cities: Ha Noi, Ho Chi Minh and Da Nang and automatically generate chart.
# Requirement
+ Python 3.8
+ Install required package with the following command: **pip install -r requirements.txt**.
+ Jupyter Note Book or Jupyter Lab.
# Intruction
## Set up
After cloning the project to your desire folder, there are things that need to be set up.
### MongoDB
+ If you already have mongoDB in your device. Proceed to final bullet.
+ If you do not have mongoDB, follow the installation guide [here](https://docs.mongodb.com/manual/installation/ "MongoDB installation"). After finish installing mongoDB, proceed to next bullet.
+ Create a new database and retrieve the URI. In setting.py file, paste the new database name in line 71 and URI in line 70.
### Spider
The project 3 spider, in each spider you will need to the following:
+ Locate driver_path varialbe and paste the path to your webdriver.
+ In spider_closed def, paste the path to Report directory accordingly to your device.
### Watch Dog
In Report directory, locate folder_path variable and paste the Report directory accordingly to your device in Watch-Dog.py
## Run the project.
+ Open a termial and input this command to run spider: **scrapy crawl** *the name of the spider*.
+ Open a second terminal, cd to Report directory and input this command to run Watch-Dog: **python Watch-Dog.py**
