# Movie-Review-Website

This is a movie review website, where you can find interesting movies and communicate with other movie-lovers.

The website is based on Django and openGauss database, so the web server is required to connect with a openGauss database to store related information.

## File Structure:

- MyProject
  - .venv         environment:python3.9
  - app1
    - migrations  Stores functions and information related to database table migrations.
    - static       Stores frontend components and images.
    - templates
      - manager   Stores HTML files related to the administrator interface.
      - user      Stores HTML files related to the user interface.
    - templatetags
      - models.py Writes project database tables.
      - views.py  Writes backend functions.
  - DataBaseProject
    - settings.py Configuration of project properties.
    - urls.py     Stores URL addresses and maps them to backend functions.
  - media         media: Stores image resources from the database.


## Database schema:
![image](https://github.com/yanhuojunjun/Movie-Review-Website/assets/149027679/08680725-f96f-48ac-bfdc-11f16a148aca)


![屏幕截图 2024-03-25 172158](https://github.com/yanhuojunjun/Movie-Review-Website/assets/149027679/08303f9e-2ced-4d5d-82c0-073b00e82892)

![image](https://github.com/yanhuojunjun/Movie-Review-Website/assets/149027679/875325dc-f9a3-4f53-b537-bf6ff6bc730e)


![image](https://github.com/yanhuojunjun/Movie-Review-Website/assets/149027679/1bc1a379-cd22-44fe-b780-4556abd8534e)
