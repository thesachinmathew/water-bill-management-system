import mysql.connector
import datetime

# Establish database connection
con = mysql.connector.connect(host="localhost", user="root", passwd="041917", database="water", charset="utf8")

# Login function
def Login():
    print('WELCOME TO KERALA WATER AUTHORITY')
    user = input('Enter User ID: ')
    pas = input('Enter Password: ')
    if user == "sachin" and pas == "12345":
        print('Successfully Logged in!')
        MainMenu()
    else:
        print('Incorrect Password')
        Login()

# Add Consumer function
def AddConsumer():
    try:
        cur = con.cursor()
        cusid = int(input("Enter Customer ID: "))
        cusname = input("Enter customer name: ")
        address = input("Enter address: ")
        typ1 = int(input("Enter type (1 Household, 2 Agriculture, 3 Industrial): "))

        if typ1 == 1:
            custype = "Household"
        elif typ1 == 2:
            custype = "Agriculture"
        elif typ1 == 3:
            custype = "Industrial"
        
        query = "INSERT INTO customer (cusid, cusname, address, type) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (cusid, cusname, address, custype))
        con.commit()
        print("Customer details are added.")
    except Exception as e:
        con.rollback()
        print(f"Error occurred: {e}")
    finally:
        MainMenu()

# Update Consumer function
def UpdateConsumer():
    try:
        cur = con.cursor()
        cusid = int(input("Enter Customer ID to be modified: "))
        cusname = input("Enter change in customer name: ")
        address = input("Enter change in address: ")
        typ1 = int(input("Enter type (1 Household, 2 Agriculture, 3 Industrial): "))

        if typ1 == 1:
            custype = "Household"
        elif typ1 == 2:
            custype = "Agriculture"
        elif typ1 == 3:
            custype = "Industrial"

        query = "UPDATE customer SET cusname=%s, address=%s, type=%s WHERE cusid=%s"
        cur.execute(query, (cusname, address, custype, cusid))
        con.commit()
        print("Customer details are updated.")
    except Exception as e:
        con.rollback()
        print(f"Error occurred: {e}")
    finally:
        MainMenu()

# Search Consumer function
def SearchConsumer():
    try:
        cur = con.cursor()
        cusid = int(input("Enter Customer ID to be searched: "))
        query = "SELECT * FROM customer WHERE cusid=%s"
        cur.execute(query, (cusid,))
        record = cur.fetchall()

        print("\nCustomer ID\tCus Name\tCus Address\tCus Type")
        for i in record:
            print(i[0], "\t\t", i[1], "\t", i[2], "\t", i[3])
    except Exception as e:
        con.rollback()
        print(f"Error occurred: {e}")
    finally:
        MainMenu()

# Delete Consumer function
def DeleteConsumer():
    try:
        cur = con.cursor()
        cusid = int(input("Enter Customer ID to be removed: "))
        query = "DELETE FROM customer WHERE cusid=%s"
        cur.execute(query, (cusid,))
        con.commit()
        print("Customer details removed.")
    except Exception as e:
        con.rollback()
        print(f"Error occurred: {e}")
    finally:
        MainMenu()

# Calculate bill amount based on customer type and reading
def calculate_amount(cus_type, red):
    """Calculate the bill amount based on customer type and reading."""
    if cus_type == "Household":
        if red <= 50:
            return 0  # First 50 units free
        elif red <= 200:
            return (red - 50) * 20  # 20 per unit after 50 units
        else:
            return (150 * 20) + ((red - 200) * 30)  # 20 per unit for 50-200 units, 30 for above 200 units
    elif cus_type == "Agriculture":
        if red <= 200:
            return 0  # First 200 units free
        elif red <= 300:
            return (red - 200) * 7  # 7 per unit after 200 units
        else:
            return (100 * 7) + ((red - 300) * 12)  # 7 per unit for 200-300 units, 12 for above 300 units
    elif cus_type == "Industrial":
        if red <= 100:
            return red * 8  # 8 per unit
        elif red <= 200:
            return red * 15  # 15 per unit for 100-200 units
        else:
            return red * 20  # 20 per unit for above 200 units

