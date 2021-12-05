import datetime
import time

from sales_list import SalesList
from sellers_list import SellersList


MENU = '''
------- MENU -------
1 - List all sales
2 - Insert a new sale
3 - Edit a sale date
4 - Delete a sale
5 - Log off
'''


# -----------------------------------------------------------------

def get_int_input(input_message):
    while True:
        try:
            input_value = int(input(input_message))
            return input_value
        except ValueError:
            print("\n--- Please inform a number! ---\n")


def get_date(input_message, format):
    while True:
        try:
            date = datetime.datetime.strptime(input(input_message), format)
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
        print(f"Sale Value: {sale['saleValue']}\n")


def get_sellers_rank(sales, sellers):
    dict_result = {}  # KEY -> sellerId, value -> amount sold}

    for sale in sales:
        sale_seller = sale['seller']['sellerId']

        if sale_seller in dict_result.keys():
            dict_result[sale_seller] += sale['saleValue']
        else:
            dict_result[sale_seller] = sale['saleValue']

    for seller in sellers:
        if seller['sellerId'] not in dict_result.keys():
            dict_result[seller['sellerId']] = 0

    dict_result = dict(sorted(dict_result.items(), key=lambda item: item[1], reverse=True))
    return dict_result.keys()


def list_sales_by_seller_rank(sales_obj: SalesList, sellers):
    print("---- SALES LIST ----")
    if not sales_obj.is_empty():
        for seller in get_sellers_rank(sales_obj.get_sales(), sellers):
            sellers_sales = sales_obj.get_sales_by_seller_id(seller)
            list_sales(sellers_sales)
    else:
        print("No sale registered!")


# ------------------------------------------------------------------


def home(logged_user, sellers_list: SellersList):
    sales_list = SalesList()
    sellers = sellers_list.get_sellers()

    while True:
        print(MENU)
        opt = get_int_input('Choose an option: ')
        print('')
        print('------------------------------')
        if opt == 1:
            list_sales_by_seller_rank(sales_list, sellers)
        elif opt == 2:
            print("NEW SALE: ")

            customer_name = input("Customer Name: ")

            date = get_date("Date (mm-dd-yyyy):", '%m-%d-%Y')

            item_name = input("Item Name: ")

            while True:
                try:
                    value = float(input("Sale Value: "))
                    break
                except ValueError:
                    print("\n--- Insert a valid value! ---\n")

            sales_list.insert_new_sale(logged_user, customer_name, date, item_name, value)
            list_sales_by_seller_rank(sales_list, sellers)
        elif opt == 3:
            logged_user_sales = sales_list.get_sales_by_seller_id(logged_user['sellerId'])
            if len(logged_user_sales) == 0:
                print("-- You don't have any sale registered! --")
            else:
                print("EDIT SALE DATE:")
                print("*To cancel, digit -1 in the sale number field!\n")

                print("Your Sales:")
                list_sales(logged_user_sales)

                while True:
                    sale_id = int(input("Insert the number of the sale you want to edit: "))
                    if sale_id == -1:
                        print("Edit operation was canceled!")
                        break
                    selected_sale = sales_list.get_sale_by_id(sale_id)
                    if selected_sale and selected_sale["seller"]['sellerId'] == logged_user['sellerId']:
                        break
                    else:
                        print("\n--- Inform a valid sale! ---\n")

                if sale_id != -1:
                    new_date = get_date("New date (mm-dd-yyyy):", '%m-%d-%Y')
                    confirmed = confirm_operation('edit')
                    if confirmed:
                        sales_list.edit_sale_date(sale_id, new_date)
                    else:
                        print("Edit operation was canceled!")

        elif opt == 4:
            logged_user_sales = sales_list.get_sales_by_seller_id(logged_user['sellerId'])
            if len(logged_user_sales) == 0:
                print("-- You don't have any sale registered! --")
            else:
                print("DELETE SALE:")
                print("*To cancel, digit -1 in the sale number field!\n")

                print("Your Sales:")
                list_sales(logged_user_sales)

                while True:
                    sale_id = int(input("Insert the number of the sale you want to delete: "))
                    if sale_id == -1:
                        print("Delete operation was canceled!")
                        break

                    selected_sale = sales_list.get_sale_by_id(sale_id)
                    if selected_sale and selected_sale["seller"]['sellerId'] == logged_user['sellerId']:
                        confirmed = confirm_operation('delete')
                        if confirmed:
                            sales_list.delete_sale(sale_id)
                            print("\n--- The sale was deleted successfully! ---\n")
                        else:
                            print("\n--- Delete operation was canceled! ---\n")
                        break
                    else:
                        print("\n--- Sale not found! Please inform a valid sale! ---\n")

        elif opt == 5:
            break

        else:
            print("\n--- Choose a valid option! ---\n")

        input("PRESS ANY BUTTON TO RETURN TO MENU")


def login(sellers_list: SellersList):
    print("----- LOGIN -----\n")

    while True:
        username = input("Username: ")
        passw = input("Password: ")
        print("Loggin in...")
        user = sellers_list.verify_login(username, passw)
        time.sleep(1.5)
        if not user:
            print("\n--- Invalid login! ---\n")
        else:
            print("Logged in sucessfully!")
            time.sleep(0.5)
            return user


if __name__ == "__main__":
    sellersList = SellersList()

    print("************ SALES MANAGER ***************")
    while True:
        print("1 - LOGIN")
        print("2 - EXIT")
        opt = get_int_input('Choose an option: ')
        if opt == 1:
            user = login(sellersList)
            home(user, sellersList)
        elif opt == 2:
            break
        else:
            print("\n--- Please select a valid option! ---\n")


