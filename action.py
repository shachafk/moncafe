import sys
from persistence import *


def insertActivity(line):
    date = str((line[3]))
    a = Activitie(line[0], line[1], line[2], date)
    repo.Activities.insert(a)



def supplyArrival(line):
    insertActivity(line)

    # update the product supplier
    product_id = line[0]
    quantity = line[1]
    p = Product(product_id, '', 0, quantity)
    Products.update(repo.Products, p)

def loadEmploees():
    em = repo.Employees.find_all()
    employees = Employees.find_all(repo.Employees)
    for employee in employees:
        name = str(employee.name)
        salary = employee.salary
        coffestand = employee.coffee_stand
        location = Coffee_stands.findLocation(repo.Coffee_stands, coffestand)
        er = EmployeeReport(name, salary, location, 0)
        repo.EmployeeReports.insert(er)


def loadToReport(emploeeid, product_id, quantity):
    e = Employees.find(repo.Employees, emploeeid)
    name = str(e.name)
    product = Products.find(repo.Products, product_id)
    income = float(product.price) * float(quantity)
    i = EmployeeReports.findIncome(repo.EmployeeReports, name)
    inc = int(i[0])
    income = income + inc
    repo.EmployeeReports.update(name, income)


def sale(line):
    product_id = line[0]
    quantity = line[1]
    emploeeid = line[2]
    date = line[3]
    q = Products.find(repo.Products, product_id)
    i = -int(quantity)
    y = int(q.quantity)
    # check if there is enough products for the activity
    if i <= y:
        u = Product(product_id, '', 0, y - i)
        insertActivity(line)
        Products.update(repo.Products, u)
        loadToReport(emploeeid, product_id, i)


def handleLine(line):
    i = line[1]
    if i > '0':
        supplyArrival(line)
    elif i < '0':
        sale(line)


def main(args):
    with open(args[1]) as inf:
        for line in inf:
            line = line.strip()
            line = [x.strip() for x in line.split(',')]
            handleLine(line)


if __name__ == '__main__':
    loadEmploees()
    main(sys.argv)
