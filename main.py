import datetime
import time
from sales_list import SalesList
from users_list import UsersList


# ------------------------------------------------------------------
# Aux Functions

def get_int_input(input_message):
    while True:
        try:
            input_value = int(input(input_message))
            return input_value
        except ValueError:
            print("\n--- Please inform a number! ---\n")


def get_date_input(input_message, date_format):
    while True:
        try:
            date = datetime.datetime.strptime(input(input_message), date_format)
            break
        except ValueError:
            print("\n--- Insert a valid date! Correct format: mm-dd-yyyy, e.g. 01-01-2000. ---\n")
    return date


def confirm_operation(operation_name):
    while True:
        confirm = input(f"Confirm {operation_name}? (y for YES or n for NO) ")
        if confirm == 'y' or confirm == 'Y':
            return True
        elif confirm == 'n' or confirm == 'N':
            return False
        else:
            print("\n--- Please digit y for YES or n for NO! ---\n")


def print_sellers(sellers):
    count = 1
    print("-- SELLERS --")
    for seller in sellers:
        print(f"{count}. {seller['username']}")
        count += 1


def list_sales(sales):
    for sale in sales:
        print(f"SALE {sale['saleId']}")
        print(f"Seller Name: {sale['seller']['username']}")
        print(f"Customer Name: {sale['customerName']}")
        print(f"Date Of Sale: {sale['date'].strftime('%m-%m-%Y')}")
        print(f"Sale Item Name: {sale['itemName']}")
        print(f"Sale Value: {sale['saleValue']:.2f}\n")


def get_sellers_rank(sales, sellers):
    dict_result = {}  # KEY -> userId, value -> amount sold}

    for sale in sales:
        sale_seller = sale['seller']['userId']

        if sale_seller in dict_result.keys():
            dict_result[sale_seller] += sale['saleValue']
        else:
            dict_result[sale_seller] = sale['saleValue']

    for seller in sellers:
        if seller['userId'] not in dict_result.keys():
            dict_result[seller['userId']] = 0

    dict_result = dict(sorted(dict_result.items(), key=lambda item: item[1], reverse=True))
    return dict_result.keys()


# ------------------------------------------------------------------
# Options

def list_sales_by_seller_rank(sales_obj: SalesList, sellers):
    print("---- SALES LIST ----")
    if not sales_obj.is_empty():
        for seller in get_sellers_rank(sales_obj.get_sales(), sellers):
            sellers_sales = sales_obj.get_sales_by_user_id(seller)
            list_sales(sellers_sales)
    else:
        print("-- No sale registered! --")


def insert_new_sale(logged_user, sales_list, sellers):
    print("---- NEW SALE ----")

    if logged_user['userType'] == 'admin':
        while True:
            try:
                print("Choose a seller:")
                print_sellers(sellers)
                seller_index = int(input("Inform the option number: ")) - 1
                seller = sellers[seller_index]
                break
            except IndexError:
                print("\n--- Inform a valid option! ---\n")
    else:
        seller = logged_user

    customer_name = input("Customer Name: ")

    date = get_date_input("Date (mm-dd-yyyy):", '%m-%d-%Y')

    item_name = input("Item Name: ")

    while True:
        try:
            value = float(input("Sale Value: "))
            break
        except ValueError:
            print("\n--- Insert a valid value! ---\n")

    sales_list.insert_new_sale(seller, customer_name, date, item_name, value)
    list_sales_by_seller_rank(sales_list, sellers)


