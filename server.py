import pymysql.cursors

dbhost='localhost'
dbuser='root'
dbpassword='root'

def userSignUp(email,password,name,street,city,state,zipCode,isBusiness,marriage,gender,age,income,category,gross):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="INSERT INTO Customers (Email,Pwd,Name,Street,City,State,ZIP,IsBusiness) VALUES ('{}','{}','{}','{}','{}','{}','{}',{})"\
                .format(email,password,name,street,city,state,zipCode,isBusiness)
            cursor.execute(query)
        connection.commit()
        
        with connection.cursor() as cursor:
            query="SELECT CustomerID FROM Customers WHERE Email='{}'".format(email)
            cursor.execute(query)
            customerID=cursor.fetchone()['CustomerID']
        if isBusiness:
            with connection.cursor() as cursor:
                query="INSERT INTO Business (CustomerID,CategoryID,GrossIncome) VALUES ({},{},{})"\
                    .format(customerID,category,gross)
                cursor.execute(query)
            connection.commit()
        else:
            with connection.cursor() as cursor:
                query="INSERT INTO Home (CustomerID,Income,Age,Gender,Marriage) VALUES ({},{},{},{},{})"\
                    .format(customerID,income,age,gender,marriage)
                cursor.execute(query)
            connection.commit()
        return customerID
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()

def browse(keyword,sort,productType):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="SELECT * FROM Products WHERE Name LIKE '%{}%'".format(keyword)
            if productType!="":
                query+=" AND TypeID={}".format(productType)
            query+=" ORDER BY Price "
            if sort:
                query+="ASC"
            else:
                query+="DESC"
            cursor.execute(query)
            productlist=[]
            for row in cursor:
                productlist.append(row)
            return productlist
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()
        
def purchase(customerID,productID,quantity,salespersonID):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="UPDATE Products SET Inventory=Inventory-{} WHERE ProductID={}".format(quantity,productID)
            cursor.execute(query)
        connection.commit()
        with connection.cursor() as cursor:
            query="INSERT INTO Transactions (SalespersonID, ProductID, Quantity, CustomerID) VALUES ({},{},{},{})"\
                .format(salespersonID,productID,quantity,customerID)
            cursor.execute(query)
        connection.commit()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()
        
def history(customerId):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="SELECT Products.Name,Price,Quantity,DATE_FORMAT(TransactionDate, '%m %d %Y') AS Date FROM Transactions LEFT OUTER JOIN Products ON Transactions.ProductID=Products.ProductID WHERE CustomerID={} ORDER BY TransactionDate DESC".format(customerId)
            print(query)
            cursor.execute(query)
            historylist=[]
            for row in cursor:
                historylist.append(row)
            return historylist
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()

def changeInventory(productID,inventory):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="UPDATE Products SET Inventory={} WHERE ProductID={}".format(inventory,productID)
            cursor.execute(query)
        connection.commit()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()
        
def addProduct(productname,inventory,price,producttype):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="INSERT INTO Products (Name,Inventory,Price,TypeID) VALUES ('{}',{},{},{})".format(productname,inventory,price,producttype)
            cursor.execute(query)
        connection.commit()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()

def userSignIn(email,password):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="SELECT CustomerID,Name FROM Customers WHERE Email='{}' AND Pwd='{}'".format(email,password)
            cursor.execute(query)
            if (not (cursor.rowcount)):
                return "Not Match"
            else:
                return cursor.fetchone()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()
        
def staffSignIn(email,password):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="SELECT SalespersonID,Name FROM Salespersons WHERE Email='{}' AND Pwd='{}'".format(email,password)
            cursor.execute(query)
            if (not (cursor.rowcount)):
                return "Not Match"
            else:
                return cursor.fetchone()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()

