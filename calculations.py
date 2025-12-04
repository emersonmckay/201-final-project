import sqlite3

def calculations(db_name):
    """
    Select data from the database and calculate:
    1. avg concert capacity for each artist
    2. num of concerts for each artist
    3. correlation between listeners and capacities 
    """

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # TODO: write sql statements here !

    conn.close()

    return {} 

if __name__ == "__main__":
    # temp test: this will error until the real database exists,
    # but it's here as a placeholder!
    db_name = "concerts.db"  # or whatever we decide to name it
    print(calculations(db_name))

