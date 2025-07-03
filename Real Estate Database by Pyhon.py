import sqlite3
import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
faker = Faker()

# Database and Excel file setup
db_name = "real_estate.db"
excel_file = "real_estate_data.xlsx"

# Connect to SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Function to generate random American phone numbers
def generate_phone():
    return f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

# Function to generate random dates
def random_date(start_year, end_year):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Function to generate email based on name components
def generate_email(first_name, middle_name):
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com"])
    random_digits = random.randint(10, 9999)
    return f"{first_name.lower()}.{middle_name.lower()}.{random_digits}@{domain}"

# Function to create the property lists
def divide_numbers(total_numbers):
    owned_list_size = 625
    rented_list_size = 310
    available_list_size = total_numbers - owned_list_size - rented_list_size

    numbers = list(range(1, total_numbers + 1))
    random.shuffle(numbers)

    owned_list = numbers[:owned_list_size]
    rented_list = numbers[owned_list_size:owned_list_size + rented_list_size]
    available_list = numbers[owned_list_size + rented_list_size:]

    return owned_list, rented_list, available_list

# Generate property lists
owned_list, rented_list, available_list = divide_numbers(1000)


# Create Properties table
cursor.execute("""
CREATE TABLE Properties (
    Property_ID INTEGER PRIMARY KEY,
    Address TEXT,
    Type TEXT,
    Status TEXT,
    Price REAL,
    Size INTEGER,
    Year_Built INTEGER,
    Bedrooms INTEGER,
    Bathrooms INTEGER
)
""")

properties = []

for i in range(1, 1001):
    address = faker.address().replace("\n", ", ")
    property_type = random.choice(["Residential", "Commercial"])

    # Determine property status based on its presence in the lists
    if i in owned_list:
        status = "Owned"
    elif i in rented_list:
        status = "Rented"
    elif i in available_list:
        status = "Available"
    else:
        raise ValueError(f"Property ID {i} is not in any list.")

    # Set price based on status
    if status == "Rented":
        price = random.randint(1000, 5000)
    else:
        price = random.randint(200_000, 2_000_000)

    # Set size based on property type
    size = random.randint(70, 500) if property_type == "Residential" else random.randint(100, 1000)
    
    # Generate other property details
    year_built = random.randint(2000, 2010)
    bedrooms = random.randint(1, 4)
    bathrooms = random.randint(1, 3)

    # Append the property details
    properties.append((i, address, property_type, status, price, size, year_built, bedrooms, bathrooms))

