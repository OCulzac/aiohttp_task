# aiohttp_task

---
This is a basic task making a book store using python, aiohttp and sql alchemy.

---

### Basic startup

_Environment setup_: Installation can be done via loading the 
venv or if from scratch then install the packages in _requirements.txt_

After setup, run  `aiohttp_store/crud.py` to connect and populate the database, then 
run `main.py` to fire up the app.

---
### Endpoints:

        http://localhost:8080/user 
    
This is a simple **GET** request that queries the db and returns all user info in the User table

        http://localhost:8080/user_orders  
    
This is a **POST** request that takes query params

_Key_: first name, _Value_: String input of first name

_Key_: surname, _Value_: String input of surname

and returns the order history of the user, if found.

        http://localhost:8080/new_order
This is  **POST** request that takes query params

_Key_: order date, _Value_: date in the format yyyy-mm-dd

_Key_: user id, _Value_: Interger number

_Key_: book id, _Value_: Interger number

_Key_: shop id, _Value_: Interger number

_Key_: book quantity, _Value_: Interger number

and first inserts the _order date_ and _user id_ into the _Order_ table then 
takes the _id_ from the _Order_ table and inserts the remaining user input into the
_OrderItem_ table.

        http://localhost:8080/sort
This is a **POST** request that takes query params

_Key_: sort by, _Value_: Choices of (user_id, id, reg_date)

and returns Orders sorted according to entry

         http://localhost:8080/book_shop
This is a **POST** request that takes query params

_Key_: store name, _Value_: string input of shop name

and returns books that were purchased from that shop.