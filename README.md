# MySQL🐬 Database Model Maker

## Description
This script generates a **database schema diagram** from a **MySQL database** using `graphviz`. It automatically extracts tables, their columns, and foreign key relationships to produce a **visual representation** of the database structure.

## Features
- Automatically fetches **tables** and **columns** from MySQL
- Identifies **foreign key relationships**
- Generates a **Graphviz-based PNG schema diagram**

## Installation
### Prerequisites
- MySQL server
- Required Python libraries:
  ```sh
  pip install mysql-connector-python graphviz
  ```
- Install Graphviz (required for visualization):
  - **Linux**: `sudo apt install graphviz`
  - **MacOS**: `brew install graphviz`
  - **Windows**: [Graphviz.org](https://graphviz.org/download/)

## Usage
### Configure Database Connection
Update the `host`, `user`, `password`, and `database` variables in `database_model_maker.py`:
```python
if __name__ == "__main__":
    host = "localhost"
    user = "root"
    password = "your_password"
    database = "your_database"
```

### Run the Script
Execute the script to generate the schema:
```sh
python database_model_maker.py
```

### Output
A PNG file will be generated in the same directory:
```
database_schema.png
```

### Example
If your database contains tables like `Users`, `Orders`, and `Products`, the script will generate a schema like this:

```
Users (ID, Name, Email)
Orders (ID, UserID, ProductID, OrderDate)
Products (ID, Name, Price)
```
And show relationships like this:
- `Orders.UserID → Users.ID`
- `Orders.ProductID → Products.ID`


