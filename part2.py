import sqlite3

#connect to database
conn = sqlite3.connect('northwind_small.sqlite3')
curs = conn.cursor()

#what is the ten most expensive items (per unit price) in the database
print('What are the ten most expensive items (per unit price) in the '
      'database?')
curs.execute('SELECT Id, ProductName, UnitPrice '
             'FROM Product '
             'ORDER BY UnitPrice DESC '
             'LIMIT 10;')
print('\n'.join([str(row) for row in curs]), '\n')

# Find average employee age at time of hire.
print('What is the average age of an employee at the time of their hiring? '
      '(Hint: a lot of arithmetic works with dates.)')
curs.execute('SELECT AVG((JULIANDAY(HireDate)-JULIANDAY(Birthdate))/365.25) '
             'FROM Employee;')
print(curs.fetchall(), '\n')

# Check: What numbers do different methods of calculating the hire age yield?
curs.execute('SELECT BirthDate, HireDate, HireDate - BirthDate, '
             '(strftime("%Y", HireDate) - strftime("%Y", BirthDate)) - '
             '(strftime("%m-%d", HireDate) < strftime("%m-%d", BirthDate)), '
             '(julianday(HireDate)-julianday(Birthdate))/365.25 '
             'FROM Employee;')
print('\n'.join([str(row) for row in curs]), '\n')

print('(Stretch) How does the average age of employee at hire vary by city?')
curs.execute('SELECT City, '
             'AVG((JULIANDAY(HireDate)-JULIANDAY(Birthdate))/365.25) '
             'FROM Employee '
             'GROUP BY City;')
print('\n'.join([str(row) for row in curs]), '\n')

# Part 3 - Sailing the Northwind Seas

#  Match the 10 most expensive items by unit price with their suppliers.
print('What are the ten most expensive items (per unit price) in the '
      'database and their suppliers?')
curs.execute('SELECT Supplier.Id, CompanyName, top10.Id, ProductName, '
             'UnitPrice FROM '
             '(SELECT Id, SupplierID, ProductName, UnitPrice '
             'FROM Product '
             'ORDER BY UnitPrice DESC '
             'LIMIT 10) AS top10 '
             'JOIN Supplier ON top10.SupplierId = Supplier.Id;')
print('\n'.join([str(row) for row in curs]), '\n')

# Find the category with the greatest number of unique products.
# We don't need the DISTINCT keyword, because we're working with a primary key.
# This one could also be done with MAX and a subquery.
print('What is the largest category (by number of unique products in it)?')
curs.execute('SELECT CategoryID, CategoryName, '
             'COUNT(Product.ID) AS numProducts '
             'FROM Category LEFT OUTER JOIN Product ON '
             'Product.CategoryID = Category.Id '
             'GROUP BY CategoryID, CategoryName '
             'ORDER BY numProducts DESC '
             'LIMIT 1;')
print(curs.fetchall(), '\n')

# Find the employee with the most territories.
print('(Stretch) Who\'s the employee with the most territories? Use '
      'TerritoryId (not name, region, or other fields) as the unique '
      'identifier for territories.')
curs.execute('SELECT Employee.Id, Title, FirstName, LastName, numTerritories '
             'FROM '
             '(SELECT EmployeeID, COUNT(TerritoryID) as numTerritories '
             'FROM EmployeeTerritory '
             'GROUP BY EmployeeID '
             'ORDER BY numTerritories DESC '
             'LIMIT 1) '
             'JOIN Employee ON EmployeeID = Employee.Id;')
print(curs.fetchall(), '\n')


conn.close()
