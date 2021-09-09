# Shopify
An open source ecommerce project powered by Django as backend and React as frontend

# installation

## Backend
backend foundation laid on Django and RestFramework API

once after cloning package you need to make an environment to isolate the application from your gerneral python invironment
user `py -m venv whatevername` to make your own env.

not it's time to install Django by using `pip install django` and install all its dependencies using `pip install -r requirements.txt`

## Frontend
to get the most out of shoping API, React Js has been used, with this architecture frontend can easily adapt to whatever device we prefere to have our shop on.
if you wanna stick to the original frontend provided by the project follow the few line below, otherwise jump into API guidence to save your time.

first thing first, you need to [download](https://nodejs.org/en/) and install node.js to provide you with `npm`.
to install React library open your terminal and head into 
>project-dir/frontend
and use `npm install` to install react and all its dependencies once.


## make project working
to make the project working we need to have both Django and React open simultaniusly.
for first runing django project you need to create database based on django models. use these two commands to create data schema:
`py manage.py makemigrations` and `py manage.py migrate` then to start the django project use `py manage.py runserver`.
now it's time to run our React project, to do so jump into the front end directory and use `npm start` and here we go! enjoy your hacking !!!


# API
all the API interfaces in store application are provided by a core Object called Store into store.py module. this module does the CRUD operations for you by simple and chainable methods. first you need to specify what you need by it's searching methods and when your specifications finished fetch them all.

## products
to get the product(s) you need they are some usefull methods you can use:
* selectById: you can simply specify the id of product you need to get information by this method.
* category(category_id): you can simply specify the category that you are intrested of having its product, this method can be used for creating category pages.
* store(store_id): this method can bring you all the producs a specific shop has into your website.
* orderBy(order_by): this method can order the results by the field provided as order_by.
* limitsBy(low,high): this method will limit your results by split and extract the portions you are really intrested of.

except selectById, all other functions can bound to each other by using chain notation like `store.product.caregory(1).store(2).orderBy('price').limitsBy(15,25)`

and the final trick, to fetch the data you have provided by chain notation you need to use the `fetch()` method to execute the quertset. to put it simple you can get all the products you need like this:

`products = store.product.caregory(1).store(2).orderBy('price').limitsBy(15,25).fetch()`
