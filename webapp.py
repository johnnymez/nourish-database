import html
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, quote, unquote, urlparse


DB_NAME = "final_project-1.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def rows(query, values=()):
    with connect() as conn:
        return conn.execute(query, values).fetchall()


def execute(query, values=()):
    with connect() as conn:
        conn.execute(query, values)


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value))


def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def table(title, data):
    if not data:
        return f"<section><h2>{esc(title)}</h2><p class='empty'>No records yet.</p></section>"

    headers = data[0].keys()
    head = "".join(f"<th>{esc(header.replace('_', ' ').title())}</th>" for header in headers)
    body = ""
    for row in data:
        cells = "".join(f"<td>{esc(row[header])}</td>" for header in headers)
        body += f"<tr>{cells}</tr>"

    return f"""
    <section>
        <h2>{esc(title)}</h2>
        <div class="table-wrap">
            <table>
                <thead><tr>{head}</tr></thead>
                <tbody>{body}</tbody>
            </table>
        </div>
    </section>
    """


def input_field(label, name, field_type="text", required=False, value=""):
    req = " required" if required else ""
    return (
        f"<label>{esc(label)}"
        f"<input type='{field_type}' name='{esc(name)}' value='{esc(value)}'{req}>"
        "</label>"
    )


def select_field(label, name, options, display):
    option_html = ""
    for row in options:
        option_html += f"<option value='{esc(row[0])}'>{esc(display(row))}</option>"
    return f"<label>{esc(label)}<select name='{esc(name)}'>{option_html}</select></label>"


