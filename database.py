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
        Caption Text,
        Description Text,
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
    (RoomType, Caption, Description, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (
        "Standard Room",
        "A cozy and practical stay option with essential amenities for a comfortable visit.",
        "The Standard Room offers all the essentials in a well-designed space. Perfect for short stays, featuring a double bed, functional furniture, and a clean, modern bathroom.",
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
    (RoomType, Caption, Description, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (
        "Deluxe Room",
        "Stylish and spacious room designed for comfort with modern amenities and a relaxing view.",
        "Our Deluxe Room offers refined comfort and smart design. Featuring a queen-size bed, cozy seating corner, and contemporary interiors — ideal for solo travelers, couples, or business stays.",
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
    (RoomType, Caption, Description, RatePerNight, MaxOccupancy, BedType, SizeSqFt, Amenities, ImagePaths)
    VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
    """, (
        "Luxury Suite",
        "Elegantly appointed suite with panoramic mountain views and private balcony.",
        "Experience the peak of comfort in our Luxury Suite — expansive living area, plush king-sized bed, curated minibar, and a spa-like ensuite.",
        8500,
        2,
        "King Bed",
        700,
        "TV,Wi-Fi,Espresso machine,Bathtub,Room service",
        "luxury1.jpg,kinfbed1.jpg,hehe.jpg"
    ))

    rooms_data = [
        ('101', 1), ('102', 1), ('103', 1), # Three Standard Rooms
        ('201', 2), ('202', 2),             # Two Deluxe Rooms
        ('301', 3)                          # One Luxury Suite
    ]
    cursor.executemany("INSERT INTO Rooms (RoomNumber, RoomTypeID) VALUES (?, ?)", rooms_data)

    conn.commit()


def login(email,password):
    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Guests WHERE Email = ? AND Password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    conn = sqlite3.connect("hospital_management.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Guests WHERE Email = ? AND Password = ?", (email, password))
    userdetails = cursor.fetchone()
    conn.close()

    if user:
        return userdetails,1
    else:
        return userdetails,0
    
def signup(username,email,password,phone):
    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Guests (Name, Email,  Password, ContactNumber )VALUES (?,?,?,?);", (username,email,password,phone))
    conn.commit()
    conn.close()

def book_room(guest_id, room_type_id, check_in, check_out):
    """Handles the complete room booking logic."""
    conn = sqlite3.connect("hospital_management.db")
    cursor = conn.cursor()

    # Find available rooms of the requested type
    cursor.execute("""
        SELECT R.RoomID FROM Rooms R
        WHERE R.RoomTypeID = ? AND R.RoomID NOT IN (
            SELECT B.RoomID FROM Bookings B
            WHERE (B.CheckInDate < ? AND B.CheckOutDate > ?)
        )
    """, (room_type_id, check_out, check_in))
    
    available_room = cursor.fetchone()

    if not available_room:
        conn.close()
        return "❌ No rooms of this type available for the given dates."

    room_id_to_book = available_room[0]

    # Insert booking
    cursor.execute("""
        INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate)
        VALUES (?, ?, ?, ?)
    """, (guest_id, room_id_to_book, check_in, check_out))
    booking_id = cursor.lastrowid

    # Calculate total bill
    cursor.execute("SELECT RatePerNight FROM RoomTypes WHERE RoomTypeID = ?", (room_type_id,))
    rate = cursor.fetchone()[0]
    cursor.execute("SELECT julianday(?) - julianday(?)", (check_out, check_in))
    nights = int(cursor.fetchone()[0])
    total_amount = rate * nights

    # Insert billing record
    cursor.execute("""
        INSERT INTO Billings (BookingID, TotalAmount, PaymentStatus)
        VALUES (?, ?, 'Pending')
    """, (booking_id, total_amount))

    conn.commit()
    conn.close()
    return f"✅ Booking Confirmed (Room {room_id_to_book}, Total ₹{total_amount})"


if __name__ == "__main__":
    createtables()
    insertvalues()

