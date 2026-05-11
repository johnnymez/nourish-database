import sqlite3

DB_NAME = "final_project-1.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def add_household():
    name = input("Household name: ")
    barcode = input("Barcode: ")
    phone = input("Phone: ")
    email = input("Email: ")
    zip_code = input("Zip code: ")
    language = input("Preferred language: ")

    num_adults = int(input("Number of adults: "))
    num_children = int(input("Number of children: "))
    num_seniors = int(input("Number of seniors: "))
    registration_date = input("Registration date (YYYY-MM-DD): ")
    tfap_certified = int(input("TFAP certified? (1=yes, 0=no): "))
    certification_date = input("Certification date (YYYY-MM-DD, blank if none): ")
    active_status = int(input("Active status? (1=active, 0=inactive): "))

    with connect() as conn:
        conn.execute("""
            INSERT INTO Household
            (barcode, household_name, phone, email, zip_code, preferred_language,
             active_status, num_adults, num_children, num_seniors,
             registration_date, tfap_certified, certification_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            barcode, name, phone, email, zip_code, language, active_status,
            num_adults, num_children, num_seniors, registration_date,
            tfap_certified, certification_date
        ))

    print("Household added.\n")


def add_volunteer():
    first = input("First name: ")
    last = input("Last name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    hours = int(input("Hours: "))

    with connect() as conn:
        conn.execute("""
            INSERT INTO Volunteer
            (first_name, last_name, phone, email, hours)
            VALUES (?, ?, ?, ?, ?)
        """, (first, last, phone, email, hours))

    print("Volunteer added.\n")


def add_donation_source():
    name = input("Source name: ")
    source_type = input("Source type: ")
    contact = input("Contact info: ")

    with connect() as conn:
        conn.execute("""
            INSERT INTO DonationSource
            (source_name, source_type, contact_info)
            VALUES (?, ?, ?)
        """, (name, source_type, contact))

    print("Donation source added.\n")


def add_inventory_item():
    name = input("Item name: ")
    category = input("Category: ")
    unit_type = input("Unit type: ")
    quality = input("Quality status: ")

    with connect() as conn:
        conn.execute("""
            INSERT INTO InventoryItem
            (item_name, category, unit_type, quality_status)
            VALUES (?, ?, ?, ?)
        """, (name, category, unit_type, quality))

    print("Inventory item added.\n")


def add_inventory_lot():
    view_inventory_items()
    view_donation_sources()

    item_id = int(input("Item ID: "))
    source_id = int(input("Source ID: "))
    quantity = float(input("Quantity received: "))
    unit_type = input("Unit type: ")
    date_received = input("Date received (YYYY-MM-DD): ")
    expiration = input("Expiration date (YYYY-MM-DD or blank): ")
    perishable = int(input("Perishable? (1=yes, 0=no): "))
    location = input("Storage location: ")

    with connect() as conn:
        conn.execute("""
            INSERT INTO InventoryLot
            (item_id, source_id, quantity_received, unit_type, date_received,
             expiration_date, perishable, storage_location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id, source_id, quantity, unit_type, date_received,
            expiration, perishable, location
        ))

    print("Inventory lot added.\n")


