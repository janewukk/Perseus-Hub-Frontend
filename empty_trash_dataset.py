import MySQLdb

# Main entry
def main():
	# mysql connection config
	host = "localhost"
	port = 3306
	user = "forge"
	password = "IdiaIRe3pjUJuRz9T5GN"
	db = "perseusdb"
	# connect
	db = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db)
	# delete trashed dataset
	db.query("DELETE FROM app_dataset WHERE trashed = 1")
	print "cleared!"

if __name__ == '__main__':
	"""
	The MySQL cleaner
	
	This piece of script should be scheduled to run every night
	to clear out trashed dataset
	"""
	main()