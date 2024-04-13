Final Project - COMP3005

Ahraaz Supra - 101266714

Video Link: https://youtu.be/C_3o4ECq9pg

Database Setup:

1. Ensure that PostgreSQL is installed and running on your system.

2. Create a PostgreSQL database.

3. Use the DDL.sql file to create the database tables.

4. Populate the tables with initial records using the DML.sql file.

Application Setup:

1. Ensure Python3 is installed on your system.

2. Install the psycopg2 library using pip:

    pip3 install psycopg2-binary

3. In the project_database.py file, update the connect_to_db() function with your actual database connection details:

    conn = psycopg2.connect(
      dbname='yourDBname',
      user='postgres',
      password='yourPassword',
      host='localhost'
    )

    Replace 'yourDBname' to your Database's name. And replace 'yourPassword' with your actual database password.

4. Run program.
