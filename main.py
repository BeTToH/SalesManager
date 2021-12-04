import datetime
from sales_list import SalesList

SELLERS = ['Andre', 'Júlia', 'Carlos', 'Leo', 'Maria']

MENU = '''
------- MENU -------
1 - List all sales
2 - Insert a new sale
3 - Edit a sale date
4 - Delete a sale
6 - EXIT
'''


# -----------------------------------------------------------------

def print_sellers():
    count = 1
    print("-- SELLERS --")
    for seller in SELLERS:
        print(f"{count}. {seller}")
        count += 1


def get_date(input_message, format):
    while True:
        try:
            date = datetime.datetime.strptime(input(input_message), format)
            break
        except ValueError:
            print("Insert a valid date!\n"
                  "Correct format: mm-dd-yyyy, e.g. 01-01-2000.")
    return date


def list_sales(sales):
    for sale in sales:
        print(f"SALE {sale['saleId']}")
        print(f"Seller Name: {sale['sellerName']}")
        print(f"Customer Name: {sale['customerName']}")
        print(f"Date Of Sale: {sale['date'].strftime('%m-%m-%Y')}")
        print(f"Sale Item Name: {sale['itemName']}")
        print(f"Sale Value: {sale['saleValue']}\n")


def get_sellers_rank(sales):
    dict_result = {}  # KEY -> seller, value -> amount sold}

    for sale in sales:
        sale_seller = sale['sellerName']

        if sale_seller in dict_result.keys():
            dict_result[sale_seller] += sale['saleValue']
        else:
            dict_result[sale_seller] = sale['saleValue']

    for seller in SELLERS:
        if seller not in dict_result.keys():
            dict_result[seller] = 0

    dict_result = dict(sorted(dict_result.items(), key=lambda item: item[1], reverse=True))
    return dict_result.keys()


def list_sales_by_seller_rank(sales_obj: SalesList):
    print("---- SALES LIST ----")
    if not sales_obj.is_empty():
        for seller in get_sellers_rank(sales_obj.get_sales()):
            sellers_sales = sales.get_sales_by_seller(seller)
            list_sales(sellers_sales)
    else:
        print("No sale registered!")


# ------------------------------------------------------------------
print("************ SALES MANAGER ***************")

sales = SalesList()
while True:
    print(MENU)
    opt = int(input('Choose an option: '))
    print('')
    print('------------------------------')
    if opt == 1:
        list_sales_by_seller_rank(sales)
    elif opt == 2:
        print("NEW SALE: ")
        while True:
            try:
                print("Choose a seller:")
                print("Options:")
                print_sellers()
                seller_index = int(input("Inform the option number: ")) - 1
                seller_name = SELLERS[seller_index]
                break
            except IndexError:
                print("\n--- Inform a valid option! ---\n")

        customer_name = input("Customer Name: ")

        date = get_date("Date (mm-dd-yyyy):", '%m-%d-%Y')

        item_name = input("Item Name: ")

        while True:
            try:
                value = float(input("Sale Value: "))
                break
            except ValueError:
                print("\n--- Insert a valid value! ---\n")

        sales.insert_new_sale(seller_name, customer_name, date, item_name, value)
        list_sales_by_seller_rank(sales)
    elif opt == 3:
        if sales.is_empty():
            print("No sale registered!")
        else:
            print("EDIT SALE DATE:\n")
            list_sales_by_seller_rank(sales)

            while True:
                sale_id = int(input("Insert the number of the sale you want to edit: "))
                if sales.get_sale_by_id(sale_id):
                    break
                else:
                    print("\n--- Inform a valid sale! ---\n")

            new_date = get_date("New date (mm-dd-yyyy):", '%m-%d-%Y')
            sales.edit_sale_date(sale_id, new_date)
    elif opt == 4:
        if sales.is_empty():
            print("No sale registered!")
        else:
            list_sales_by_seller_rank(sales)
            while True:
                sale_id = int(input("Insert the number of the sale you want to delete: "))
                if sales.delete_sale(sale_id):
                    print("The sale was deleted successfully!")
                    break
                else:
                    print("\n--- Sale not found! Please inform a valid sale! ---\n")
            list_sales_by_seller_rank(sales)
    elif opt == 6:
        break

    input("PRESS ANY BUTTON TO RETURN TO MENU")
