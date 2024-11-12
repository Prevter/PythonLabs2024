import psycopg2

def create_tables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            contact_name VARCHAR(255) NOT NULL,
            contact_phone VARCHAR(255) NOT NULL CHECK (LENGTH(contact_phone) = 10),
            address VARCHAR(255) NOT NULL
        );
                
        CREATE TABLE IF NOT EXISTS materials (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        );
                
        CREATE TABLE IF NOT EXISTS deliveries (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            supplier_id INT NOT NULL,
            material_id INT NOT NULL,
            days_to_deliver INT NOT NULL CHECK (days_to_deliver BETWEEN 1 AND 7),
            quantity INT NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (material_id) REFERENCES materials(id)
        );
    """)
    print("Tables created successfully!")

def drop_tables(cur):
    cur.execute("""
        DROP TABLE IF EXISTS deliveries;
        DROP TABLE IF EXISTS materials;
        DROP TABLE IF EXISTS suppliers;
    """)
    print("Tables dropped successfully!")

def insert_data(cur):
    """
    add:
    4 suppliers
    22 deliveries
    materials: wood, varnish, metal parts
    """
    cur.execute("""
        INSERT INTO materials (name, price) VALUES
            ('wood', 100),
            ('varnish', 50),
            ('metal parts', 200);
        
        INSERT INTO suppliers (name, contact_name, contact_phone, address) VALUES
            ('Supplier 1', 'John', '1234567890', '123 Main St'),
            ('Supplier 2', 'Jane', '0987654321', '456 Elm St'),
            ('Supplier 3', 'Alice', '1234567890', '789 Oak St'),
            ('Supplier 4', 'Bob', '0987654321', '101 Pine St');
            
        INSERT INTO deliveries (date, supplier_id, material_id, days_to_deliver, quantity) VALUES
            ('2024-01-01', 1, 1, 1, 100),
            ('2024-01-01', 2, 2, 2, 200),
            ('2024-01-01', 3, 3, 3, 300),
            ('2024-01-01', 4, 1, 4, 400),
            ('2024-01-02', 1, 2, 5, 500),
            ('2024-01-02', 2, 3, 6, 600),
            ('2024-01-02', 3, 1, 7, 700),
            ('2024-01-02', 4, 2, 1, 800),
            ('2024-01-03', 1, 3, 2, 900),
            ('2024-01-03', 2, 1, 3, 1000),
            ('2024-01-03', 3, 2, 4, 1100),
            ('2024-01-03', 4, 3, 5, 1200),
            ('2024-01-04', 1, 1, 6, 1300),
            ('2024-01-04', 2, 2, 7, 1400),
            ('2024-01-04', 3, 3, 1, 1500),
            ('2024-01-04', 4, 1, 2, 1600),
            ('2024-01-05', 1, 2, 3, 1700),
            ('2024-01-05', 2, 3, 4, 1800),
            ('2024-01-05', 3, 1, 5, 1900),
            ('2024-01-05', 4, 2, 6, 2000),
            ('2024-01-06', 1, 3, 7, 2100),
            ('2024-01-06', 2, 1, 1, 2200);
    """)
    print("Data inserted successfully!")


def main():
    try:
        conn = psycopg2.connect(dbname='deliveries', user='nemesh', password='12345678', host='localhost')
    except psycopg2.OperationalError as e:
        print("Unable to connect!", e)

    cur = conn.cursor()

    try:
        drop_tables(cur)
        create_tables(cur)
        insert_data(cur)
    except Exception as e:
        print("Error creating tables!", e)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()