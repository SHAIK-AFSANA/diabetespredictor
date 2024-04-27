import sqlite3

# Establish connection to SQLite database
db_connection = sqlite3.connect('diabetes.db')
cursor = db_connection.cursor()

# Execute SQL command to create patienttable
cursor.execute("""
CREATE TABLE IF NOT EXISTS patienttable (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Execute SQL command to create patientsdata
cursor.execute("""
CREATE TABLE IF NOT EXISTS patientsdata (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    patient_id INTEGER,
    age INTEGER NOT NULL,
    gender TEXT CHECK(gender IN ('Male', 'Female')) NOT NULL,
    Polyuria TEXT CHECK(Polyuria IN ('Yes', 'No')) NOT NULL,
    Polydipsia TEXT CHECK(Polydipsia IN ('Yes', 'No')) NOT NULL,
    Sudden_Weight_Loss TEXT CHECK(Sudden_Weight_Loss IN ('Yes', 'No')) NOT NULL,
    Weakness TEXT CHECK(Weakness IN ('Yes', 'No')) NOT NULL,
    Polyphagia TEXT CHECK(Polyphagia IN ('Yes', 'No')) NOT NULL,
    Genital_Thrush TEXT CHECK(Genital_Thrush IN ('Yes', 'No')) NOT NULL,
    Visual_Blurring TEXT CHECK(Visual_Blurring IN ('Yes', 'No')) NOT NULL,
    Itching TEXT CHECK(Itching IN ('Yes', 'No')) NOT NULL,
    Irritability TEXT CHECK(Irritability IN ('Yes', 'No')) NOT NULL,
    Delayed_Healing TEXT CHECK(Delayed_Healing IN ('Yes', 'No')) NOT NULL,
    Partial_Paresis TEXT CHECK(Partial_Paresis IN ('Yes', 'No')) NOT NULL,
    Muscle_Stiffness TEXT CHECK(Muscle_Stiffness IN ('Yes', 'No')) NOT NULL,
    Alopecia TEXT CHECK(Alopecia IN ('Yes', 'No')) NOT NULL,
    Obesity TEXT CHECK(Obesity IN ('Yes', 'No')) NOT NULL,
    Prediction TEXT,
    FOREIGN KEY (patient_id) REFERENCES patienttable(id)          
)
""")

# Commit changes and close cursor
db_connection.commit()
cursor.close()

# Close database connection
db_connection.close()
