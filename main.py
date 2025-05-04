import sqlite3
import os
import random

DB_FILE = "flood_response.db"

class Suburb:
    def __init__(self, id, name, x, y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y

class EvacuationCenter:
    def __init__(self, id, suburb_id, address, pet_friendly, catered, overnight):
        self.id = id
        self.suburb_id = suburb_id
        self.address = address
        self.pet_friendly = pet_friendly
        self.catered = catered
        self.overnight = overnight

class Street:
    def __init__(self, id, suburb_id, name, status):
        self.id = id
        self.suburb_id = suburb_id
        self.name = name
        self.status = status

class Administrator:
    def __init__(self, name, current_suburb_id):
        self.name = name
        self.current_suburb_id = current_suburb_id

def init_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""CREATE TABLE suburbs (
        id INTEGER PRIMARY KEY,
        name TEXT,
        x INTEGER,
        y INTEGER
    )""")
    cursor.execute("""CREATE TABLE resources (
        suburb_id INTEGER,
        resource_type TEXT,
        quantity INTEGER,
        PRIMARY KEY (suburb_id, resource_type),
        FOREIGN KEY (suburb_id) REFERENCES suburbs(id)
    )""")
    cursor.execute("""CREATE TABLE evacuation_centers (
        id INTEGER PRIMARY KEY,
        suburb_id INTEGER,
        address TEXT,
        pet_friendly INTEGER,
        catered INTEGER,
        overnight INTEGER,
        FOREIGN KEY (suburb_id) REFERENCES suburbs(id)
    )""")
    cursor.execute("""CREATE TABLE streets (
        id INTEGER PRIMARY KEY,
        suburb_id INTEGER,
        name TEXT,
        status TEXT,
        FOREIGN KEY (suburb_id) REFERENCES suburbs(id)
    )""")
    cursor.execute("""CREATE TABLE admin_inventory (
        resource_type TEXT PRIMARY KEY,
        quantity INTEGER
    )""")
    
    # Insert suburbs (3x3 grid)
    suburbs = [
        (1, 'Northwest', 0, 0), (2, 'North', 0, 1), (3, 'Northeast', 0, 2),
        (4, 'West', 1, 0), (5, 'Central', 1, 1), (6, 'East', 1, 2),
        (7, 'Southwest', 2, 0), (8, 'South', 2, 1), (9, 'Southeast', 2, 2)
    ]
    cursor.executemany("INSERT INTO suburbs (id, name, x, y) VALUES (?, ?, ?, ?)", suburbs)
    
    # Insert resources
    resources = ['sandbags', 'pumps', 'barriers']
    for suburb_id in range(1, 10):
        for resource in resources:
            quantity = random.randint(5, 20)
            cursor.execute("INSERT INTO resources (suburb_id, resource_type, quantity) VALUES (?, ?, ?)", 
                          (suburb_id, resource, quantity))
    
    # Insert evacuation centers
    for suburb_id in range(1, 10):
        cursor.execute("INSERT INTO evacuation_centers (suburb_id, address, pet_friendly, catered, overnight) VALUES (?, ?, ?, ?, ?)", 
                      (suburb_id, f"{suburb_id}00 Main St", 1, 0, 1))
        cursor.execute("INSERT INTO evacuation_centers (suburb_id, address, pet_friendly, catered, overnight) VALUES (?, ?, ?, ?, ?)", 
                      (suburb_id, f"{suburb_id}01 Elm St", 0, 1, 0))
    
    # Insert streets
    statuses = ['normal', 'advice', 'order']
    for suburb_id in range(1, 10):
        for i, status in enumerate(statuses):
            cursor.execute("INSERT INTO streets (suburb_id, name, status) VALUES (?, ?, ?)", 
                          (suburb_id, f"Street {chr(65+i)}", status))
    
    conn.commit()
    conn.close()

def look(conn, admin):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM suburbs WHERE id = ?", (admin.current_suburb_id,))
    suburb_name = cursor.fetchone()[0]
    print(f"\nYou are in {suburb_name}, {admin.name}.")
    
    # Resources
    cursor.execute("SELECT resource_type, quantity FROM resources WHERE suburb_id = ?", (admin.current_suburb_id,))
    resources = cursor.fetchall()
    print("Resources:")
    for resource, qty in resources:
        print(f"- {resource}: {qty}")
    
    # Evacuation Centers
    cursor.execute("SELECT address, pet_friendly, catered, overnight FROM evacuation_centers WHERE suburb_id = ?", 
                  (admin.current_suburb_id,))
    centers = cursor.fetchall()
    print("Evacuation Centers:")
    for center in centers:
        pet = "Yes" if center[1] else "No"
        cat = "Yes" if center[2] else "No"
        over = "Yes" if center[3] else "No"
        print(f"- {center[0]}: Pet-friendly: {pet}, Catered: {cat}, Overnight: {over}")
    
    # Streets
    cursor.execute("SELECT name, status FROM streets WHERE suburb_id = ?", (admin.current_suburb_id,))
    streets = cursor.fetchall()
    print("Streets:")
    for street in streets:
        print(f"- {street[0]}: {street[1]}")
    
    # Admin Inventory
    cursor.execute("SELECT resource_type, quantity FROM admin_inventory")
    inventory = cursor.fetchall()
    print("Your Inventory:")
    if inventory:
        for item in inventory:
            print(f"- {item[0]}: {item[1]}")
    else:
        print("- Empty")

def move(conn, admin, direction):
    cursor = conn.cursor()
    cursor.execute("SELECT x, y FROM suburbs WHERE id = ?", (admin.current_suburb_id,))
    x, y = cursor.fetchone()
    
    if direction == "north":
        target_x, target_y = x - 1, y
    elif direction == "south":
        target_x, target_y = x + 1, y
    elif direction == "east":
        target_x, target_y = x, y + 1
    elif direction == "west":
        target_x, target_y = x, y - 1
    else:
        return False
    
    cursor.execute("SELECT id FROM suburbs WHERE x = ? AND y = ?", (target_x, target_y))
    result = cursor.fetchone()
    if result:
        admin.current_suburb_id = result[0]
        return True
    return False

def pickup(conn, admin, resource, quantity):
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM resources WHERE suburb_id = ? AND resource_type = ?", 
                  (admin.current_suburb_id, resource))
    result = cursor.fetchone()
    suburb_qty = result[0] if result else 0
    
    if suburb_qty >= quantity:
        new_suburb_qty = suburb_qty - quantity
        if new_suburb_qty > 0:
            cursor.execute("UPDATE resources SET quantity = ? WHERE suburb_id = ? AND resource_type = ?", 
                          (new_suburb_qty, admin.current_suburb_id, resource))
        else:
            cursor.execute("DELETE FROM resources WHERE suburb_id = ? AND resource_type = ?", 
                          (admin.current_suburb_id, resource))
        
        cursor.execute("SELECT quantity FROM admin_inventory WHERE resource_type = ?", (resource,))
        result = cursor.fetchone()
        if result:
            new_admin_qty = result[0] + quantity
            cursor.execute("UPDATE admin_inventory SET quantity = ? WHERE resource_type = ?", 
                          (new_admin_qty, resource))
        else:
            cursor.execute("INSERT INTO admin_inventory (resource_type, quantity) VALUES (?, ?)", 
                          (resource, quantity))
        conn.commit()
        print(f"Picked up {quantity} {resource}.")
    else:
        print(f"Not enough {resource} available.")

def putdown(conn, admin, resource, quantity):
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM admin_inventory WHERE resource_type = ?", (resource,))
    result = cursor.fetchone()
    admin_qty = result[0] if result else 0
    
    if admin_qty >= quantity:
        new_admin_qty = admin_qty - quantity
        if new_admin_qty > 0:
            cursor.execute("UPDATE admin_inventory SET quantity = ? WHERE resource_type = ?", 
                          (new_admin_qty, resource))
        else:
            cursor.execute("DELETE FROM admin_inventory WHERE resource_type = ?", (resource,))
        
        cursor.execute("SELECT quantity FROM resources WHERE suburb_id = ? AND resource_type = ?", 
                      (admin.current_suburb_id, resource))
        result = cursor.fetchone()
        if result:
            new_suburb_qty = result[0] + quantity
            cursor.execute("UPDATE resources SET quantity = ? WHERE suburb_id = ? AND resource_type = ?", 
                          (new_suburb_qty, admin.current_suburb_id, resource))
        else:
            cursor.execute("INSERT INTO resources (suburb_id, resource_type, quantity) VALUES (?, ?, ?)", 
                          (admin.current_suburb_id, resource, quantity))
        conn.commit()
        print(f"Dropped {quantity} {resource}.")
    else:
        print(f"You don’t have enough {resource}.")

def main():
    init_database()
    conn = sqlite3.connect(DB_FILE)
    admin = Administrator("Alex", 5)  # Start in Central (id=5)
    print("Welcome to the Flood Emergency Response Model.")
    look(conn, admin)
    
    while True:
        command = input("\nCommand (north/south/east/west/look/pickup/putdown/exit): ").strip().lower()
        if command == "exit":
            print("Exiting model. Goodbye.")
            break
        elif command == "look":
            look(conn, admin)
        elif command in ["north", "south", "east", "west"]:
            if move(conn, admin, command):
                look(conn, admin)
            else:
                print("Can’t move that way.")
        elif command.startswith("pickup "):
            try:
                _, resource, qty = command.split()
                pickup(conn, admin, resource, int(qty))
            except ValueError:
                print("Use: pickup <resource> <quantity>")
        elif command.startswith("putdown "):
            try:
                _, resource, qty = command.split()
                putdown(conn, admin, resource, int(qty))
            except ValueError:
                print("Use: putdown <resource> <quantity>")
        else:
            print("Invalid command.")

    conn.close()

if __name__ == "__main__":
    main()
