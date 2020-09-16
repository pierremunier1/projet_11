
# projet_onze pur beurre

Program developed by Pierre Munier, September2020.

## Update of September 2020

- Autocomplete field in the home page
- Reset password by email

## What the project is for ?

    Pur Beurre website allows you to find a substitute healthy food to your junk food !
    Food quality is based on the nutriscore, with all the data from the Open Food Facts open source database.
    The user enters the name and the brand of the food to substitute. 
    The website find a list of substitute foods from the same category and with a better nutriscore.
    You can check on each substitute food the user can have more information about it.
    The user can save the healthy products found in the substitute list and then consult his selection.
    Each selected food can also be deleted.

## How to use it or get it running ?

    Pur Beurre is a Python website, developed with the Django framework 3.0, Python 3.7.5 and PostgreSQL 
    for the backend and Boostrap creative for the theme.

    You can access the program from your Terminal 
    executing ./manage.py runserver and watching it from your localhost:8000 in your browser 
     here https://purbeurre75.herokupapp.com, deployed with Heroku.

## How to update the category list and food data if running this app with localhost ?

    Pur Beurre has been developped with 5 different categories of food. 
    See the name of these categories in the CATEGORIES (pur_beurre/products/managements/config.py).     
    if you want to change it - add some more or drop ones - just modify that list before running an update.
    If you change the CATEGORIES or just want to update your database with the latest food data, 
    You need to run this command from your command line :
    ./manage.py openff.py

Enjoy it !