def aggregate():
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="SELECT P.Name AS Name ,CAST(SUM(Quantity) AS SIGNED) AS Sales,P.price*SUM(Quantity) AS Profits FROM Transactions T,Products P WHERE T.ProductID=P.ProductID GROUP BY T.ProductID ORDER BY Sales DESC, Profits DESC"
            cursor.execute(query)
            sales=[]
            for row in cursor:
                sales.append(row)
            query="SELECT PT.Name FROM Products P,ProductType PT WHERE PT.typeID=P.typeID AND P.ProductId=(SELECT ProductID FROM Transactions GROUP BY ProductID HAVING SUM(Quantity)=(SELECT MAX(temp.sum) FROM(SELECT ProductID,SUM(Quantity) AS sum FROM Transactions T GROUP BY T.ProductID)AS temp ))"
            cursor.execute(query)
            pt=cursor.fetchone()
            print(query,pt)
            query="SELECT R.Name,CAST(SUM(Quantity) AS SIGNED) AS Sale FROM Transactions T,Salespersons SP,Stores S,Regions R WHERE T.SalespersonID=SP.SalespersonID AND SP.StoreID=S.StoreID AND S.RegionID=R.RegionID GROUP BY R.RegionID"
            cursor.execute(query)
            region=[]
            for row in cursor:
                region.append(row)
            data = {'salesprofits':sales,'topproducttype':pt,'regionsales':region}
            return data
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()

def businessofproduct(pid):
    connection = pymysql.connect(host=dbhost,
                             user=dbuser,
                             password=dbpassword,
                             db='dbmfinal',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            query="SELECT Name FROM Customers WHERE CustomerID=(SELECT T.CustomerID FROM Transactions T,Products P WHERE P.ProductID={} AND P.ProductID=T.ProductID GROUP BY T.CustomerID ORDER BY SUM(T.Quantity) DESC LIMIT 1)".format(pid)
            cursor.execute(query)
            if (not (cursor.rowcount)):
                return "null"
            else:
                return cursor.fetchone()
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message
    finally:
        connection.close()
##################
##################
from bottle import route, run, get, post, request, static_file
import json

@route('/')
@route('/index')
def index():
    return "LLDAFAHAO"
@post('/signup')
def do_signup():
    email=request.forms.get('email')
    password=request.forms.get('password')
    name=request.forms.get('name')
    street=request.forms.get('street')
    city=request.forms.get('city')
    state=request.forms.get('state')
    zipCode=request.forms.get('zipcode')
    print(zipCode)
    isBusiness=int(request.forms.get('isbusiness'))
    marriage=int(request.forms.get('marriage'))
    gender=int(request.forms.get('gender'))
    age=request.forms.get('age')
    income=request.forms.get('income')
    category=int(request.forms.get('category'))
    gross=request.forms.get('gross')
    response=userSignUp(email,password,name,street,city,state,zipCode,isBusiness,marriage,gender,age,income,category,gross)
    return json.dumps(response)

@post('/browse')
def do_browse():
    keyword=request.forms.get('keyword')
    sort=int(request.forms.get('sort'))
    productType=request.forms.get('producttype')
    response=browse(keyword,sort,productType)
    return json.dumps(response)

@post('/purchase')
def do_purchase():
    customerID=request.forms.get('customerid')
    productID=request.forms.get('productid')
    quantity=request.forms.get('quantity')
    salespersonID=request.forms.get('salespersonid')
    response=purchase(customerID,productID,quantity,salespersonID)
    return json.dumps(response)

@post('/history')
def do_history():
    customerId=request.forms.get('customerid')
    response=history(customerId)
    return json.dumps(response)

@post('/changeinventory')
def do_changeinventory():
    productID=request.forms.get('productid')
    inventory=request.forms.get('inventory')
    response=changeInventory(productID,inventory)
    return json.dumps(response)

@post('/addproduct')
def do_addproduct():
    productname=request.forms.get('productname')
    inventory=request.forms.get('inventory')
    price=request.forms.get('price')
    producttype=request.forms.get('producttype')
    response=addProduct(productname,inventory,price,producttype)
    return json.dumps(response)

@post('/signin')
def do_signin():
    email=request.forms.get('email')
    password=request.forms.get('password')
    response=userSignIn(email,password)
    return json.dumps(response)

@post('/staffsignin')
def do_staffsignin():
    email=request.forms.get('email')
    password=request.forms.get('password')
    response=staffSignIn(email,password)
    return json.dumps(response)

@get('/static/<filename>')
def do_staticfile(filename):
    return static_file(filename, root='/root/DBM/static')

@post('/upload')
def do_upload():
    upload=request.files.get('upload')
    print('filename:')
    print(upload.filename)
    upload.save('/root/DBM/static',overwrite=True)
    return 'OK'

@get('/aggregate')
def do_aggregate():
    return json.dumps(aggregate())

@post('/businessofproduct')
def do_bop():
    pid=int(request.forms.get('productid'))
    return json.dumps(businessofproduct(pid))
#############

run(host='45.78.59.251', port=8080)

