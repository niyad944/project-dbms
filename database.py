import sqlite3


conn = sqlite3.connect("hospital_management.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Guests (
    GuestID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    ContactNumber TEXT,
    Email TEXT UNIQUE,
    Address TEXT
);""")

cursor.execute("""CREATE TABLE RoomTypes (
    RoomTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomType TEXT,
    RatePerNight REAL NOT NULL,
    MaxOccupancy INTEGER,
    BedType TEXT,
    SizeSqFt INTEGER,
    Amenities TEXT
    Icon Path TEXT
);""")

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



