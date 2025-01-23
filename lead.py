import sqlite3
import streamlit as st


# Initialize the database
def init_db():
    conn = sqlite3.connect("inquiries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telecaller_name TEXT NOT NULL,
            parent_name TEXT NOT NULL,
            student_name TEXT NOT NULL,
            student_class TEXT NOT NULL,
            lang_medium TEXT NOT NULL,
            admission_fees TEXT NOT NULL,
            address TEXT NOT NULL,
            branch TEXT NOT NULL,
            mobile_number TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Function to add sample entries with Indian names
def add_sample_entries():
    sample_data = [
        ("Rajesh Kumar", "Vijay Kumar", "Aarti Kumar", "10th", "Hindi", "25000", "123 Lajpat Nagar, New Delhi",
         "Branch A", "9876543210"),
        ("Sushma Verma", "Anil Verma", "Ravi Verma", "12th", "English", "30000", "456 MG Road, Mumbai", "Branch B",
         "8765432109"),
        (
        "Pradeep Sharma", "Sunita Sharma", "Neha Sharma", "8th", "Marathi", "20000", "789 Baner Road, Pune", "Branch A",
        "7654321098"),
        ("Seema Gupta", "Raghav Gupta", "Tanvi Gupta", "11th", "Hindi", "28000", "101 Shankar Colony, Bangalore",
         "Branch C", "6543210987"),
        ("Vikram Singh", "Manju Singh", "Krishna Singh", "9th", "English", "22000", "222 Kacheri Road, Lucknow",
         "Branch B", "5432109876")
    ]

    conn = sqlite3.connect("inquiries.db")
    cursor = conn.cursor()

    for entry in sample_data:
        try:
            cursor.execute("""
                INSERT INTO inquiries (telecaller_name, parent_name, student_name, student_class, 
                lang_medium, admission_fees, address, branch, mobile_number) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, entry)
        except sqlite3.IntegrityError:
            pass  # Skip if the mobile number already exists

    conn.commit()
    conn.close()


# Call function to initialize database and add sample entries
init_db()
add_sample_entries()

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(#ff7eb3, #ff758f);
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .header {
            background-color: #2196F3;
            padding: 10px;
            border-radius: 5px;
            color: white;
            text-align: center;
        }
        .container {
            margin: 20px;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="header"><h1>Training Institute Lead Record Keeper</h1></div>', unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Add Record", "View Records"])

# Add Record Section
if menu == "Add Record":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Add a New Inquiry Record")

    telecaller_name = st.text_input("Telecaller Name")
    parent_name = st.text_input("Parent Name")
    student_name = st.text_input("Student Name")
    student_class = st.text_input("Class")
    lang_medium = st.selectbox("Language Medium", ["English", "Hindi", "Marathi"])
    admission_fees = st.text_input("Admission Fees")
    address = st.text_area("Address")
    branch = st.selectbox("Branch", ["Branch A", "Branch B", "Branch C"])
    mobile_number = st.text_input("Mobile Number")

    if st.button("Add Record"):
        try:
            conn = sqlite3.connect("inquiries.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inquiries (telecaller_name, parent_name, student_name, student_class, 
                lang_medium, admission_fees, address, branch, mobile_number) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            telecaller_name, parent_name, student_name, student_class, lang_medium, admission_fees, address, branch,
            mobile_number))
            conn.commit()
            conn.close()
            st.success("Record added successfully!")
        except sqlite3.IntegrityError:
            st.error("A record with this mobile number already exists.")
    st.markdown('</div>', unsafe_allow_html=True)

# View Records Section
elif menu == "View Records":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Search and View Records")

    search_by = st.radio("Search by", ["All Records", "Mobile Number", "Telecaller Name"])

    conn = sqlite3.connect("inquiries.db")
    cursor = conn.cursor()

    if search_by == "All Records":
        cursor.execute("SELECT * FROM inquiries")
    elif search_by == "Mobile Number":
        mobile_search = st.text_input("Enter Mobile Number")
        cursor.execute("SELECT * FROM inquiries WHERE mobile_number = ?", (mobile_search,))
    elif search_by == "Telecaller Name":
        telecaller_search = st.text_input("Enter Telecaller Name")
        cursor.execute("SELECT * FROM inquiries WHERE telecaller_name = ?", (telecaller_search,))

    records = cursor.fetchall()
    conn.close()

    if records:
        st.table(records)
    else:
        st.warning("No records found.")
    st.markdown('</div>', unsafe_allow_html=True)
