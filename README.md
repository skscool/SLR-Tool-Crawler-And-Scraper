# SSD33

## Website
A website for scholars that makes Advanced Search & Fast Download of literature metadata in 4 most popular online literate library very easy.
It lets you search in ACM, IEEE, ScienceDirect and Springer all at once. It fetches the bibTeX and gives it as output which is a JSON file.
You can also search for individual libraries ACM, IEEE, ScienceDirect or Springer from here itself.

## Prerequisits
* Django ``pip3 install Django``
* BeautifulSoup ``pip3 install beautifulsoup4``
* requests ``pip3 install requests``
* requests_html ``pip3 requests_html``
* Multidict ``pip3 install multidict``
* threading module for parallel download from all the libraries ``pip3 install threading``

## Running the application
* ``python manage.py runserver 8080`` or any other Port.

## UI

![Homepage](https://github.com/skscool/SLR-Tool-Crawler-And-Scraper/blob/main/screenshots/Screenshot%202020-11-21%20at%2011.14.42%20PM.png)

![SCM](https://github.com/skscool/SLR-Tool-Crawler-And-Scraper/blob/main/screenshots/Screenshot%202020-11-21%20at%2011.14.44%20PM.png)

![IEEE](https://github.com/skscool/SLR-Tool-Crawler-And-Scraper/blob/main/screenshots/Screenshot%202020-11-21%20at%2011.14.46%20PM.png)

![Springer](https://github.com/skscool/SLR-Tool-Crawler-And-Scraper/blob/main/screenshots/Screenshot%202020-11-21%20at%2011.14.48%20PM.png)

![ScienceDirect](https://github.com/skscool/SLR-Tool-Crawler-And-Scraper/blob/main/screenshots/Screenshot%202020-11-21%20at%2011.14.50%20PM.png)
