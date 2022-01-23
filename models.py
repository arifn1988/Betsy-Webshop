import peewee
# Models go here

db = peewee.SqliteDatabase(':memory:')

class User(peewee.Model):
	username= peewee.CharField()
	address= peewee.CharField()
	billing_information= peewee.CharField()

	class Meta:
		database =db

class Product(peewee.Model):
	name= peewee.CharField()
	owner_id = peewee.ForeignKeyField(User)
	description =  peewee.CharField()
	price_per_unit = peewee.FloatField()
	quantity = peewee.IntegerField()

	class Meta: 
		database=db

class Tag(peewee.Model):
	tag = peewee.CharField()

	class Meta:
		database = db  

class ProductTag(peewee.Model):
	product_id = peewee.ForeignKeyField(Product)
	tag_id= peewee.ForeignKeyField(Tag)

	class Meta:
		database = db

class Sales(peewee.Model):
	product_id = peewee.ForeignKeyField(Product)
	buyer_id = peewee.ForeignKeyField(User)
	quantity=peewee.IntegerField()
	sell_date = peewee.DateField()

	class Meta :
		database =db

