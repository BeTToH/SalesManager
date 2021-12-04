"""
    SALE: {saleId, sellerName, customerName, date, itemName, saleValue}
"""
import datetime


class SalesList:
    ID_COUNT = 3
    SALES = [{'saleId': 1, 'sellerName': 'Robert', 'customerName': 'Renanf',
              'date': datetime.datetime.today(), 'itemName': 'Ball', 'saleValue': 100},
             {'saleId': 2, 'sellerName': 'Robert', 'customerName': 'Renanf',
              'date': datetime.datetime.today(), 'itemName': 'Ball', 'saleValue': 100},
             {'saleId': 3, 'sellerName': 'Leo', 'customerName': 'Renanf',
              'date': datetime.datetime.today(), 'itemName': 'Ball', 'saleValue': 100}
             ]

    # FUNCTIONS
    def get_sales(self):
        return self.SALES.copy()

    def get_sales_by_seller(self, seller):
        return [sale for sale in self.SALES if sale['sellerName'] == seller]

    def get_sale_by_id(self, sale_id):
        for i in range(len(self.SALES)):
            if self.SALES[i]['saleId'] == sale_id:
                return self.SALES[i]

        return False

    def insert_new_sale(self, seller_name, customer_name, date, item_name, sale_value):
        new_sale = {'saleId': self.ID_COUNT, 'sellerName': seller_name, 'customerName': customer_name,
                    'date': date, 'itemName': item_name, 'saleValue': sale_value}

        self.SALES.append(new_sale)
        self.ID_COUNT += 1

    def edit_sale_date(self, sale_id, new_date):
        for i in range(len(self.SALES)):
            if self.SALES[i]['saleId'] == sale_id:
                self.SALES[i]['date'] = new_date
                break

    def delete_sale(self, sale_id):
        for i in range(len(self.SALES)):
            if self.SALES[i]['saleId'] == sale_id:
                del self.SALES[i]
                return True

        return False

    def is_empty(self):
        return len(self.SALES) == 0
