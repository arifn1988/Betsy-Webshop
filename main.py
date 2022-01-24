__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models as m
import peewee
import csv
from datetime import date
import os

def main():
    create_db()    
    #search('table')
    #list_user_products(2)
    #list_products_per_tag(2)
    #add_product_to_catalog(2,[{'name':'psp','owner_id':2,'description':'a handheld gaming console','price_per_unit':200,'quantity':2}])
    #update_stock(3,10)
    #remove_product(1)
    #purchase_product(1,2,1)

def search(term): 
    for item in m.Product.select(m.Product.name,m.Product.description).dicts():
        if(term.lower() in item['name'].lower() or term.lower() in item['description']):
            print(item)

def list_user_products(user_id):

    if m.User.select().where(m.User.id==user_id):
        for item in m.Product.select(m.Product.name,m.User.username).join(m.User).where(m.User.id==user_id).dicts():
            print(item)
    else:
        print('User does not exist')

def list_products_per_tag(tag_id):
    for item in m.Product.select(m.Product.name,m.Tag.tag).join(m.ProductTag).join(m.Tag).where(m.Tag.id==tag_id).dicts():
        print(item)


def add_product_to_catalog(user_id, product):
   m.Product.insert(product).execute()
   list_user_products(user_id)


def update_stock(product_id, new_quantity):
    m.Product.update({m.Product.quantity : new_quantity}).where(m.Product.id==product_id).execute()

    print(m.Product.select().where(product_id==m.Product.id).dicts().get())

def purchase_product(product_id, buyer_id, quantity):
     
    product = m.Product.select().where(product_id==m.Product.id).first()

    if not product:
        quit('This product does not exist')
    elif product.quantity-quantity <0:
        quit('Not enough product in stock')
    elif (product.owner_id.id==buyer_id):
        quit('Can\t buy your own product')
    else:
        sale = {'product_id':product_id,'buyer_id':buyer_id,'quantity':quantity,'sell_date':date.today().isoformat()}
        m.Sales.insert(sale).execute()    
        update_stock(product_id,product.quantity-quantity)

def remove_product(product_id):
    m.Product.delete().where(m.Product.id==product_id).execute()
    m.ProductTag.delete().where(m.ProductTag.product_id==product_id).execute()

    for item in m.ProductTag.select().dicts():
        print(item)

def csv_reader(file):
    file = open(file)
    return csv.DictReader(file)

def create_db():
    directory = os.path.dirname(os.path.abspath(__file__))
    users = csv_reader(os.path.join(directory,'csv/users.csv'))
    products=csv_reader(os.path.join(directory,'csv/products.csv'))
    tags =csv_reader(os.path.join(directory,'csv/tag.csv'))
    products_tags=csv_reader(os.path.join(directory,'csv/product_tag.csv'))

    m.db.create_tables([m.User,m.Product,m.Tag,m.ProductTag,m.Sales])
    m.User.insert_many(users).execute()
    m.Product.insert_many(products).execute()
    m.Tag.insert_many(tags).execute()
    m.ProductTag.insert_many(products_tags).execute()

if __name__ =='__main__':
    main()