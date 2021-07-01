# negotimate
Your mate in negotiating trade deals!

## Setup
To setup the project up you will need to have python 3 installed on your machine, and it is encouraged to use virtual environments.

To install the requirements for this project, use

`pip install -r reqs.txt`

To start the application on your localhost, please run

`python manage.py runserver`

You can then use the API to create offers using

`POST http://localhost:8000/offers/<userId>/submit`

with body like

```
{
    "user_id": "superman",
    "product_name": "batmobile",
    "price": 1000.00,
    "quantity": 10
}
```

This will create an offer and return a unique Id which can be used to do further actions on, including:


Accept - `PATCH http://localhost:8000/offers/<offerId>/<userId>/accept`

Cancel - `PATCH http://localhost:8000/offers/<offerId>/<userId>/cancel`

Propose update - `PATCH http://localhost:8000/offers/<offerId>/<userId>/proposeUpdate`

with body like
```
{
    "product_name": "batmobile",
    "price": 1000.00,
    "quantity": 10
}
```

Withdraw - `PATCH http://localhost:8000/offers/<offerId>/<userId>/withdraw`


You can also get a view of the history of the orders using

`GET http://localhost:8000/offers/<offerId>/<userId>/history`



Unfortunately not all features have been implemented. But happy to talk through what I would done with more time.s