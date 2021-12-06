"""
    SALE: {saleId, sellerName, customerName, date, itemName, saleValue}
"""
import datetime


class SalesList:
    ID_COUNT = 4
    SALES = [{'saleId': 1, 'seller': {'userId': 1, 'username': 'Andre', 'password': 'password', 'userType': 'seller'},
              'customerName': 'Renanf', 'date': datetime.datetime.today(), 'itemName': 'Ball', 'saleValue': 100},
             {'saleId': 2, 'seller': {'userId': 1, 'username': 'Andre', 'password': 'password', 'userType': 'seller'},
              'customerName': 'Renanf', 'date': datetime.datetime.today(), 'itemName': 'Ball', 'saleValue': 100},
             {'saleId': 3, 'seller': {'userId': 4, 'username': 'Monica', 'password': 'password', 'userType': 'seller'},
              'customerName': 'Renanf', 'date': datetime.datetime.today(), 'itemName': 'Ball', 'saleValue': 100}]

    # FUNCTIONS
    def get_sales(self):
        return self.SALES.copy()

    def get_sales_by_user_id(self, seller_id):
        return [sale for sale in self.SALES if sale['seller']['userId'] == seller_id]

    def get_sale_by_id(self, sale_id):
        for i in range(len(self.SALES)):
            if self.SALES[i]['saleId'] == sale_id:
                return self.SALES[i]

        return False

    def insert_new_sale(self, seller, customer_name, date, item_name, sale_value):
        new_sale = {'saleId': self.ID_COUNT, 'seller': seller, 'customerName': customer_name,
                    'date': date, 'itemName': item_name, 'saleValue': sale_value}

        self.SALES.append(new_sale)
        self.ID_COUNT += 1

    def edit_sale(self, sale_id, seller, customer_name, date, item_name, sale_value):
        for i in range(len(self.SALES)):
            if self.SALES[i]['saleId'] == sale_id:
                self.SALES[i] = {'saleId': sale_id, 'seller': seller, 'customerName': customer_name,
                                 'date': date, 'itemName': item_name, 'saleValue': sale_value}
                break

    def delete_sale(self, sale_id):
        for i in range(len(self.SALES)):
            if self.SALES[i]['saleId'] == sale_id:
                del self.SALES[i]
                return True

        return False

    def is_empty(self):
        return len(self.SALES) == 0
