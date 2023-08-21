# <img src="https://github.com/dpCTwork/FlaskApp/assets/128423686/70b980d5-e222-46e4-8dc2-f46a38c4df20" width="40" height="40"> Flask Budget App

### About 

This is a basic budgeting app using Flask. The app frontend was made using jinja and Bootstrap 5, while the backend was made using Flask-SQLAlchemy and connected to a PostgreSQL database. The frontend is currently minimal, and will be revamped using React.

By creating this app, I was able to gain experience in the following:

- Modular programming using Flask and MVC architecture
- Database connections and building using Flask-SQLAlchemy
- PostgreSQL
- Python programming (OOP, modules, etc.)
- REST API development and CRUD operations
- API testing/debugging with Insomnia
- HTML, CSS, and Bootstrap5

### API Endpoints

#### User endpoints

- **Register a new User:** `POST /api/register`
- **Verify User and return token:** `POST /api/verify`
- **Update User info by user_id:** `PUT /api/users/update/<user_id>`
- **Delete User by user_id:** `DELETE /api/users/delete/<user_id>`

#### Transactions endpoints

- **Get all transactions from all users:** `GET /api/transactions/get`
- **Get a single transaction:** `GET /api/transactions/get/<transaction_id>`
- **Get all transactions from a single user by username:** `GET /api/transactions/get/users/<username>`
- **Get a single transaction (by id) from a single user (by username):** `GET /api/transactions/get/users/<username>/<transaction_id>`
- **Add a new transaction:** `POST /api/transactions/add`
- **Update a transaction by id:** `PUT /api/transactions/update/<transaction_id>`
- **Delete a transaction by id:** `DELETE /api/transactions/delete/<transaction_id>`

