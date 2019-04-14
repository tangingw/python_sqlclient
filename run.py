import sys
import os


def main():

    if len(sys.argv) < 3:

        print("python run.py <DB_TYPE> <DB_NAME>")
    
    elif len(sys.argv) > 3:

        print("Too many variables. You are prohibited to run the webapp")

    else:
        
        os.environ["DB_TYPE"] = sys.argv[1]
        os.environ["DB_NAME"] = sys.argv[2]
        
        from app.webapp import app

        app.run(host="127.0.0.1", port=5000)

        del os.environ["DB_TYPE"]
        del os.environ["DB_NAME"]


if __name__ == "__main__":

    main()
    