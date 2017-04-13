from mysql.connector import (connection) #import library mysql
import datetime #import library datetime
import sys #import library sys
from config import usermariadb, passwordmariadb, hostmariadb, databasemariadb

cnx = connection.MySQLConnection(user=usermariadb,
                              password=passwordmariadb,
                              host=hostmariadb,
                              database=databasemariadb)
cursor=cnx.cursor()
global valore_variabile_ON_dati
global valore_variabile_on
global operatore_variabile_on
global iddativ
global idvariabile_do
global valore_variabile_do
global operatore_variabile_on
global valore_variabile_on
global id_variabile_on
global valore_variabile_ON_dati

def list_scena(b): #
    id_scena_mysql="SELECT idscene FROM scene "
    cursor.execute(id_scena_mysql)
    for row in cursor.fetchall():
        id_scena=row[0]
        print(id_scena)
        controllo_scena(id_scena)


def controllo_scena(idscena):
    a = 0
    id_scena_trigger_mysql="SELECT id_scena_trigger FROM scene_trigger where scene_trigger.id_scena=('%s')"
    cursor.execute(id_scena_trigger_mysql,idscena)
    for row in cursor.fetchall():
        idscena_trigger=row[a]
        print(idscena_trigger)
        controllo_scena_trigger(idscena_trigger)
        a+=1

def controllo_scena_trigger(idscena_trigger):
    valore_variabile_ON_dati_def(idscena_trigger)
    global valore_variabile_ON_dati
    valore_variabile_ON_def(idscena_trigger)
    global valore_variabile_on
    operatore_variabile_on_def
    global operatore_variabile_on
    if (operatore_variabile_on == 0):
        if (valore_variabile_ON_dati == valore_variabile_on):
            esecuzione_scena_trigger(idscena_trigger)
    elif (operatore_variabile_on == 1):
        if (valore_variabile_ON_dati != valore_variabile_on):
            esecuzione_scena_trigger(idscena_trigger)
    elif (operatore_variabile_on == 2):
        if(valore_variabile_ON_dati < valore_variabile_on):
           esecuzione_scena_trigger(idscena_trigger)
    elif(operatore_variabile_on == 3):
        if(valore_variabile_ON_dati<= valore_variabile_on):
            esecuzione_scena_trigger(idscena_trigger)
    elif(operatore_variabile_on ==4):
        if(valore_variabile_ON_dati> valore_variabile_on):
            esecuzione_scena_trigger(idscena_trigger)
    elif(operatore_variabile_on==5):
        if(valore_variabile_ON_dati>=valore_variabile_on):
            esecuzione_scena_trigger(idscena_trigger)


    emp_no = cursor.lastrowid

def esecuzione_scena_trigger(idscena_trigger):
    iddati(1)
    global iddativ
    idDati =int(iddativ) +1
    data_valore = datetime.datetime.now()
    idvariabile_do_mysql="SELECT id_variabile_DO FROM scene_trigger where scene_trigger.id_scena_trigger=('%s')"
    cursor.execute(idvariabile_do_mysql,idscena_trigger)
    for row in cursor.fetchall():
        global idvariabile_do
        idvariabile_do=row[0]
        print(idvariabile_do)
    valore_variabile_do_mysql="SELECT valore_variabile_DO FROM scene_trigger where scene_trigger.id_scena_trigger=('%s')"
    cursor.execute(valore_variabile_do_mysql,idscena_trigger)
    for row in cursor.fetchall():
        global valore_variabile_do
        valore_variabile_do=row[0]
        print(valore_variabile_do)
    insert_variabile =("INSERT INTO dati "
                   "(iddati,idvariabile, valore_variabile,data_variabile,creatore) "
                   "VALUES (%s,%s,%s,%s,'1')")
    dati_variabile=(idDati,idvariabile_do,valore_variabile_do,data_valore)
    cursor.execute(insert_variabile, dati_variabile)
    emp_no = cursor.lastrowid
    print (dati_variabile)

def iddati(a):
    cursor.execute(" SELECT MAX(iddati) FROM dati")
    for row in cursor.fetchall():
        global iddativ
        iddativ=row[0]
        print(iddativ)

def operatore_variabile_on_def(idscena_trigger):
    operatore_variabile_on_mysql="SELECT operatore_variabile_on FROM scene_trigger where scene_trigger.id_scena_trigger=('%s')"
    cursor.execute(operatore_variabile_on_mysql,idscena_trigger)
    for row in cursor.fetchall():
        global operatore_variabile_on
        operatore_variabile_on=row[0]
        print(operatore_variabile_on)

def valore_variabile_ON_def(idscena_trigger):
    valore_variabile_on_mysql="SELECT valore_variabile_on FROM scene_trigger WHERE scene_trigger.id_scena_trigger=('%s')"
    cursor.execute(valore_variabile_on_mysql,idscena_trigger)
    for row in cursor.fetchall():
        global valore_variabile_on
        valore_variabile_on=row[0]
        print(valore_variabile_on)


def id_variabile_on_def(idscena_trigger):
    id_variabile_on="SELECT id_variabile_on FROM scene_trigger WHERE scene_trigger.id_scena_trigger =('%s')"
    cursor.execute(id_variabile_on,idscena_trigger)
    for row in cursor.fetchall():
        global id_variabile_on
        id_variabile_on=row[0]
        print(id_variabile_on)

def valore_variabile_ON_dati_def(idscena_trigger):
    id_variabile_on_def(idscena_trigger)
    global id_variabile_on
    max_iddati_variabile="SELECT MAX(iddati) FROM dati WHERE dati.idvariabile=('%s')"
    cursor.execute(max_iddati_variabile,id_variabile_on)
    for row in cursor.fetchall():
        id_dati_variabilemax=row[0]
        print(id_dati_variabilemax)
    valore_variabile_ON_dati1="SELECT valore_variabile FROM dati  WHERE dati.idvariabile = ('%s') AND dati.iddati = ('%s')"
    variabili=(id_variabile_on,id_dati_variabilemax)
    cursor.execute(valore_variabile_ON_dati1,variabili)
    for row in cursor.fetchall():
        global valore_variabile_ON_dati
        valore_variabile_ON_dati=row[0]
        print(valore_variabile_ON_dati)

while 1<2:
    list_scena(1)

# insert_variabile =("INSERT INTO dati "
#                "(iddati,idvariabile, valore_variabile,data_variabile,creatore) "
#                "VALUES (%s,%s,%s,%s,'1')")
# dati_variabile=(idDati,idvariabile,valore_variabile,data_valore)
# cursor.execute(insert_variabile, dati_variabile)
# emp_no = cursor.lastrowid
