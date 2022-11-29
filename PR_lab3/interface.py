import requests

hostName = "localhost"
serverPort = 8080
address = "http://%s:%s" % (hostName, serverPort)

def retrieve_id(employee_id):
    r = requests.get(address + "/" + str(employee_id))
    return r.content.decode("utf-8")

def retrieve_many(n_start, n_end):
    r = requests.get(address + "/" + str(n_start) + "/" + str(n_end))
    return r.content.decode("utf-8")

def insert_row(fname, lname, pay):
    r = requests.post(address, json={"name":fname, "last name":lname, "pay":pay})
    if (r.status_code == 200):
        print("200 OK")
    else:
        print(str(r.status_code) + " An error occured.")

def edit_row(id, column, value):
    r = requests.put(address, json={"id":id, "column":column, "value":value})
    if (r.status_code == 200):
        print("200 OK")
    else:
        print(str(r.status_code) + " An error occured.")

def delete_row(id):
    r = requests.delete(address, json={"id":id})
    if (r.status_code == 200):
        print("200 OK")
    else:
        print(str(r.status_code) + " An error occured.")