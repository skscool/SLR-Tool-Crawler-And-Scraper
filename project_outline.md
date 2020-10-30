# Project Outline

## Brief project outline
* The task in hand is to create a UI which provides a basic search (search bar to take user input) and advanced search (to add more filters).
* Then for a particular search input extract citations from ACM, IEEE, Springer and Science direct
* Remove duplicates from the search result and create a json file and let the user download it.

## Solution Approach
* Web scraping will be required for which python's BeautifulSoup library could be used to extract results from ACM,IEEE etc.
* Analyzing various libraries for their filters(basic and advanced search).
* A simple UI is to be created using HTML,CSS and JavaScript where user can download the results.
* Generating search string url for every library based on the user input.
* Combining the results from the 4 libraries and removing duplicates.
* Integrating frontend and backend.
* Hosting the website.

## System Requirements for using the Application
* Modern web browser.

## Constraints
* If the search is too generic then it takes some time to show the results.

## Timeline
* The whole project could be broken down into sub-activities as follows:
* Phase 1 -- 17-10-2020 : 
    - Backend part, creating python scripts to extract the data for each library. 
* Phase 2 -- 30-10-2020 : 
    - Analyzing various citations platforms, their filters and all.
* Phase 3 -- 10-11-2020 : 
    - Extract results for IEEE.
    - Creating Web page for the UI. 
    - Generating search string url for every library based on the user input.
    - Combining the results and removing duplicates.
    - Integrating frontend and backend.
    - Hosting the website.
* Phase 4 -- Validating the results.
