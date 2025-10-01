import sqlite3

def createtables():
    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE Guests (
        GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT UNIQUE,
        Password TEXT NOT NULL,
        ContactNumber TEXT
    );""")

    cursor.execute("""
    CREATE TABLE RoomTypes (
        RoomTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
        RoomType TEXT NOT NULL,
        RatePerNight REAL NOT NULL,
        MaxOccupancy INTEGER,
        BedType TEXT,
        SizeSqFt INTEGER,
        Amenities TEXT,       
        ImagePaths TEXT       
    );
    """)

    cursor.execute("""CREATE TABLE Rooms (
        RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
        RoomNumber TEXT UNIQUE NOT NULL,
        RoomTypeID INTEGER,
        RoomStatus TEXT DEFAULT 'Available',
        FOREIGN KEY (RoomTypeID) REFERENCES RoomTypes(RoomTypeID) ON DELETE CASCADE
    );""")

    cursor.execute("""CREATE TABLE Bookings (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
        GuestID INTEGER,
        RoomID INTEGER,
        CheckInDate DATE NOT NULL,
        CheckOutDate DATE NOT NULL,
        BookingStatus TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (GuestID) REFERENCES Guests(GuestID) ON DELETE CASCADE,
        FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE SET NULL
    );""")


    cursor.execute("""CREATE TABLE Services (
        ServiceID INTEGER PRIMARY KEY AUTOINCREMENT,
        ServiceType TEXT NOT NULL,
        ServiceDetails TEXT,
        ServiceCost REAL NOT NULL
    );""")


    cursor.execute("""CREATE TABLE Billings (
        BillingID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookingID INTEGER,
        TotalAmount REAL NOT NULL,
        AmountPaid REAL DEFAULT 0,
        PaymentStatus TEXT CHECK(PaymentStatus IN ('Paid', 'Pending')) DEFAULT 'Pending',
        FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID) ON DELETE CASCADE
    );""")

    conn.commit()
    conn.close()

def insertvalues():

    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()
    # Standard Room
    cursor.execute("""
    INSERT INTO RoomTypes 
    (RoomType, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Standard Room",
        3500,                        # example price
        2,
        "Double Bed",
        300,
        "TV,Wi-Fi,Tea kettle,Bath essentials",
        "new1.jpg,new2.jpg,newbath.jpg"
    ))

    # Deluxe Room
    cursor.execute("""
    INSERT INTO RoomTypes 
    (RoomType, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Deluxe Room",
        5500,
        2,
        "Queen Bed",
        430,
        "TV,Wi-Fi,Tea/Coffee maker,Work desk,Laundry service",
        "deluxer.jpg,deluxue2.jpg,deluxew.jpeg"
    ))

    # Luxury Suite
    cursor.execute("""
    INSERT INTO RoomTypes 
    (RoomType, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "Luxury Suite",
        8500,
        2,
        "King Bed",
        700,
        "TV,Wi-Fi,Espresso machine,Bathtub,Room service",
        "luxury1.jpg,kinfbed1.jpg,hehe.jpg"
    ))

    conn.commit()


def login(email,password):
    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Guests WHERE Email = ? AND Password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return 1
    else:
        return 0
    
def signup(username,email,password,phone):
    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Guests (Name, Email,  Password, ContactNumber )VALUES (?,?,?,?);", (username,email,password,phone))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    createtables()
    insertvalues()

