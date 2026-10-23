#!/usr/bin/env python3
from config import clean_text
from mailer import send_email


def send_order_email():
    safe_table = clean_text(table_no, 32)
    safe_items = clean_text(items, 500)
    result = send_email(
        subject=f"Table {safe_table} order",
        body=f"Table Number {safe_table} ordered {safe_items} .",
    )
    if result == "sent":
        return True
    if result == "skipped":
        print(
            "Email is not configured. Set SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL in .env."
        )
    else:
        print("Could not send email. Check the SMTP settings in .env.")
    return False


print("""

████████╗██╗░░██╗███████╗  ░█████╗░██╗░░░░░██╗
╚══██╔══╝██║░░██║██╔════╝  ██╔══██╗██║░░░░░██║
░░░██║░░░███████║█████╗░░  ██║░░╚═╝██║░░░░░██║
░░░██║░░░██╔══██║██╔══╝░░  ██║░░██╗██║░░░░░██║
░░░██║░░░██║░░██║███████╗  ╚█████╔╝███████╗██║
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ░╚════╝░╚══════╝╚═╝

██████╗░███████╗░██████╗████████╗░█████╗░██╗░░░██╗██████╗░░█████╗░███╗░░██╗████████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██║░░░██║██╔══██╗██╔══██╗████╗░██║╚══██╔══╝
██████╔╝█████╗░░╚█████╗░░░░██║░░░███████║██║░░░██║██████╔╝███████║██╔██╗██║░░░██║░░░
██╔══██╗██╔══╝░░░╚═══██╗░░░██║░░░██╔══██║██║░░░██║██╔══██╗██╔══██║██║╚████║░░░██║░░░
██║░░██║███████╗██████╔╝░░░██║░░░██║░░██║╚██████╔╝██║░░██║██║░░██║██║░╚███║░░░██║░░░
╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░
""")
try:
    table_no = input("Table no >")
except EOFError:
    raise SystemExit(0)

hitems = ""

items = ""
hitems = items
print("hi")
run = 1
while run == 1:
    print("""
    welcome choose your dish
    (1)burger
    (2)veg biryani
    (3)french fries
    (4)falooda
    (5)royal falooda
    (6)fruit salad
    (7)vegetable salad
    (8)fish fry
    (9)chicken fry
    (10)chicken biriyani
    (11)veg cutlet
    (12)paneer butter masala
    (13)veg meals
    (14)naan 
    (15)butter naan
    (16)dosai
    (17)ghee dosai
    (18)masal dosai
    (00)send
    (99)exit

    """)
    
    try:
        option = int(input(">"))
    except ValueError:
        print("Please enter a number from the menu.")
        continue
    except EOFError:
        raise SystemExit(0)
    if option == 99:
        raise SystemExit(0)
    if option == 1:
        print("burger coming up")
        burger_no = str(input("How Many: "))
        items = (hitems+","+"burger "+burger_no)
        print(items)
        hitems = items
    if option == 2:
        print("veg biriani coming up")
        veg_bir_no = str(input("How Many: "))
        items = (hitems+","+"veg biriyani "+veg_bir_no)
        print(items)
        hitems = items
    if option == 3:
        print("frenchfries coming up")
        french_fries_no = str(input("How Many: "))
        items = (hitems+","+"french fries "+french_fries_no)
        print(items)
        hitems = items
    if option == 4:
        print("falooda coming up")
        fal_no = str(input("How Many: "))
        items = (hitems+","+"falooda "+fal_no)
        print(items)
        hitems = items
    if option == 5:
        print("royal falooda coming up")
        ryl_fal_no = str(input("How Many: "))
        items = (hitems+","+"royal falooda "+ryl_fal_no)
        print(items)
        hitems = items
    if option == 6:
        print("fruit salad coming up")
        frt_sal_no = str(input("How Many: "))
        items = (hitems+","+"fruit salad "+frt_sal_no)
        print(items)
        hitems = items
    if option == 7:
        print("vegetable salad coming up")
        veg_sal_no = str(input("How Many: "))
        items = (hitems+","+"vegetable salad "+veg_sal_no)
        print(items)
        hitems = items
    if option == 8:
        print("fish fry coming up")
        fis_fry_no = str(input("How Many: "))
        items = (hitems+","+"fish fry "+fis_fry_no)
        print(items)
        hitems = items
    if option == 9:
        print("chicken fry coming up")
        chic_fry_no = str(input("How Many: "))
        items = (hitems+","+"chicken fry "+chic_fry_no)
        print(items)
        hitems = items
    if option == 10:
        print("chicken biriyani coming up")
        chic_bir_no = str(input("How Many: "))
        items = (hitems+","+"chicken biriyani "+chic_bir_no)
        print(items)
        hitems = items
    if option == 11:
        print("veg cutlet coming up")
        veg_cut_no = str(input("How Many: "))
        items = (hitems+","+"veg cutlet "+veg_cut_no)
        print(items)
        hitems = items
    if option == 12:
        print("paneer butter masala coming up")
        pan_but_mas_no = str(input("How Many: "))
        items = (hitems+","+"paneer butter masala "+pan_but_mas_no)
        print(items)
        hitems = items
    if option == 13:
        print("veg meals coming up")
        veg_meal_no = str(input("How Many: "))
        items = (hitems+","+"veg meals "+veg_meal_no)
        print(items)
        hitems = items
    if option == 14:
        print("naan coming up")
        nan_no = str(input("How Many: "))
        items = (hitems+","+"naan "+nan_no)
        print(items)
        hitems = items
    if option == 15:
        print("butter naan coming up")
        but_nan_no = str(input("How Many: "))
        items = (hitems+","+"butter naan "+but_nan_no)
        print(items)
        hitems = items
    if option == 16:
        print("dosai coming up")
        dosai_no = str(input("How Many: "))
        items = (hitems+","+"dosai "+dosai_no)
        print(items)
        hitems = items
    if option == 17:
        print("ghee dosai coming up")
        ghee_dosai_no = str(input("How Many: "))
        items = (hitems+","+"ghee dosai "+ghee_dosai_no)
        print(items)
        hitems = items
    if option == 18:
        print("masala dosai coming up")
        mas_dosai_no = str(input("How Many: "))
        items = (hitems+","+"masala dosai "+mas_dosai_no)
        print(items)
        hitems = items
    
    if option == 0:
        if send_order_email():
            print("Email sent.")
            print("Thank you ,closing this app")
            raise SystemExit(0) 