# Insert data into Properties table
cursor.executemany("""
INSERT INTO Properties (Property_ID, Address, Type, Status, Price, Size, Year_Built, Bedrooms, Bathrooms)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", properties)


# Create Owners table
cursor.execute("""
CREATE TABLE Owners (
    Owner_ID INTEGER PRIMARY KEY,
    F_Name TEXT,
    L_Name TEXT,
    Middle_Name TEXT,
    Phone TEXT,
    Email TEXT,
    Date_Of_Birth DATE,
    Address TEXT
)
""")

owners = []
for i in range(1001, 1251):
    first_name = faker.first_name()
    last_name = faker.last_name()
    middle_name = faker.first_name()
    phone = generate_phone()
    email = generate_email(first_name, middle_name)
    date_of_birth = random_date(1975, 2000).strftime('%Y-%m-%d')
    address = faker.address().replace("\n", ", ")
    owners.append((i, first_name, last_name, middle_name, phone, email, date_of_birth, address))

    
cursor.executemany("""
INSERT INTO Owners (Owner_ID, F_Name, L_Name, Middle_Name, Phone, Email, Date_Of_Birth, Address)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", owners)

# Create Agents table
cursor.execute("""
CREATE TABLE Agents (
    Agent_ID INTEGER PRIMARY KEY,
    F_Name TEXT,
    L_Name TEXT,
    Middle_Name TEXT,
    Phone TEXT,
    Email TEXT,
    Agency TEXT,
    Experience INTEGER,
    Commission_Rate REAL
)
""")

agency_names = [
    "Realty Associates", "Heritage Homes", "Century Properties", "Legacy Realty", "Sterling Realty",
    "Future Homes", "NextGen Realty", "Modern Living Properties", "Tech Realty", "Urban Edge Realty",
    "Neighborhood Realty", "Hometown Properties", "Local Legends Realty", "Community Choice Realty", "Neighborly Homes",
    "Premier Properties", "Elite Estates", "Luxury Living Realty", "Exclusive Estates", "Opulent Homes",
    "Home Sweet Home Realty", "Key Realty", "House Hunters Realty", "Property Pros", "Real Estate Solutions",
    "Dream Homes Realty", "The Key to Your Home", "Your Perfect Place", "Homeward Bound Realty", "Nest Egg Realty",
    "Buyer's Choice Realty", "Seller's Advantage Realty", "Investor's Edge Realty", "Rental Solutions Realty", "Commercial Corner Realty",
    "The Happy Home Hunters", "The Home Sweet Home Team", "The House Whisperers", "The Property Ninjas", "The Real Estate Wizards"
]

agents = []
for i in range(501, 551):
    first_name = faker.first_name()
    last_name = faker.last_name()
    middle_name = faker.first_name()
    phone = generate_phone()
    email = generate_email(first_name, middle_name)
    agency = random.choice(["Realty Associates", "Heritage Homes", "Century Properties"])
    experience = random.randint(1, 10)
    commission_rate = round(random.uniform(4, 7), 2)
    agents.append((i, first_name, last_name, middle_name, phone, email, agency, experience, commission_rate))

    
cursor.executemany("""
INSERT INTO Agents (Agent_ID, F_Name, L_Name, Middle_Name, Phone, Email, Agency, Experience, Commission_Rate)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", agents)

# Create MaintenanceRequests table
cursor.execute("""
CREATE TABLE MaintenanceRequests (
    Request_ID INTEGER PRIMARY KEY,
    Property_ID INTEGER,
    Date_Submitted DATE,
    Issue_Description TEXT,
    Status TEXT,
    Date_Resolved DATE,
    Cost REAL
)
""")

maintenance_requests = []
issue_descriptions = [
    "Ant infestation in the kitchen",
    "Cockroach infestation in the bathroom",
    "Rodent infestation in the attic or basement",
    "Bed bug infestation in the bedroom",
    "Slow-draining bathtub",
    "Leaky toilet tank",
    "Water heater not heating water to the desired temperature",
    "Clogged kitchen sink disposal",
    "Water damage in the basement",
    "Dimming lights in certain rooms",
    "Frequent tripping of circuit breakers",
    "Electrical outlets not working",
    "Buzzing sound from electrical outlets",
    "Flickering lights",
    "Uneven heating or cooling in different rooms",
    "High energy bills due to inefficient HVAC system",
    "Strange noises coming from the HVAC unit",
    "HVAC system not turning on or off as scheduled",
    "Poor air quality due to inadequate ventilation",
    "Refrigerator not cooling or freezing properly",
    "Dishwasher not cleaning dishes effectively",
    "Stove or oven not heating correctly",
    "Washing machine not draining or spinning properly",
    "Dryer not drying clothes efficiently",
    "Broken or malfunctioning security system",
    "Unauthorized access to the property",
    "Suspicious activity in the neighborhood",
    "Lost or stolen keys",
    "Damaged or missing roof shingles",
    "Leaky gutters or downspouts",
    "Cracked or uneven driveway or walkway",
    "Peeling paint on the exterior walls",
    "Damaged or overgrown landscaping",
    "Faulty outdoor lighting","Scratched or damaged flooring",
    "Water stains on the ceiling or walls",
    "Mold or mildew growth in damp areas",
    "Squeaky floors or doors",
    "Drafty windows or doors",
    "Damaged or missing ceiling tiles",
    "Loud noise from neighbors",
    "Excessive noise from traffic or construction",
    "Noise from pets or children",
    "Vandalism or graffiti",
    "Water damage from a leak or flood",
    "Fire damage",
    "Storm damage (e.g., wind, hail, lightning)",
    "Accidental damage (e.g., broken windows, damaged walls)"
]

# Generate 150 maintenance requests
pending_or_in_progress_indices = random.sample(range(150), 20)

for i in range(3001, 3151):
    property_id = random.randint(1, 1001)

    # Determine if the row should have "Pending" or "In Progress" status
    if i - 1 in pending_or_in_progress_indices:
        status = random.choice(["Pending", "In Progress"])
        date_resolved = None
        # Request date between September and December 2024
        date_submitted = datetime.strptime(f"2024-{random.randint(9, 12)}-{random.randint(1, 28)}", "%Y-%m-%d")
    else:
        status = "Resolved"
        date_submitted = random_date(2005, 2024)
        date_resolved = (date_submitted + timedelta(days=random.randint(7, 60))).strftime('%Y-%m-%d')

    issue_description = issue_descriptions[i % len(issue_descriptions)]
    cost = round(random.uniform(100, 1000), 2)

    maintenance_requests.append((
        i,
        property_id,
        date_submitted.strftime('%Y-%m-%d'),
        issue_description,
        status,
        date_resolved,
        cost
    ))

# Insert into the database
cursor.executemany("""
INSERT INTO MaintenanceRequests (Request_ID, Property_ID, Date_Submitted, Issue_Description, Status, Date_Resolved, Cost)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", maintenance_requests)


# Create the Features table
cursor.execute("""
CREATE TABLE Features (
    Feature_ID INTEGER PRIMARY KEY,
    Feature_Description TEXT,
    Feature_Type TEXT,
    Feature_Sub_Type TEXT
)
""")

# Data to populate the Features table
data = [
    (1, 'Swimming Pool', 'Exterior', 'Pool'),
    (2, 'Garage', 'Exterior', 'Garage'),
    (3, 'Fireplace', 'Interior', 'Fireplace'),
    (4, 'Garden', 'Exterior', 'Garden'),
    (5, 'Rooftop', 'Exterior', 'Rooftop'),
    (6, 'Gym', 'Interior', 'Fitness'),
    (7, 'Basement', 'Interior', 'Basement'),
    (8, 'Elevator', 'Interior', 'Accessibility'),
    (9, 'Balcony', 'Exterior', 'Balcony'),
    (10, 'Solar Panels', 'Exterior', 'Energy'),
    (11, 'Smart Home System', 'Technology', 'Smart Home'),
    (12, 'Security System', 'Security', 'Security System'),
    (13, 'Sauna', 'Interior', 'Wellness'),
    (14, 'Jacuzzi', 'Interior', 'Wellness'),
    (15, 'Home Theater', 'Interior', 'Entertainment'),
    (16, 'Green Roof', 'Exterior', 'Rooftop'),
    (17, 'Modern Kitchen', 'Interior', 'Kitchen'),
    (18, 'Playground', 'Exterior', 'Recreation'),
    (19, 'Tennis Court', 'Exterior', 'Recreation'),
    (20, 'Central Air Conditioning', 'Interior', 'Climate Control'),
    (21, 'Spacious Backyard', 'Exterior', 'Yard'),
    (22, 'City View', 'Exterior', 'View'),
    (23, 'Fire Alarm', 'Security', 'Safety'),
    (24, 'Sprinkler System', 'Security', 'Safety'),
    (25, 'Energy-Efficient Appliances', 'Energy Efficiency', 'Appliances'),
    (26, 'Water-Efficient Fixtures', 'Energy Efficiency', 'Fixtures'),
    (27, 'Golf Course', 'Exterior', 'Recreation'),
    (28, 'Home Office', 'Interior', 'Room')
]

# Insert data into the Features table
cursor.executemany("""
INSERT INTO Features (Feature_ID, Feature_Description, Feature_Type, Feature_Sub_Type)
VALUES (?, ?, ?, ?)
""", data)



# Create Sales table
cursor.execute("""
CREATE TABLE Sales (
    Sale_ID INTEGER PRIMARY KEY,
    Property_ID INTEGER,
    Owner_ID INTEGER,
    Sale_Date DATE,
    Sale_Price REAL,
    Agent_ID INTEGER,
    Commission REAL,
    Closing_Costs REAL
)
""")

# Define owner IDs (1001 to 1250)
owner_ids = list(range(1001, 1251))
owner_ids = (owner_ids * ((625 // len(owner_ids)) + 1))[:625]  # Repeat and truncate to 625
random.shuffle(owner_ids)  # Shuffle to randomize the order

# Define agent IDs (501 to 550)
agent_ids = list(range(501, 551))
agent_ids = (agent_ids * ((625 // len(agent_ids)) + 1))[:625]  # Repeat and truncate to 625
random.shuffle(agent_ids)  # Shuffle to randomize the order

# Generate sales data
sales = []
for i, property_id in enumerate(owned_list, start=3001):  # Use all owned_list values without repetition
    owner_id = owner_ids[i % len(owner_ids)]  # Cycle through owner_ids if necessary
    sale_date = random_date(2002, 2024).strftime('%Y-%m-%d')
    sale_price = random.randint(200_000, 2_000_000)
    agent_id = agent_ids[i % len(agent_ids)]  # Cycle through agent_ids if necessary
    commission = round(random.uniform(4, 10), 2)  # Commission range 4% to 10%
    closing_costs = sale_price + random.uniform(1000, 3000)  # Closing costs > sale price by 1000 to 3000
    sales.append((i, property_id, owner_id, sale_date, sale_price, agent_id, commission, closing_costs))

# Insert sales data into the table
cursor.executemany("""
INSERT INTO Sales (Sale_ID, Property_ID, Owner_ID, Sale_Date, Sale_Price, Agent_ID, Commission, Closing_Costs)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", sales)


# Create Tenants table
cursor.execute("""
CREATE TABLE Tenants (
    Tenant_ID INTEGER PRIMARY KEY,
    F_Name TEXT,
    L_Name TEXT,
    Middle_Name TEXT,
    Phone TEXT,
    Email TEXT,
    Date_Of_Birth DATE,
    Address TEXT
)
""")

tenants = []
for i in range(2001, 2201):
    first_name = faker.first_name()
    last_name = faker.last_name()
    middle_name = faker.first_name()
    phone = generate_phone()
    email = generate_email(first_name, middle_name)
    date_of_birth = random_date(1975, 2005).strftime('%Y-%m-%d')
    address = faker.address().replace("\n", ", ")
    tenants.append((i, first_name, last_name, middle_name, phone, email, date_of_birth, address))

cursor.executemany("""
INSERT INTO Tenants (Tenant_ID, F_Name, L_Name, Middle_Name, Phone, Email, Date_Of_Birth, Address)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", tenants)

# Create Rentals table
cursor.execute("""
CREATE TABLE Rentals (
    Rental_ID INTEGER PRIMARY KEY,
    Property_ID INTEGER,
    Tenant_ID INTEGER,
    Start_Date DATE,
    End_Date DATE,
    Monthly_Rent REAL,
    Security_Deposit REAL,
    Agent_ID INTEGER,
    Commission REAL
)
""")

# Define tenant_ids (2001 to 2200) and repeat to match the number of rows
tenant_ids = list(range(2001, 2201))
tenant_ids = (tenant_ids * ((310 // len(tenant_ids)) + 1))[:310]  # Repeat and truncate
random.shuffle(tenant_ids)  # Randomize the order

# Generate Rentals table data
rentals = []
for rental_id, property_id in enumerate(rented_list, start=5001):
    # Use values from the shuffled rented_list for property_id
    tenant_id = tenant_ids.pop()  # Pop tenant IDs to avoid repetition
    start_date = random_date(2002, 2024)
    end_date = start_date + timedelta(days=random.randint(90, 365))  # 3 months to 1 year later
    monthly_rent = random.randint(1000, 5000)  # Monthly rent between 1000 and 5000
    security_deposit = monthly_rent * random.uniform(1, 2)  # 1x to 2x monthly rent
    agent_id = random.randint(501, 550)  # Agent IDs range
    commission = round(random.uniform(4, 10), 2)  # Commission between 4% and 10%

    rentals.append((
        rental_id,
        property_id,
        tenant_id,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        monthly_rent,
        round(security_deposit, 2),
        agent_id,
        commission
    ))


cursor.executemany("""
INSERT INTO Rentals (Rental_ID, Property_ID, Tenant_ID, Start_Date, End_Date, Monthly_Rent, Security_Deposit, Agent_ID, Commission)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rentals)


# Create Rent_Payments table
cursor.execute("""
CREATE TABLE Rent_Payments (
    Payment_ID INTEGER PRIMARY KEY,
    Rental_ID INTEGER,
    Payment_Amount REAL,
    Payment_Date DATE,
    Payment_Method TEXT,
    Status TEXT,
    Notes TEXT,
    Tenant_ID INTEGER,
    Property_ID INTEGER
)
""")

# Tenant ID range
tenant_ids = list(range(2001, 2201))  # Tenant IDs between 2001 and 2200

# Rental period parameters
start_year = 2003
end_year = 2024

# Generate rental start dates for properties
rental_start_dates = {property_id: datetime(random.randint(start_year, end_year - 1), random.randint(1, 12), 1) for property_id in rented_list}

# Assign tenants to properties (1 property -> 1 tenant, 1 tenant -> multiple properties)
tenant_property_pairs = []
assigned_tenants = set()  # Keep track of assigned tenants

for property_id in rented_list:
    if len(assigned_tenants) < len(tenant_ids):  # Ensure we don't exceed available tenants
        tenant_id = random.choice(tenant_ids)
        assigned_tenants.add(tenant_id)
    else:
        tenant_id = random.choice(list(assigned_tenants))  # If all tenants are assigned, reuse one

    tenant_property_pairs.append((tenant_id, property_id))

# Generate payment dates for each tenant-property pair
payment_methods = ["Bank Transfer", "Credit Card", "Cash", "Mobile Payment"]
statuses = ["Completed", "Pending"]

rent_payments = []

for tenant_id, property_id in tenant_property_pairs:
    start_date = rental_start_dates[property_id]
    current_date = start_date + timedelta(days=30)  # Payments start the month after the rental start
    while current_date <= datetime(end_year, 12, 31):
        payment_amount = random.randint(1000, 5000)

        # Set status based on Payment_Date
        if current_date.year == 2024 and current_date.month == 12:
            status = "Pending"
        else:
            status = "Completed"

        # Set payment method only for "Completed" status
        payment_method = random.choice(payment_methods) if status == "Completed" else None

        # Ensure consistency between Status and Notes
        if status == "Completed":
            notes = random.choice(["", "Paid early", "Discount applied"])
        else:  # status == "Pending"
            notes = random.choice(["Payment delayed", "Awaiting confirmation", "Partial payment"])

        # Append a complete payment record
        rent_payments.append((
            None,  # Placeholder for Payment_ID, to be sorted later
            None,  # Placeholder for Rental_ID, to be updated based on Payment_ID
            payment_amount,
            current_date.strftime('%Y-%m-%d'),  # Payment_Date
            payment_method,
            status,
            notes,
            tenant_id,
            property_id
        ))

        current_date += timedelta(days=30)  # Add one month

# Sort payments by Payment_Date
rent_payments.sort(key=lambda x: datetime.strptime(x[3], '%Y-%m-%d'))

# Assign Payment_ID and Rental_ID sequentially after sorting
for i, payment in enumerate(rent_payments, start=1):
    rent_payments[i - 1] = (i, i, *payment[2:])  # Assign sequential IDs to Payment_ID and Rental_ID

# Insert data into Rent_Payments table
cursor.executemany("""
INSERT INTO Rent_Payments (Payment_ID, Rental_ID, Payment_Amount, Payment_Date, Payment_Method, Status, Notes, Tenant_ID, Property_ID)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rent_payments)


# Create the PropertyFeatures table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Property_Features (
    Property_ID INTEGER,
    Feature_ID INTEGER

)
""")

# Generate data for the junction table
property_feature_data = []

for property_id in range(1, 1001):
    # Randomly decide how many features this property will have (1 to 4 features per property)
    num_features = random.randint(1, 4)
    features = random.sample(range(1, 29), num_features)  # Choose unique features for this property

    # Append each (property_id, feature_id) pair to the data list
    for feature_id in features:
        property_feature_data.append((property_id, feature_id))

# Shuffle the data to mix rows before inserting (optional, for randomness)
random.shuffle(property_feature_data)

# Limit the data to 4000 rows
property_feature_data = property_feature_data[:4000]

# Insert data into the Property_Features table
cursor.executemany("""
INSERT INTO Property_Features (Property_ID, Feature_ID)
VALUES (?, ?)
""", property_feature_data)

# Export all data to Excel
tables = ["Properties", "Owners", "Agents", "MaintenanceRequests", "Features", "Sales", "Tenants", "Rentals", "Rent_Payments", "Property_Features"]
with pd.ExcelWriter(excel_file) as writer:
    for table in tables:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        df.to_excel(writer, sheet_name=table, index=False)

print(f"Database and Excel file created: {excel_file}")

# Finalize
conn.commit()
conn.close()
