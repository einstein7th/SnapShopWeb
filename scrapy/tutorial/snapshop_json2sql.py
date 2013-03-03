#!/usr/bin/python

import sys
import MySQLdb
import json
import re

print "connecting to database..."
db = MySQLdb.connect("localhost","root", "","snapshop")
c=db.cursor()

cat_dict = dict()
#maintain a cnid to mysql id mapping
print "openning categories json file..."
with open("all_categories.txt") as category_file:
	category_data = json.load(category_file)

i=0
print "parsing and inserting categories..."
while i<259: #there are that many total categories
	#grab the fields from the json
	cnid = category_data[i]['cnid']
	name = category_data[i]['name']
	parent = category_data[i]['parent']
	#if parent is "", then assign NULL in mysql.  
	if(parent==""):
		parent = "NULL"
	else:
		#else grab the id from the dictionary
		parent = cat_dict[parent]
	#build our query
	values = "(0,'N/A','" + name + "','" + cnid + "',"+ str(parent)+")"
	query = "INSERT INTO  shop_categories VALUES " + values
	
	try:
   	c.execute(query)
   	db.commit()
   	#make hash of cnid to the id generated.  
	cat_dict[cnid] = i+1 #it so happens that i starts at 0, and the id's start at 1.  

	except:
   		db.rollback()
	i+=1	

#insert items, hooked up to the categories.  
print "parsing and inserting items..."
with open('all_items_detail.txt') as data_file:
	data = json.load(data_file)

i=0
while i<10033:
	#escape any characters to avoid bad sql queries.  
	item_name = re.escape(data[i]["name"])
	item_price = data[i]['price']
	item_size = re.escape(data[i]['size'])
	item_unit_price = re.escape(data[i]['unit_price'])
	item_thumb_small = re.escape(data[i]['small_image'])
	item_thumb_medium = re.escape(data[i]['med_image'])
	item_thumb_large = re.escape(data[i]['large_image'])
	item_peapod_productid = re.escape(data[i]['productId'])
	item_peapod_cnid = re.escape(data[i]["cnid"])
	item_nutrition_html = re.escape(data[i]["nutrition"])
	# ingredients and details have bad encoding, throws error...

	item_ingredients_html = "N/A" #re.escape(data[i]["ingredients"])
	item_details_html = "N/A" #re.escape(data[i]["details"])
	# we do not have a description field.  
	item_description_html = "N/A"

	# insert info into database.
	columns = " (item_category_id, item_name, item_price, item_size, item_unit_price, item_thumb_small, item_thumb_medium, item_thumb_large, item_peapod_productid, item_peapod_cnid, item_nutrition_html, item_description_html, item_ingredients_html, item_details_html ) "
	values = " ("+ str(cat_dict[item_peapod_cnid]) +",'" + item_name + "'," + item_price + ",'" + item_size + "','" +item_unit_price + "','" +item_thumb_small + "','"+item_thumb_medium+ "','" + item_thumb_large +"','"+item_peapod_productid+"','"+item_peapod_cnid+"','" +item_nutrition_html+"','"+item_description_html+"','"+item_ingredients_html+"','"+item_details_html+  "' ) "
	query = "INSERT INTO  shop_shopitem " + columns + " VALUES " + values
	try:
   		c.execute(query)
   		db.commit()
	except:
   		db.rollback()

	i+=1	
print "finished! closing database connection..."
db.close()
print "fin."