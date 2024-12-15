CRUD Operations:
Books:  create, read, update, and delete books.
Users:  user registration and management.
Transactions: users can borrow and return books. 


API Endpoints

 
Register a User ---   POST /api/users/  ---  Create a new user
List Users  ---   GET  /api/users/  ---  List all users
Get User Details  ---  GET  /api/users/{id}/  ---  Retrieve a specific user's details
Update User  ---  PUT/PATCH /api/users/{id}/  ---  Update a specific user
Delete User  ---  DELETE    /api/users/{id}/  ---  Delete a specific user
Obtain JWT Token  ---  POST /api/token/  ---  Obtain a JWT token
Refresh JWT Token  ---  POST /api/token/refresh/ --- Refresh a JWT token
List All Books --- GET  /api/books/  ---  List all books, with optional filters
Create a Book --- POST /api/books/  ---  Add a new book
Get Book Details  ---  GET  /api/books/{id}/  ---  Retrieve a specific book's details
Update a Book --- PUT/PATCH /api/books/{id}/  ---  Update a book's details
Delete a Book --- DELETE    /api/books/{id}/  ---  Delete a specific book
Borrow a Book --- POST /api/transactions/check_out/ --- Borrow (check out) a book
Return a Book --- POST /api/transactions/return/   ---  Return a borrowed book
View Borrowing History  ---  GET  /api/transactions/history/  ---  View current user's borrowing history


Examples

1.Create user
    Post  >>  https://kidusom.pythonanywhere.com/api/users/
    Content type >> application/json
    Body >> 
    {
     "username": "user4",
     "password": "user4password",
     "email": "user4@user4.com",
     "first_name": "user",
     "last_name": "4"
    }


2.Get user auth token 
          Post  >>  https://kidusom.pythonanywhere.com/api/token/
         Content type >> application/json
       {
        "username": "user4",
        "password": "user4password"
       }

3.Delete user
    Delete >> https://kidusom.pythonanywhere.com/api/users/5/
    Token >> Authorization,bearer
    Content type >> application/json



4.List users
     Get >> https://kidusom.pythonanywhere.com/api/users/
     Content type >> application/json


5.Create book
    Post >> https://kidusom.pythonanywhere.com/api/books/
    Content type >> application/json
    Body >>
    {
     "title": "Across the Sand",
     "author": "hugh howey",
     "isbn": "9780061120085",
     "published_date": "2022-10-04",
     "copies_available": 30
     }


6.Delete book
    Delete >> https://kidusom.pythonanywhere.com/api/books/4/
    Content type >> application/json


7.List books
      Get >> https://kidusom.pythonanywhere.com/api/books/
      Content type >> application/json


8.Borrow book
      Post >> https://kidusom.pythonanywhere.com/api/transactions/check_out/
      User2  >> Authorization,bearer
           Content type >> application/json
           Body  >> 
           {
           "book_id": 1
           }


9.Return book
     Post >> https://kidusom.pythonanywhere.com/api/transactions/return/
          User2  >> Authorization,bearer
           Content type >> application/json
           Body  >> 
           {
           "book_id": 1
           }


10.See copies 
     Get >> https://kidusom.pythonanywhere.com/api/transactions/history/
          User2  >> Authorization,bearer
          Content type >> application/json


11.See transaction history 
     Get >> https://kidusom.pythonanywhere.com/api/books/1/
         Content type >> application/json   


12.Errors 
        Checkout book twice 
       And return book i didn't not borrow 
           Post >> https://kidusom.pythonanywhere.com/api/transactions/check_out/
       User2  >> Authorization,bearer
           Content type >> application/json
           Body  >> 
           {
           "book_id": 1
           }
 