def edit_sale_date(logged_user, sales_list):
    logged_user_sales = []
    if logged_user['userType'] == 'seller':
        logged_user_sales = sales_list.get_sales_by_user_id(logged_user['userId'])
    elif logged_user['userType'] == 'admin':
        logged_user_sales = sales_list.get_sales()

    if len(logged_user_sales) == 0:
        print("-- You don't have any sale registered! --")
    else:
        print("---- EDIT SALE DATE ----")
        print("*To cancel, digit -1!\n")

        if logged_user['userType'] == 'seller':
            print("Your Sales:")
        elif logged_user['userType'] == 'admin':
            print("All Sales:")

        list_sales(logged_user_sales)

        while True:
            sale_id = int(input("Insert the number of the sale you want to edit: "))
            if sale_id == -1:
                print("\n--- Edit operation was canceled! ---\n")
                break
            selected_sale = sales_list.get_sale_by_id(sale_id)
            if selected_sale and \
                    (selected_sale["seller"]['userId'] == logged_user['userId'] or logged_user['userType'] == 'admin'):
                break
            else:
                print("\n--- Inform a valid sale! ---\n")

        if sale_id != -1:
            new_date = get_date_input("New date (mm-dd-yyyy):", '%m-%d-%Y')
            confirmed = confirm_operation('edit')
            if confirmed:
                sales_list.edit_sale_date(sale_id, new_date)
            else:
                print("\n--- Edit operation was canceled! ---\n")


def delete_sale(logged_user, sales_list):
    logged_user_sales = []
    if logged_user['userType'] == 'seller':
        logged_user_sales = sales_list.get_sales_by_user_id(logged_user['userId'])
    elif logged_user['userType'] == 'admin':
        logged_user_sales = sales_list.get_sales()

    if len(logged_user_sales) == 0:
        print("-- You don't have any sale registered! --")
    else:
        print("---- DELETE SALE ----")
        print("*To cancel, digit -1!\n")

        if logged_user['userType'] == 'seller':
            print("Your Sales:")
        elif logged_user['userType'] == 'admin':
            print("All Sales:")

        list_sales(logged_user_sales)

        while True:
            sale_id = int(input("Insert the number of the sale you want to delete: "))
            if sale_id == -1:
                print("\n--- Delete operation was canceled! ---\n")
                break

            selected_sale = sales_list.get_sale_by_id(sale_id)
            if selected_sale and \
                    (selected_sale["seller"]['userId'] == logged_user['userId'] or logged_user['userType'] == 'admin'):
                confirmed = confirm_operation('delete')
                if confirmed:
                    sales_list.delete_sale(sale_id)
                    print("\n--- The sale was deleted successfully! ---\n")
                else:
                    print("\n--- Delete operation was canceled! ---\n")
                break
            else:
                print("\n--- Sale not found! Please inform a valid sale! ---\n")


# ------------------------------------------------------------------
# INTERFACE

HOME_MENU = '''
------- MENU -------
1 - List all sales
2 - Insert a new sale
3 - Edit a sale date
4 - Delete a sale
5 - Log off
'''


def home(logged_user, users_list: UsersList):
    sales_list = SalesList()
    sellers = users_list.get_users_by_user_type('seller')

    while True:
        print(HOME_MENU)
        opt = get_int_input('Choose an option: ')
        print('')
        if opt == 1:
            list_sales_by_seller_rank(sales_list, sellers)

        elif opt == 2:
            insert_new_sale(logged_user, sales_list, sellers)

        elif opt == 3:
            edit_sale_date(logged_user, sales_list)

        elif opt == 4:
            delete_sale(logged_user, sales_list)

        elif opt == 5:
            print("Loggin off...")
            time.sleep(0.5)
            break

        else:
            print("\n--- Choose a valid option! ---\n")

        input("PRESS ANY BUTTON TO RETURN TO MENU")


def login(users_list: UsersList):
    print("---------- LOGIN ----------")
    print("*To exit, digit -1 in the username field\n")

    while True:
        username = input("Username: ")
        if username == '-1':
            return False

        passw = input("Password: ")
        print("Loggin in...")
        user = users_list.verify_login(username, passw)
        time.sleep(1.2)
        if not user:
            print("\n--- Invalid login! ---\n")
        else:
            print("\n--- Logged in sucessfully! ---\n")
            time.sleep(0.5)
            return user


if __name__ == "__main__":
    usersList = UsersList()

    while True:
        print("************ SALES MANAGER ***************\n")

        user = login(usersList)
        if user:
            home(user, usersList)
        else:
            break