def record_visit():
    view_households()
    view_volunteers()

    household_id = int(input("Household ID: "))
    volunteer_id = int(input("Volunteer ID: "))
    visit_date = input("Visit date (YYYY-MM-DD): ")
    checkin_time = input("Check-in time (HH:MM): ")
    pounds_taken = float(input("Pounds taken: "))
    pickup_type = input("Pickup type: ")
    notes = input("Notes: ")

    with connect() as conn:
        cursor = conn.execute("""
            INSERT INTO Visit
            (household_id, volunteer_id, visit_date, checkin_time,
             pounds_taken, pickup_type, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            household_id, volunteer_id, visit_date, checkin_time,
            pounds_taken, pickup_type, notes
        ))

        visit_id = cursor.lastrowid

    print(f"Visit recorded. New visit ID: {visit_id}\n")


def add_distribution_item():
    view_visits()
    view_inventory_lots()

    visit_id = int(input("Visit ID: "))
    lot_id = int(input("Inventory lot ID: "))
    quantity = float(input("Quantity given: "))
    unit_type = input("Unit type: ")

    with connect() as conn:
        conn.execute("""
            INSERT INTO DistributionItem
            (visit_id, lot_id, quantity_given, unit_type)
            VALUES (?, ?, ?, ?)
        """, (visit_id, lot_id, quantity, unit_type))

    print("Distribution item added.\n")


def add_proxy():
    view_households()

    household_id = int(input("Household ID: "))
    proxy_name = input("Proxy name: ")
    phone = input("Phone: ")
    relationship = input("Relationship: ")

    with connect() as conn:
        conn.execute("""
            INSERT INTO Proxy
            (household_id, proxy_name, phone, relationship)
            VALUES (?, ?, ?, ?)
        """, (household_id, proxy_name, phone, relationship))

    print("Proxy added.\n")


def view_households():
    with connect() as conn:
        rows = conn.execute("""
            SELECT household_id, household_name, phone, zip_code, active_status
            FROM Household
            ORDER BY household_id
        """).fetchall()

    print("\nHouseholds:")
    for row in rows:
        print(dict(row))
    print()


def view_volunteers():
    with connect() as conn:
        rows = conn.execute("""
            SELECT volunteer_id, first_name, last_name, phone, email, hours
            FROM Volunteer
            ORDER BY volunteer_id
        """).fetchall()

    print("\nVolunteers:")
    for row in rows:
        print(dict(row))
    print()


def view_donation_sources():
    with connect() as conn:
        rows = conn.execute("""
            SELECT source_id, source_name, source_type, contact_info
            FROM DonationSource
            ORDER BY source_id
        """).fetchall()

    print("\nDonation Sources:")
    for row in rows:
        print(dict(row))
    print()


def view_inventory_items():
    with connect() as conn:
        rows = conn.execute("""
            SELECT item_id, item_name, category, unit_type, quality_status
            FROM InventoryItem
            ORDER BY item_id
        """).fetchall()

    print("\nInventory Items:")
    for row in rows:
        print(dict(row))
    print()


def view_inventory_lots():
    with connect() as conn:
        rows = conn.execute("""
            SELECT
                il.lot_id,
                ii.item_name,
                ds.source_name,
                il.quantity_received,
                il.unit_type,
                il.date_received,
                il.expiration_date,
                il.perishable,
                il.storage_location
            FROM InventoryLot il
            JOIN InventoryItem ii ON il.item_id = ii.item_id
            JOIN DonationSource ds ON il.source_id = ds.source_id
            ORDER BY il.lot_id
        """).fetchall()

    print("\nInventory Lots:")
    for row in rows:
        print(dict(row))
    print()


def view_visits():
    with connect() as conn:
        rows = conn.execute("""
            SELECT
                v.visit_id,
                h.household_name,
                vol.first_name || ' ' || vol.last_name AS volunteer,
                v.visit_date,
                v.checkin_time,
                v.pounds_taken,
                v.pickup_type,
                v.notes
            FROM Visit v
            JOIN Household h ON v.household_id = h.household_id
            JOIN Volunteer vol ON v.volunteer_id = vol.volunteer_id
            ORDER BY v.visit_id
        """).fetchall()

    print("\nVisits:")
    for row in rows:
        print(dict(row))
    print()


def view_proxies():
    with connect() as conn:
        rows = conn.execute("""
            SELECT
                p.proxy_id,
                h.household_name,
                p.proxy_name,
                p.phone,
                p.relationship
            FROM Proxy p
            JOIN Household h ON p.household_id = h.household_id
            ORDER BY h.household_name
        """).fetchall()

    print("\nProxies:")
    for row in rows:
        print(dict(row))
    print()


def view_inventory_remaining():
    with connect() as conn:
        rows = conn.execute("""
            SELECT
                il.lot_id,
                ii.item_name,
                il.quantity_received,
                COALESCE(SUM(di.quantity_given), 0) AS quantity_given,
                il.quantity_received - COALESCE(SUM(di.quantity_given), 0) AS quantity_remaining,
                il.unit_type,
                il.expiration_date,
                il.storage_location
            FROM InventoryLot il
            JOIN InventoryItem ii ON il.item_id = ii.item_id
            LEFT JOIN DistributionItem di ON il.lot_id = di.lot_id
            GROUP BY il.lot_id
            ORDER BY ii.item_name
        """).fetchall()

    print("\nInventory Remaining:")
    for row in rows:
        print(dict(row))
    print()


def view_visit_history():
    view_households()

    household_id = int(input("Household ID: "))

    with connect() as conn:
        rows = conn.execute("""
            SELECT
                v.visit_id,
                h.household_name,
                v.visit_date,
                v.checkin_time,
                v.pounds_taken,
                v.pickup_type,
                vol.first_name || ' ' || vol.last_name AS volunteer,
                v.notes
            FROM Visit v
            JOIN Household h ON v.household_id = h.household_id
            JOIN Volunteer vol ON v.volunteer_id = vol.volunteer_id
            WHERE h.household_id = ?
            ORDER BY v.visit_date DESC
        """, (household_id,)).fetchall()

    print("\nVisit History:")
    for row in rows:
        print(dict(row))
    print()


def main():
    while True:
        print("""
Food Pantry Distribution System

1. Add household
2. Add volunteer
3. Add donation source
4. Add inventory item
5. Add inventory lot
6. Record household visit
7. Add distributed item to visit
8. Add proxy for household

9. View households
10. View volunteers
11. View donation sources
12. View inventory items
13. View inventory lots
14. View visits
15. View proxies
16. View inventory remaining
17. View household visit history

0. Exit
""")

        choice = input("Choose an option: ")

        if choice == "1":
            add_household()
        elif choice == "2":
            add_volunteer()
        elif choice == "3":
            add_donation_source()
        elif choice == "4":
            add_inventory_item()
        elif choice == "5":
            add_inventory_lot()
        elif choice == "6":
            record_visit()
        elif choice == "7":
            add_distribution_item()
        elif choice == "8":
            add_proxy()
        elif choice == "9":
            view_households()
        elif choice == "10":
            view_volunteers()
        elif choice == "11":
            view_donation_sources()
        elif choice == "12":
            view_inventory_items()
        elif choice == "13":
            view_inventory_lots()
        elif choice == "14":
            view_visits()
        elif choice == "15":
            view_proxies()
        elif choice == "16":
            view_inventory_remaining()
        elif choice == "17":
            view_visit_history()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()