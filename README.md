# Universal SQL Client

## Synopsis

This is a universal SQL client that is written in Python. It is a command prompt developed due to nuisance experience that author faces when he uses a traditional SQL client. This is also a very lightweight SQL client that tries its best to reduce the dependacy of the external libraries apart from the SQL connectors and webapp library. The author hopes that with the minimal coding effort, the tool can be fitted into any platform that installs Python, including modern embedded devices.

## Addressing Controversial Remarks

1. What is the purpose of writing such a tool/CLI?

    The purpose of the design has no means to replace any kind of tools/libraries that are currently available. The purpose of this design is try to understand how a command prompt of SQL client works and mimic one by creating one. Hence in order for the author to connect to different DBs easily, he decided to build a SQL client prompt to utilize the dynamicity of Python module to create the universal connector, and the standardize of SQL library using PEP 249.

    *Use what you need* is the core philosophy of building this tool. This tool does not include every single DB connector library. Rather it will only download/use the library that you need. For e.g. if your DB is MySQL DB, then you will need to download MySQLdb and run MySQLdb only with the tool.

2. Isn't that sqlalchemy can handle everything that relates to SQL?

    Comparing sqlalchemy with my tool might be irrelevant, because my tool is a tool. Hence it should be compared with mysql (client for MySQL) and psql (client for PostgreSQL). With the help in PEP 249, it allows me to build a universal tool such that the client can be used after I install the library MySQLDb or pymssql, without editing any part of the code in the codebase.

3. What is PEP 249 and How does this help in explaining **Universal** client?

    For understanding of PEP249, please refer to [PEP249](https://www.python.org/dev/peps/pep-0249/). With the standardization of API structures for *nearly* (I don't know if it is for all the SQL connectors) of all the SQL connectors, it allows me to build the universal client with one single codebase. I don't need to maintain several modules of codebase for different SQL connectors. It took me several years of connectors coding before I came to know that there is such a standard.

4. What is the pro and cons for your *so-called* Universal SQL Client?

    The interesting feature of the tool:

    1. Same commands across all the SQL DB:
        e.g.

        Traditional:

        ```unix
        sqlite3: .tables
        postgresql: \dt
        MySQL: show tables
        ```

        My tool
        Universal: ```tables```

    2. No funky mode for traditional client. The funky mode works like unix/linux command: ```more``` or ```less```. With this funky mode: It allows the user to browse through the query result easily.

        My tool:

        ```unix
        1> select * from mytable; | #the "|" is the funky mode trigger
        ```

    3. It is embedded with the webapp

         Traditional:

         MySQL: PHPMyAdmin

         PostgreSQL: PHPPgAdmin

         My tool:

         By typing ```webapp``` on the command prompt:

         ```unix
         1> webapp
         ```

         A webapp will be spawn on http://127.0.0.1:5000/sql_web

    4. Save the query to csv file

         Traditional:
         NA

         My tool:

         There are two modes that can do that:

         ```unix
         1> select * from mytable;
         2> save mytable_query.csv
         ```

         or

         ```unix
         1> save select * from mytable mytable_query.csv
         ```

    5. Data visualization (Currently in planning):

        Traditional:
        NA

        My tool:

        It is integrated within the webapp that allows the user
        to build the data visualization based on their SQL query.

## Installation

The installation is easy. Once you have ```git clone``` this repo, all you need to do is to add the python SQL connector into ```requirements.txt``` file. For example:

```txt
flask
mysqlclient
pymssql

```

Once you are done, you can type:

```shell
pip install -r requirements.txt
```

## Before you use

Register your Database to the config file:

```unix
python init.py
```

After typing the command, you will see the prompt below:

```txt
Please enter your db_hostname:
Please enter your db_username:
Please enter your db_password:
Please enter your db_name:
Please give a nickname for your definition:

```

Please enter your db hostname, db username, db password (password is masked), db name, and together with the *cute* db nickname.

The ```init.py``` script will write to config file based on your input

## How to Use

1. How to connect to your DB

    ```unix
    python main.py <YOUR DB_TYPE> <YOUR_DB_NICKNAME>
    ```

    example:

    ```unix
    python main.py mysql test_yahoo
    python main.py mssql test_yahoo
    python main.py postgresql test_yahoo
    ```

2. Basic Command

    ```unix
    e                                   -- exeucte the previous command
    p                                   -- show previous command
    db                                  -- list out all the registered db
    exit/x                              -- same as quit
    help/h                              -- list out the command
    quit/q                              -- quit
    table                               -- list out the table within the db
    column <TABLE_NAME>                 -- show the attribute of the table
    connect <DB_NAME>                   -- connect to the designated db
    switch <DB_NAME>                    -- switch from current db to designated db
    save <FILENAME.csv>                 -- save previous query result to CSV file
    save <SQL QUERY> <FILENAME.csv>     -- save query result to CSV file
    webapp                              -- spawn a webapp at http://127.0.0.1:5000/sql_webapp

    Funky mode:
    |  -- This is similar to unix/linux "more" or "less" command:
    e.g. select * from table_123; |
    This will display the first 10 entries from the select/table/column query
    To display remaining queries, press "<" or ">"
    To quit from Funky mode, press x
    ```

3. SQL Command

   On the prompt, just enter your usual SQL command:

   ```unix
   prompt> select * from yahoo_123;

   ```

## Tested Database Connector

1. SQLite3
2. [MySQL](https://github.com/PyMySQL/mysqlclient-python)
3. [MsSQL](https://github.com/pymssql/pymssql)

## Things to Do

1. Write the test case (In Progress)
2. Write the data visualization (In Progress)
3. Make the module more scalable and extensible
4. Consider Asynchronous approach (thanks go to [Christoforus](https://www.facebook.com/totoganteng))
5. Finish the test for:

* [PostgreSQL](https://github.com/psycopg/psycopg2)
* [FireBird](https://github.com/FirebirdSQL/fdb)

## Future Roadmap

1. Adding ER diagram inside the prompt
2. Better structure of the codebase for code extension and scability
3. Better UI design for the webapp interface.

## History to remember (14/4/2019)

Facebook, Instagram and WhatsApp are currently down upon my submission of this repo.