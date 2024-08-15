# Groceries Cart API

<p align="center">
  <img src="https://github.com/nazaruys/groceries_cart-frontend/blob/master/app/assets/Groceries-Cart.png?raw=true" alt="Groceries Cart"  width="200" height="200" />
</p>

Groceries Cart API is a Django REST Framework (DRF) API for an app that helps you and your family keep track of the items you need to buy from stores.

## Features

- Create groups.
- CRUD grocery items.
- Categorize items by store and priority.
- Mark items as purchased and more.

## API Endpoints

### Core API

#### Users

- **GET** `/api/core/users/`: Retrieve list of users
- **POST** `/api/core/users/`: Create a new user
- **GET** `/api/core/users/{id}/`: Retrieve details of a specific user
- **PATCH** `/api/core/users/{id}/`: Update a specific user

#### Authentication

- **POST** `/api/core/login/`: Login and obtain access token
- **POST** `/api/core/logout/`: Logout and invalidate access token
- **POST** `/api/core/refresh/`: Refresh access token

### Groups API

#### Groups

- **GET** `/api/group/groups/`: Retrieve list of groups
- **POST** `/api/group/groups/`: Create a new group
- **GET** `/api/group/groups/{id}/`: Retrieve details of a specific group
- **PATCH** `/api/group/groups/{id}/`: Update a specific group

#### Group Products

- **GET** `/api/group/groups/{group_id}/products/`: Retrieve products for a specific group
- **POST** `/api/group/groups/{group_id}/products/`: Create a new product for a specific group
- **GET** `/api/group/groups/{id}/products/{id}/`: Retrieve details of a specific product of a group
- **PATCH** `/api/group/groups/{id}/products/{id}/`: Update a specific product of a group
- **DELETE** `/api/group/groups/{id}/products/{id}/`: Delete a specific product of a group
- **CRUD** `/api/group/groups/{group_id}/stores/{store_id}/products/`: Create, Read, Update, Delete products within a specific store

#### Group Stores

- **GET** `/api/group/groups/{group_id}/stores/`: Retrieve stores for a specific group
- **POST** `/api/group/groups/{group_id}/stores/`: Create a new store for a specific group
- **GET** `/api/group/groups/{id}/stores/{id}/`: Retrieve details of a specific store of a group
- **PATCH** `/api/group/groups/{id}/stores/{id}/`: Update a specific store of a group

#### Group Members

- **GET** `/api/group/groups/{group_id}/members/`: Retrieve members for a specific group

## Stack

- Django
- MySql Client
- Django Rest Framework
- Docker
- DRF SimpleJWT
- Pytest
- Pytest Watch
- Django Debug Toolbar
- Python Dotenv
- DRF Nested Routers

## Getting Started

#### This project uses Docker, in order to start it on your machine, make sure you have Docker installed and follow the instructions:

- `git clone https://github.com/nazaruys/groceries_cart-api.git`
- `cd groceries_cart-api`
- `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- Create a `.env` file with following context:
  `SECRET_KEY=AboveCreatedSecretKey`
  `DATABASE_PASSWORD=YourNewPassword`
  `DEBUG=True`
- `docker-compose up --build`

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