def page(content, message=""):
    alert = f"<div class='message'>{esc(message)}</div>" if message else ""
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Nourish Database</title>
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            background: #f6f7f4;
            color: #20231f;
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.45;
        }}

        header {{
            background: #315c45;
            color: white;
            padding: 24px 32px;
        }}

        header h1 {{
            margin: 0 0 4px;
            font-size: 28px;
        }}

        header p {{
            margin: 0;
            color: #e6efe8;
        }}

        nav {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            padding: 14px 32px;
            background: white;
            border-bottom: 1px solid #d9ded8;
        }}

        nav a {{
            color: #315c45;
            text-decoration: none;
            border: 1px solid #b8c7bc;
            border-radius: 6px;
            padding: 8px 10px;
            font-size: 14px;
            background: #fbfcfa;
        }}

        main {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 24px 24px 48px;
        }}

        section {{
            margin-bottom: 24px;
        }}

        h2 {{
            margin: 0 0 12px;
            font-size: 20px;
            color: #263b2f;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
        }}

        form {{
            background: white;
            border: 1px solid #d9ded8;
            border-radius: 8px;
            padding: 16px;
        }}

        label {{
            display: block;
            font-weight: 700;
            font-size: 13px;
            color: #2e3a33;
            margin-bottom: 10px;
        }}

        input, select, textarea {{
            width: 100%;
            margin-top: 4px;
            border: 1px solid #bcc8c0;
            border-radius: 6px;
            padding: 8px;
            font: inherit;
            background: white;
        }}

        textarea {{
            min-height: 76px;
            resize: vertical;
        }}

        button {{
            border: 0;
            border-radius: 6px;
            background: #315c45;
            color: white;
            padding: 9px 12px;
            font-weight: 700;
            cursor: pointer;
        }}

        .message {{
            background: #e5f2e8;
            border: 1px solid #adc9b5;
            border-radius: 6px;
            color: #1f4d31;
            padding: 10px 12px;
            margin-bottom: 18px;
        }}

        .table-wrap {{
            overflow-x: auto;
            background: white;
            border: 1px solid #d9ded8;
            border-radius: 8px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 720px;
        }}

        th, td {{
            text-align: left;
            padding: 9px 10px;
            border-bottom: 1px solid #e5e8e3;
            vertical-align: top;
            font-size: 14px;
        }}

        th {{
            background: #edf2ed;
            color: #263b2f;
        }}

        .empty {{
            background: white;
            border: 1px solid #d9ded8;
            border-radius: 8px;
            padding: 16px;
            color: #657064;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Nourish Database System</h1>
        <p>Food pantry household, visit, volunteer, donation, and inventory tracking.</p>
    </header>
    <nav>
        <a href="/">Dashboard</a>
        <a href="/households">Households</a>
        <a href="/inventory">Inventory</a>
        <a href="/visits">Visits</a>
        <a href="/volunteers">Volunteers</a>
        <a href="/donations">Donation Sources</a>
        <a href="/proxies">Proxies</a>
    </nav>
    <main>
        {alert}
        {content}
    </main>
</body>
</html>"""


def dashboard(message=""):
    counts = {
        "Households": rows("SELECT COUNT(*) AS count FROM Household")[0]["count"],
        "Volunteers": rows("SELECT COUNT(*) AS count FROM Volunteer")[0]["count"],
        "Inventory Items": rows("SELECT COUNT(*) AS count FROM InventoryItem")[0]["count"],
        "Inventory Lots": rows("SELECT COUNT(*) AS count FROM InventoryLot")[0]["count"],
        "Visits": rows("SELECT COUNT(*) AS count FROM Visit")[0]["count"],
        "Proxies": rows("SELECT COUNT(*) AS count FROM Proxy")[0]["count"],
    }
    cards = "".join(
        f"<form><h2>{esc(name)}</h2><p class='empty'>{esc(count)} records</p></form>"
        for name, count in counts.items()
    )
    inventory = inventory_remaining_table()
    return page(f"<section><h2>Dashboard</h2><div class='grid'>{cards}</div></section>{inventory}", message)


def household_page(message=""):
    form = f"""
    <section>
        <h2>Add Household</h2>
        <form method="post" action="/add-household" class="grid">
            {input_field("Household Name", "household_name", required=True)}
            {input_field("Barcode", "barcode")}
            {input_field("Phone", "phone")}
            {input_field("Email", "email", "email")}
            {input_field("Zip Code", "zip_code")}
            {input_field("Preferred Language", "preferred_language")}
            {input_field("Number of Adults", "num_adults", "number", value="0")}
            {input_field("Number of Children", "num_children", "number", value="0")}
            {input_field("Number of Seniors", "num_seniors", "number", value="0")}
            {input_field("Registration Date", "registration_date", "date")}
            <label>TFAP Certified
                <select name="tfap_certified"><option value="1">Yes</option><option value="0">No</option></select>
            </label>
            {input_field("Certification Date", "certification_date", "date")}
            <label>Active Status
                <select name="active_status"><option value="1">Active</option><option value="0">Inactive</option></select>
            </label>
            <label>&nbsp;<button type="submit">Add Household</button></label>
        </form>
    </section>
    """
    data = rows("""
        SELECT household_id, barcode, household_name, phone, email, zip_code,
               preferred_language, active_status, num_adults, num_children, num_seniors
        FROM Household
        ORDER BY household_id
    """)
    return page(form + table("Households", data), message)


def volunteers_page(message=""):
    form = f"""
    <section>
        <h2>Add Volunteer</h2>
        <form method="post" action="/add-volunteer" class="grid">
            {input_field("First Name", "first_name", required=True)}
            {input_field("Last Name", "last_name", required=True)}
            {input_field("Phone", "phone")}
            {input_field("Email", "email", "email")}
            {input_field("Hours", "hours", "number", value="0")}
            <label>&nbsp;<button type="submit">Add Volunteer</button></label>
        </form>
    </section>
    """
    data = rows("SELECT volunteer_id, first_name, last_name, phone, email, hours FROM Volunteer ORDER BY volunteer_id")
    return page(form + table("Volunteers", data), message)


def donations_page(message=""):
    form = f"""
    <section>
        <h2>Add Donation Source</h2>
        <form method="post" action="/add-donation-source" class="grid">
            {input_field("Source Name", "source_name", required=True)}
            {input_field("Source Type", "source_type")}
            {input_field("Contact Info", "contact_info")}
            <label>&nbsp;<button type="submit">Add Source</button></label>
        </form>
    </section>
    """
    data = rows("SELECT source_id, source_name, source_type, contact_info FROM DonationSource ORDER BY source_id")
    return page(form + table("Donation Sources", data), message)


def inventory_remaining_table():
    data = rows("""
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
    """)
    return table("Inventory Remaining", data)


def inventory_page(message=""):
    items = rows("SELECT item_id, item_name, category, unit_type, quality_status FROM InventoryItem ORDER BY item_id")
    sources = rows("SELECT source_id, source_name FROM DonationSource ORDER BY source_name")
    item_form = f"""
    <section>
        <h2>Add Inventory Item</h2>
        <form method="post" action="/add-inventory-item" class="grid">
            {input_field("Item Name", "item_name", required=True)}
            {input_field("Category", "category")}
            {input_field("Unit Type", "unit_type")}
            {input_field("Quality Status", "quality_status")}
            <label>&nbsp;<button type="submit">Add Item</button></label>
        </form>
    </section>
    """
    lot_form = f"""
    <section>
        <h2>Add Inventory Lot</h2>
        <form method="post" action="/add-inventory-lot" class="grid">
            {select_field("Inventory Item", "item_id", items, lambda row: row["item_name"])}
            {select_field("Donation Source", "source_id", sources, lambda row: row["source_name"])}
            {input_field("Quantity Received", "quantity_received", "number", value="0")}
            {input_field("Unit Type", "unit_type")}
            {input_field("Date Received", "date_received", "date")}
            {input_field("Expiration Date", "expiration_date", "date")}
            <label>Perishable
                <select name="perishable"><option value="1">Yes</option><option value="0">No</option></select>
            </label>
            {input_field("Storage Location", "storage_location")}
            <label>&nbsp;<button type="submit">Add Lot</button></label>
        </form>
    </section>
    """
    lots = rows("""
        SELECT il.lot_id, ii.item_name, ds.source_name, il.quantity_received,
               il.unit_type, il.date_received, il.expiration_date, il.perishable,
               il.storage_location
        FROM InventoryLot il
        JOIN InventoryItem ii ON il.item_id = ii.item_id
        JOIN DonationSource ds ON il.source_id = ds.source_id
        ORDER BY il.lot_id
    """)
    return page(item_form + lot_form + table("Inventory Items", items) + table("Inventory Lots", lots) + inventory_remaining_table(), message)


def visits_page(message=""):
    households = rows("SELECT household_id, household_name FROM Household ORDER BY household_name")
    volunteers = rows("SELECT volunteer_id, first_name, last_name FROM Volunteer ORDER BY last_name, first_name")
    visits = rows("""
        SELECT v.visit_id, h.household_name,
               vol.first_name || ' ' || vol.last_name AS volunteer,
               v.visit_date, v.checkin_time, v.pounds_taken, v.pickup_type, v.notes
        FROM Visit v
        JOIN Household h ON v.household_id = h.household_id
        JOIN Volunteer vol ON v.volunteer_id = vol.volunteer_id
        ORDER BY v.visit_id
    """)
    lots = rows("""
        SELECT il.lot_id, ii.item_name, il.quantity_received, il.unit_type
        FROM InventoryLot il
        JOIN InventoryItem ii ON il.item_id = ii.item_id
        ORDER BY il.lot_id
    """)
    visit_form = f"""
    <section>
        <h2>Record Visit</h2>
        <form method="post" action="/add-visit" class="grid">
            {select_field("Household", "household_id", households, lambda row: row["household_name"])}
            {select_field("Volunteer", "volunteer_id", volunteers, lambda row: row["first_name"] + " " + row["last_name"])}
            {input_field("Visit Date", "visit_date", "date")}
            {input_field("Check-in Time", "checkin_time", "time")}
            {input_field("Pounds Taken", "pounds_taken", "number", value="0")}
            {input_field("Pickup Type", "pickup_type")}
            <label>Notes<textarea name="notes"></textarea></label>
            <label>&nbsp;<button type="submit">Record Visit</button></label>
        </form>
    </section>
    """
    distribution_form = f"""
    <section>
        <h2>Add Distributed Item</h2>
        <form method="post" action="/add-distribution" class="grid">
            {select_field("Visit", "visit_id", visits, lambda row: "Visit " + str(row["visit_id"]) + " - " + row["household_name"])}
            {select_field("Inventory Lot", "lot_id", lots, lambda row: "Lot " + str(row["lot_id"]) + " - " + row["item_name"])}
            {input_field("Quantity Given", "quantity_given", "number", value="0")}
            {input_field("Unit Type", "unit_type")}
            <label>&nbsp;<button type="submit">Add Distributed Item</button></label>
        </form>
    </section>
    """
    distributed = rows("""
        SELECT di.distribution_item_id, di.visit_id, ii.item_name, di.quantity_given, di.unit_type
        FROM DistributionItem di
        JOIN InventoryLot il ON di.lot_id = il.lot_id
        JOIN InventoryItem ii ON il.item_id = ii.item_id
        ORDER BY di.distribution_item_id
    """)
    return page(visit_form + distribution_form + table("Visits", visits) + table("Distributed Items", distributed), message)


def proxies_page(message=""):
    households = rows("SELECT household_id, household_name FROM Household ORDER BY household_name")
    form = f"""
    <section>
        <h2>Add Proxy</h2>
        <form method="post" action="/add-proxy" class="grid">
            {select_field("Household", "household_id", households, lambda row: row["household_name"])}
            {input_field("Proxy Name", "proxy_name", required=True)}
            {input_field("Phone", "phone")}
            {input_field("Relationship", "relationship")}
            <label>&nbsp;<button type="submit">Add Proxy</button></label>
        </form>
    </section>
    """
    data = rows("""
        SELECT p.proxy_id, h.household_name, p.proxy_name, p.phone, p.relationship
        FROM Proxy p
        JOIN Household h ON p.household_id = h.household_id
        ORDER BY h.household_name
    """)
    return page(form + table("Proxies", data), message)


class NourishHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        message = parse_qs(parsed.query).get("message", [""])[0]
        pages = {
            "/": dashboard,
            "/households": household_page,
            "/inventory": inventory_page,
            "/visits": visits_page,
            "/volunteers": volunteers_page,
            "/donations": donations_page,
            "/proxies": proxies_page,
        }
        if parsed.path in pages:
            self.respond(pages[parsed.path](unquote(message)))
        else:
            self.send_error(404, "Page not found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = parse_qs(self.rfile.read(length).decode("utf-8"))
        values = {key: item[0] if item else "" for key, item in data.items()}

        try:
            redirect_to, message = self.save_post(self.path, values)
        except sqlite3.Error as error:
            redirect_to, message = "/", f"Database error: {error}"

        self.send_response(303)
        self.send_header("Location", f"{redirect_to}?message={quote(message)}")
        self.end_headers()

    def save_post(self, path, values):
        if path == "/add-household":
            execute("""
                INSERT INTO Household
                (barcode, household_name, phone, email, zip_code, preferred_language,
                 active_status, num_adults, num_children, num_seniors,
                 registration_date, tfap_certified, certification_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                values.get("barcode", ""),
                values.get("household_name", ""),
                values.get("phone", ""),
                values.get("email", ""),
                values.get("zip_code", ""),
                values.get("preferred_language", ""),
                to_int(values.get("active_status"), 1),
                to_int(values.get("num_adults")),
                to_int(values.get("num_children")),
                to_int(values.get("num_seniors")),
                values.get("registration_date", ""),
                to_int(values.get("tfap_certified")),
                values.get("certification_date", ""),
            ))
            return "/households", "Household added."

        if path == "/add-volunteer":
            execute("""
                INSERT INTO Volunteer (first_name, last_name, phone, email, hours)
                VALUES (?, ?, ?, ?, ?)
            """, (
                values.get("first_name", ""),
                values.get("last_name", ""),
                values.get("phone", ""),
                values.get("email", ""),
                to_int(values.get("hours")),
            ))
            return "/volunteers", "Volunteer added."

        if path == "/add-donation-source":
            execute("""
                INSERT INTO DonationSource (source_name, source_type, contact_info)
                VALUES (?, ?, ?)
            """, (
                values.get("source_name", ""),
                values.get("source_type", ""),
                values.get("contact_info", ""),
            ))
            return "/donations", "Donation source added."

        if path == "/add-inventory-item":
            execute("""
                INSERT INTO InventoryItem (item_name, category, unit_type, quality_status)
                VALUES (?, ?, ?, ?)
            """, (
                values.get("item_name", ""),
                values.get("category", ""),
                values.get("unit_type", ""),
                values.get("quality_status", ""),
            ))
            return "/inventory", "Inventory item added."

        if path == "/add-inventory-lot":
            execute("""
                INSERT INTO InventoryLot
                (item_id, source_id, quantity_received, unit_type, date_received,
                 expiration_date, perishable, storage_location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                to_int(values.get("item_id")),
                to_int(values.get("source_id")),
                to_float(values.get("quantity_received")),
                values.get("unit_type", ""),
                values.get("date_received", ""),
                values.get("expiration_date", ""),
                to_int(values.get("perishable")),
                values.get("storage_location", ""),
            ))
            return "/inventory", "Inventory lot added."

        if path == "/add-visit":
            execute("""
                INSERT INTO Visit
                (household_id, volunteer_id, visit_date, checkin_time,
                 pounds_taken, pickup_type, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                to_int(values.get("household_id")),
                to_int(values.get("volunteer_id")),
                values.get("visit_date", ""),
                values.get("checkin_time", ""),
                to_float(values.get("pounds_taken")),
                values.get("pickup_type", ""),
                values.get("notes", ""),
            ))
            return "/visits", "Visit recorded."

        if path == "/add-distribution":
            execute("""
                INSERT INTO DistributionItem (visit_id, lot_id, quantity_given, unit_type)
                VALUES (?, ?, ?, ?)
            """, (
                to_int(values.get("visit_id")),
                to_int(values.get("lot_id")),
                to_float(values.get("quantity_given")),
                values.get("unit_type", ""),
            ))
            return "/visits", "Distributed item added."

        if path == "/add-proxy":
            execute("""
                INSERT INTO Proxy (household_id, proxy_name, phone, relationship)
                VALUES (?, ?, ?, ?)
            """, (
                to_int(values.get("household_id")),
                values.get("proxy_name", ""),
                values.get("phone", ""),
                values.get("relationship", ""),
            ))
            return "/proxies", "Proxy added."

        return "/", "Unknown action."

    def respond(self, body):
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), NourishHandler)
    print("Nourish web interface running at http://localhost:8000")
    print(f"Using database: {DB_NAME}")
    print("The web interface adds rows to the existing database without changing its schema.")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
