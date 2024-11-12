import psycopg2
from table_gen import table

"""
Відобразити всі поставки, які здійснюються за 3 або менше днів. Відсортувати назви
постачальників за алфавітом;
"""
def view_data1(cur: psycopg2.extensions.cursor):
    cur.execute("""
        SELECT s.name, d.date, m.name, d.quantity, d.days_to_deliver
        FROM suppliers s
        JOIN deliveries d ON s.id = d.supplier_id
        JOIN materials m ON d.material_id = m.id
        WHERE d.days_to_deliver <= 3
        ORDER BY s.name;
    """)
    res = cur.fetchall()
    t = table.from_list([
        ["Supplier", "Date", "Material", "Quantity", "Days to deliver"],
        *res
    ])
    print("#1: Відобразити всі поставки, які здійснюються за 3 або менше днів")
    print(t)
    print()

"""
Порахувати суму, яку треба сплатити за кожну поставку (запит з обчислювальним полем);
"""
def view_data2(cur):
    cur.execute(f"""
        SELECT s.name, d.date, m.name, m.price, d.quantity, d.quantity * m.price AS total_price
        FROM suppliers s
        JOIN deliveries d ON s.id = d.supplier_id
        JOIN materials m ON d.material_id = m.id
        ORDER BY s.name;
    """)
    res = cur.fetchall()
    t = table.from_list([
        ["Supplier", "Date", "Material", "Price", "Quantity", "Total price"],
        *res
    ])
    print("#2: Порахувати суму, яку треба сплатити за кожну поставку")
    print(t)
    print()

"""
Відобразити всі поставки обраного матеріалу (запит з параметром);
"""
def view_data3(cur):
    print("#3: Відобразити всі поставки обраного матеріалу")
    material = input("Введіть назву матеріалу: ")
    cur.execute(f"""
        SELECT s.name, d.date, m.name, d.quantity, d.days_to_deliver
        FROM suppliers s
        JOIN deliveries d ON s.id = d.supplier_id
        JOIN materials m ON d.material_id = m.id
        WHERE m.name = %s
        ORDER BY s.name;
    """, (material,))
    res = cur.fetchall()
    t = table.from_list([
        ["Supplier", "Date", "Material", "Quantity", "Days to deliver"],
        *res
    ])
    print(t)
    print()

"""
Порахувати кількість кожного матеріалу, що поставляється кожним постачальником
(перехресний запит);
"""
def view_data4(cur):
    cur.execute("""
        SELECT s.name, m.name, SUM(d.quantity) AS total_quantity
        FROM suppliers s
        JOIN deliveries d ON s.id = d.supplier_id
        JOIN materials m ON d.material_id = m.id
        GROUP BY s.name, m.name
        ORDER BY s.name;
    """)
    res = cur.fetchall()
    t = table.from_list([
        ["Supplier", "Material", "Total quantity"],
        *res
    ])
    print("#4: Порахувати кількість кожного матеріалу, що поставляється кожним постачальником")
    print(t)
    print()

"""
Порахувати загальну кількість кожного матеріалу (підсумковий запит);
"""
def view_data5(cur):
    cur.execute("""
        SELECT m.name, SUM(d.quantity) AS total_quantity
        FROM materials m
        JOIN deliveries d ON m.id = d.material_id
        GROUP BY m.name;
    """)
    res = cur.fetchall()
    t = table.from_list([
        ["Material", "Total quantity"],
        *res
    ])
    print("#5: Порахувати загальну кількість кожного матеріалу")
    print(t)
    print()

"""
Порахувати кількість поставок від кожного постачальника (підсумковий запит).
"""
def view_data6(cur):
    cur.execute("""
        SELECT s.name, COUNT(d.id) AS total_deliveries
        FROM suppliers s
        JOIN deliveries d ON s.id = d.supplier_id
        GROUP BY s.name;
    """)
    res = cur.fetchall()
    t = table.from_list([
        ["Supplier", "Total deliveries"],
        *res
    ])
    print("#6: Порахувати кількість поставок від кожного постачальника")
    print(t)
    print()


def main():
    try:
        conn = psycopg2.connect(dbname='deliveries', user='nemesh', password='12345678', host='localhost')
    except psycopg2.OperationalError as e:
        print("Unable to connect!", e)

    cur = conn.cursor()

    try:
        view_data1(cur)
        view_data2(cur)
        view_data3(cur)
        view_data4(cur)
        view_data5(cur)
        view_data6(cur)
    except Exception as e:
        print("Error creating tables!", e)

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()