# Personal project - Diet-Creation

This is a web application for creating a personal menu. This application allows the user to create, store and share recipes that the user uses in his life and use them to create a planned menu for periods ranging from one day to a month. This will allow the user to plan a basic list of products for the required period.

The purpose of this application is to facilitate menu planning so that every day or meal you do not have to think about what you can cook next. It will also allow you to correctly plan the volume of purchased products, so that it minimizes the amount of surplus that can be lost and subsequently simply thrown into the trash.

[Web-App on Heroku](https://diet-creation.herokuapp.com/)

# Development Environment

The tools that I used to develop software are VSCode and the corresponding extensions for working with the python language. I also actively used Git and its version control system.

This Web App was written in Python programming language using Flask framework as a backend and HTML, CSS/Bootstrap and JavaScript/JQuery as frontend. For working with data I use SQL and sqlite3 python module.

# Web Pages

* Home page: 
    Have links for three main sections of the app: Products (not availiable now), Recipes, Menu (not availiable now); with a little description of the purpose of each of them. (You can return to this page from any page of the application using the navigation block or by clicking on the name in the header.)

* Recipes page: 
    Display a full list of recipes with its name, type and list of ingredients which are taken from the database. Each recipe has delete and edit buttons. At the top of the list placed button for adding new recipe. If there are no recipes in the database, the user will be notified and a button to add a recipe will be shown. (You can return to this page from any page of the application using the navigation block.)

* Recipe page: 
    Display full information about a specific recipe which is taken from the database.(You can access this page only from the page of the main list of recipes by clicking on any of the displayed recipes.)

* Create recipe page: 
    This page contains a form to fill in information about the recipe. As a standard, she suggests adding: name, type, one ingredient, one cooking step of the recipe and mark the possibility to make it an ingredient for other recipes. If the recipe contains more than one ingredient or cooking step, then you must click on the corresponding button and an additional field will be added. After the form is completed and the user has clicked on the save recipe button, the user will be taken to a page with an updated list of recipes. (You can access this page only if the user is logged in from the page of the main list of recipes by clicking on plus button at the top of list or if list is empty by "Create recipe" button.)
    
* Edit recipe page: 
    This page contains a form to fill in information about the recipe. By default, it contains the following information about the recipe, if available: name, type, ingredients, recipe preparation steps and the ability to make it an ingredient for other recipes. If you need to add more than one ingredient or cooking step to the recipe, then you must click on the corresponding button and an additional field will be added. After the form is completed and the user clicks the save recipe button, the user will be taken to a page with an updated list of recipes. (You can only access this page only if the user is logged in from the main recipe list page by clicking the edit button in the box next to each recipe created by this user, or from the page for viewing data about a particular recipe.)

* Autorization and registration pages: 
    The authorization page contains a login form if the user has previously registered in the application. (this page is available if the user is not authorized by clicking on the closed dish icon in the upper right corner) Otherwise, go to the registration page (the link is under the authorization form) and enter registration data.
    
* User's page: 
    This page contains data on the number of products, recipes and various menus for this user. (This page is only available to authorized users by clicking on the user icon in the top right corner.)
    
# Future Work

* Create 4 pages for products (list, create, edit, view a single product) that the user buys from the store and uses in recipes. (Similar to recipes)

* Create 4 pages for the menu (list of different menus, create a new one, change, view a separate menu), which the user will compile according to the available recipes.
