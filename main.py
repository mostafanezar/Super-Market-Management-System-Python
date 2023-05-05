import os

class Product:
    def __init__(self, code, name, price, quantity):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity

class Customer:
    def __init__(self, name, phone, basket):
        self.name = name
        self.phone = phone
        self.basket = basket

def insert_product():
    with open('inventory.txt', 'r') as file:
        existing_products = set(line.split('\t')[1].strip() for line in file)
    with open('inventory.txt', 'a') as file:
        while True:
            code = input('Enter the product code: ')
            name = input('Enter the product name: ')
            if name in existing_products:
                print('The product name already exists.')
                continue
            price = input('Enter the product price: ')
            quantity = input('Enter the product quantity: ')
            file.write(code + '\t' + name + '\t' + price + '\t' + quantity + '\n')
            print('Product added successfully.')
            break
def view_all_products():
    with open('inventory.txt', 'r') as file:
        print('Code\tName\tPrice\tQuantity')
        print('--------------------------------')
        for line in file:
            print(line, end='')

def search_product():
    name = input('Enter the product name: ')
    with open('inventory.txt', 'r') as file:
        flag = False
        for line in file:
            fields = line.split('\t')
            if fields[1] == name:
                flag = True
                print('Code\tName\tPrice\tQuantity')
                print('--------------------------------')
                print(line)
        if not flag:
            print('The product name was not found.')
def update_product():
    name = input('Enter the product name: ')
    file = open('inventory.txt', 'r')
    tempfile = open('tempinventory.txt', 'w')
    flag = False
    for line in file:
        st = line.split('\t')
        if st[1] == name:
            flag = True
            while flag:
                print('Press 1 to edit code')
                print('Press 2 to edit name')
                print('Press 3 to edit price')
                print('Press 4 to edit quantity')
                print('Press 0 to confirm changes')
                x = int(input())
                if x == 1:
                    code = input('Enter new code: ')
                    st[0] = code
                elif x == 2:
                    name = input('Enter new name: ')
                    st[1] = name
                elif x == 3:
                    price = input('Enter new price: ')
                    st[2] = price
                elif x == 4:
                    quantity = input('Enter new quantity: ')
                    st[3] = quantity
                elif x == 0:
                    break
            line = '\t'.join(st) + '\n'
        else:
            line = line.rstrip('\n')
        tempfile.write(line)
    file.close()
    tempfile.close()
    os.remove('inventory.txt')
    os.rename('tempinventory.txt', 'inventory.txt')
    if not flag:
        print('The product name was not found.')
    else:
        print('Product updated successfully.')
def delete_product():
    name = input('Enter the product name: ')
    file = open('inventory.txt', 'r')
    tempfile = open('tempinventory.txt', 'w')
    flag = False
    for line in file:
        st = line.split('\t')
        if st[1] == name:
            flag = True
            continue
        tempfile.write(line)
    file.close()
    tempfile.close()
    os.remove('inventory.txt')
    os.rename('tempinventory.txt', 'inventory.txt')
    if not flag:
        print('The product name was not found.')
    else:
        print('Product deleted successfully.')
def add_to_basket(basket):
    name = input('Enter the product name: ')
    quantity = input('Enter the quantity: ')
    with open('inventory.txt', 'r') as file:
        flag = False
        for line in file:
            fields = line.split('\t')
            if fields[1] == name:
                flag = True
                if int(fields[3]) >= int(quantity):
                    basket.append(Product(fields[0], fields[1], fields[2], quantity))
                    print('Product added to basket successfully.')
                else:
                    print('Sorry, the required quantity is not available.')
        if not flag:
            print('The product name was not found.')
def view_basket(basket):
    if len(basket) == 0:
        print('Basket is empty.')
    else:
        total_price = 0
        print('Code\tName\tPrice\tQuantity')
        print('--------------------------------')
        for item in basket:
            print(item.code + '\t' + item.name + '\t' + item.price + '\t' + item.quantity)
            total_price += float(item.price) * int(item.quantity)
        print('--------------------------------')
        print('Total price:', total_price)
