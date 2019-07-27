import mysql.connector
import config
import time
import requests
import json

api_key = config.api_key

#creates and opens a connection to the AWS database
def create_cnx_cur():
    cnx = mysql.connector.connect(
            host = config.host,
            user = config.user,
            passwd = config.password)

    cursor = cnx.cursor()
    return (cnx, cursor)


def close_connection(cnx, cursor):
    cursor.close()
    cnx.close()

#creates a new database in the AWS database
def create_database(cursor, database):
    try:
        #it will try to create a database with whatever name passed through
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
        #if this fails, the error will print out as a message
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        try:
            exit()
        except NameError:
            return

    #this is going to try the above function
    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, db_name)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit()


def add_tables_to_db(TABLES, cursor):
    from mysql.connector import errorcode
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute("""USE yelp""")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def yelp_call(url, api_key, url_params = None):
    headers = {'Authorization': 'Bearer {}'.format(api_key)}
    response = requests.get(url, headers=headers, params=url_params)
    data = response.json()
    return data


#adds results just gotten from API to data base
def add_businesses_to_db(tryresults):
    cnx_cur = create_cnx_cur()
    cnx = cnx_cur[0]
    cursor = cnx_cur[1]
    # for each business that is in our results from our API request
    for i in range(len(tryresults['businesses'])):
        # sql statement to add row
        add_business = ("""INSERT INTO businesses
                                VALUES (%s, %s, %s, %s, %s)
                        """)
        try:
            # note: location is made of a two-item list -- the first address line
            # and the city/state/etc.
            business_values = (tryresults['businesses'][i]['id'],
                            tryresults['businesses'][i]['name'],
                            tryresults['businesses'][i]['price'],
                            tryresults['businesses'][i]['rating'],
                            tryresults['businesses'][i]['location']['display_address'][0]+", "+tryresults['businesses'][i]['location']['display_address'][1])

            cursor.execute("USE yelp") #gets us into the yelp db instance
            cursor.execute(add_business, business_values)

        except mysql.connector.IntegrityError: # here to skip existing entries
            continue
        except KeyError: # here to skip the restaurants that are missing values, such as price
            continue
        except IndexError:
            try:
                print("Issue with: ", tryresults['businesses'][i])
                business_values = (tryresults['businesses'][i]['id'],
                                tryresults['businesses'][i]['name'],
                               tryresults['businesses'][i]['price'],
                               tryresults['businesses'][i]['rating'],
                               tryresults['businesses'][i]['location']['display_address'][0])
                cursor.execute("USE yelp") #gets us into the yelp db instance
                cursor.execute(add_business, business_values)
            except:
                print("Issue with: ", tryresults['businesses'][i])
                business_values = (tryresults['businesses'][i]['id'],
                                tryresults['businesses'][i]['name'],
                               tryresults['businesses'][i]['price'],
                               tryresults['businesses'][i]['rating'],
                               null)
                cursor.execute("USE yelp") #gets us into the yelp db instance
                cursor.execute(add_business, business_values)




    cnx.commit()
    close_connection(cnx, cursor)


def all_results(tryresults, url, api_key, url_params=None):
    num = tryresults['total']
    print('{} total matches found.'.format(num))
    cur = 0
    while cur < num and cur < 500:
        # This gets you to where you should be in the data, rather than just keeping grabbing
        # the first 50 over and over again
        url_params['offset'] = cur
        results = yelp_call(url, api_key, url_params)
        add_businesses_to_db(results)
        time.sleep(1) #Wait a second
        cur += 50 # count to go to next 50 results
    return


def get_reviews(businessIds, url_template, api_key):
    reviews = []
    for i in businessIds:
        url = url_template.format(i)
        reviews.append({'businessId': i, 'reviews': yelp_call(url, api_key)['reviews']})
    return reviews


def add_reviews_to_db(businessIds, url_template, api_key):
    cnx = mysql.connector.connect(
        host = config.host,
        user = config.user,
        passwd = config.password)

    cursor = cnx.cursor()

    results = get_reviews(businessIds, url_template, api_key)

    # for each review that is in our dictionary of results from our API requests
    # get each dictionary with all 3 reviews for each business
    for i in range(len(results)):
        # gets each review from dictionary
        for review in results[i]['reviews']:
            # sql statement to add row
            add_review = ("""INSERT INTO reviews
                                    VALUES (%s, %s, %s, %s, %s, %s)
                            """)
            try:
                review_values = (review['id'], results[i]['businessId'],
                                   review['user']['id'], review['text'], review['rating'],
                                   review['time_created'])

                cursor.execute("USE yelp") #gets us into the yelp db instance
                cursor.execute(add_review, review_values)

            except mysql.connector.IntegrityError: # here to skip existing entries
                continue
            except KeyError: # here to skip the restaurants that are missing values, such as price
                continue

    cnx.commit()
    cursor.close()
    cnx.close()