# Generate Bill function
def GenerateBill():
    try:
        cur = con.cursor()
        billid = int(input("Enter Bill ID: "))
        cusid = int(input("Enter Customer ID: "))
        dp = input("Enter date of payment (yyyy-mm-dd): ")
        dl = input("Enter last date of payment (yyyy-mm-dd): ")

        # Current Date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        status = "Not paid"
        red = int(input("Enter reading (units used): "))

        query1 = "SELECT * FROM customer WHERE cusid=%s"
        cur.execute(query1, (cusid,))
        record = cur.fetchall()

        if not record:
            print(f"No customer found with ID {cusid}. Please check the ID.")
            return

        cusname, cusaddress, cus_type = record[0][1], record[0][2], record[0][3]
        
        amt = calculate_amount(cus_type, red)

        # Insert bill into the database
        query = "INSERT INTO bill (billid, cusid, amount, dp, dl, status, reading) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (billid, cusid, amt, dp, dl, status, red))
        con.commit()

        # Store bill details for later printing
        bill_details = {
            "billid": billid,
            "cusid": cusid,
            "cusname": cusname,
            "cusaddress": cusaddress,
            "cus_type": cus_type,
            "reading": red,
            "amount": amt,
            "dp": dp,
            "dl": dl,
            "status": status,
            "current_date": current_date
        }

        # Print the bill after generating
        PrintBill(bill_details)

    except mysql.connector.Error as err:
        con.rollback()
        print(f"Database error: {err}")
    except Exception as e:
        con.rollback()
        print(f"Error occurred: {e}")
    finally:
        MainMenu()

# Print Bill function
def PrintBill(bill_details):
    print("\n" + "="*60)
    print(f"       KERALA WATER AUTHORITY")
    print(f"         Government of Kerala")
    print("="*60)
    print(f" Bill ID: {bill_details['billid']}")
    print(f" Customer ID: {bill_details['cusid']}")
    print(f" Customer Name: {bill_details['cusname']}")
    print(f" Customer Address: {bill_details['cusaddress']}")
    print(f" Customer Type: {bill_details['cus_type']}")
    print("-" * 60)
    print(f" Reading: {bill_details['reading']} units")
    print(f" Amount: ₹{bill_details['amount']}")
    print("-" * 60)
    print(f" Date of Payment: {bill_details['dp']}")
    print(f" Last Date of Payment: {bill_details['dl']}")
    print(f" Status: {bill_details['status']}")
    print("-" * 60)
    print(f" Issued on: {bill_details['current_date']}")
    print("="*60)

    # Go back to main menu after printing the bill
    MainMenu()

# Check Bill function
def CheckBill():
    try:
        cur = con.cursor()
        billid = int(input("Enter Bill ID: "))
        
        # Fetching bill details along with customer name, amount, property type, consumed units, and date of payment
        query = """
        SELECT b.billid, b.cusid, b.amount, b.status, b.reading, b.dp, c.cusname, c.type
        FROM bill b
        JOIN customer c ON b.cusid = c.cusid
        WHERE b.billid = %s
        """
        cur.execute(query, (billid,))
        record = cur.fetchall()

        # If no record found
        if not record:
            print("No bill found with the provided Bill ID.")
            return
        
        # Extracting details from the record
        bill_details = record[0]
        billid, cusid, amount, status, reading, dp, cusname, cus_type = bill_details
        
        # Current date for the bill
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Printing the bill in a structured format
        print("\n" + "="*60)
        print(f"{'KERALA WATER AUTHORITY':^60}")
        print(f"{'Issued by Govt. of Kerala':^60}")
        print("="*60)
        print(f"Bill ID: {billid}")
        print(f"Customer ID: {cusid}")
        print(f"Customer Name: {cusname}")
        print(f"Customer Type: {cus_type}")
        print("-" * 60)
        print(f"Consumed Units: {reading} units")
        print(f"Amount: ₹{amount}")
        print("-" * 60)
        print(f"Date of Payment: {dp}")
        print(f"Status: {status}")
        print("-" * 60)
        print(f"Issued on: {current_date}")
        print("="*60)
        
    except Exception as e:
        con.rollback()
        print(f"Error occurred: {e}")
    finally:
        MainMenu()

# Main Menu function
def MainMenu():
    print("\nMain Menu:")
    print("1. Add Consumer")
    print("2. Update Consumer")
    print("3. Search Consumer")
    print("4. Delete Consumer")
    print("5. Generate Bill")
    print("6. Check Bill")
    print("7. Pay Bill")
    print("8. Exit")
    choice = int(input("Enter choice: "))

    if choice == 1:
        AddConsumer()
    elif choice == 2:
        UpdateConsumer()
    elif choice == 3:
        SearchConsumer()
    elif choice == 4:
        DeleteConsumer()
    elif choice == 5:
        GenerateBill()
    elif choice == 6:
        CheckBill()
    elif choice == 7:
        BillPay()
    elif choice == 8:
        print("Thank you for using Kerala Water Authority!")
        exit()
    else:
        print("Invalid choice. Please try again.")
        MainMenu()
# Start the login process
Login()