def checkout(basket):
    if len(basket) == 0:
        print('Basket is empty.')
    else:
        name = input('Enter your name: ')
        phone = input('Enter your phone number: ')
        customer = Customer(name, phone, basket)
        total_price = 0
        print('Code\tName\tPrice\tQuantity')
        print('--------------------------------')
        for item in customer.basket:
            print(item.code + '\t\t' + item.name + '\t\t' + item.price + '\t\t' + item.quantity)
            total_price += float(item.price) * int(item.quantity)
            with open('inventory.txt', 'r') as invfile:
                invlines = invfile.readlines()
            invfile.close()
            with open('inventory.txt', 'w') as invfile:
                for invline in invlines:
                    fields = invline.split('\t')
                    if fields[0] == item.code:
                        fields[3] = str(int(fields[3]) - int(item.quantity))
                        invline = '\t'.join(fields) + '\n'
                    invfile.write(invline)
        print('--------------------------------')
        print('Total price:', total_price)
        print('================================')
        with open('sales.txt', 'a') as file:
            file.write('Customer Name: ' + customer.name + '\n')
            file.write('Phone Number: ' + customer.phone + '\n')
            file.write('Code\tName\tPrice\tQuantity\n')
            file.write('--------------------------------\n')
            for item in customer.basket:
                file.write(item.code + '\t' + item.name + '\t' + item.price + '\t' + item.quantity + '\n')
            file.write('--------------------------------\n')
            file.write('Total price: ' + str(total_price) + '\n')
            file.write('================================\n')
        print('Checkout successful. Thank you for shopping with us!')
        basket.clear()

def view_all_orders_details():
    with open('sales.txt', 'r') as file:
        orders = []
        for line in file:
            if line.startswith('Customer Name:'):
                order = {'customer_name': line.split(':')[1].strip(), 'phone_number': '', 'products': []}
            elif line.startswith('Phone Number:'):
                order['phone_number'] = line.split(':')[1].strip()
            elif line.startswith('Code'):
                fields = line.split('\t')
                product = {'code': fields[0], 'name': fields[1], 'price': fields[2], 'quantity': fields[3].strip()}
                order['products'].append(product)
            elif line.startswith('Total price:'):
                order['total_price'] = line.strip()
                orders.append(order)
        if orders:
            print('Orders:')
            for order in orders:
                print('Customer Name:', order['customer_name'])
                print('Phone Number:', order['phone_number'])
                for product in order['products']:
                    print('Product Code:', product['code'])
                    print('Product Name:', product['name'])
                    print('Product Price:', product['price'])
                print(order['total_price'])
                print('================================')
        else:
            print('No orders found.')
def main():
    basket = []
    print('\t\t1_seller', '\t\t2_client')
    choice = input('Enter your choice: ')
    if choice == '1':
        choice = input('\t\tEnter password:\t\n ')
        if choice == '123':
            while True:
                print('-------------------------------------------------------')
                print('1. View all products')
                print('2. Search product')
                print('3. Delete product')
                print('4. Add to product')
                print('5. update product')
                print('6. view customer orders')
                print('0. Exit')
                choice = input('Enter your choice: ')
                if choice == '1':
                    view_all_products()
                elif choice == '2':
                    search_product()
                elif choice == '3':
                    delete_product()
                elif choice == '4':
                    insert_product()
                elif choice == '5' :
                    update_product()
                elif choice == '6' :
                    view_all_orders_details()
                elif choice == '0':
                    break
                else:
                    print('Invalid choice. Please try again.')
    elif choice == '2':
        while True:
            print('-------------------------------------------------------')
            print('1. View all products')
            print('2. Search product')
            print('3. Add to basket')
            print('4. View basket')
            print('5. Checkout')
            print('0. Exit')
            choice = input('Enter your choice: ')
            if choice == '1':
                view_all_products()
            elif choice == '2':
                search_product()
            elif choice == '3':
                add_to_basket(basket)
            elif choice == '4':
                view_basket(basket)
            elif choice == '5':
                checkout(basket)
            elif choice == '0':
                    break
            else:
                print('Invalid choice. Please try again.')
if __name__ == '__main__':
    basket = []
    main()
