#!/bin/python2
from mysql.connector import (connection) #import library mysql
import datetime  #import library mysql
import sys #import library sys
try:
  import paho.mqtt.client as mqtt
  import paho.mqtt.publish as publish
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.client"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish  #import library paho.mqtt.client for mqtt client
from config import usermariadb, passwordmariadb, hostmariadb, databasemariadb, portamqtt, usernameadminmqtt, passwordadminmqtt, hostmqtt




global id_valore
id_valore  = "1"
x = 1
def on_connect(mqttc, obj, flags, rc): #when on connect
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg): #when recive a message
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload)) #print for debug
    if (msg.topic == "ora" and str(msg.payload)== "topic"): #if topic is ora unsubscribe and subscribe the topic
      unsubscribe(1)
      subscribe(1)
    else: # seno la si si tratta normale  DA TRADURRE
      topic = msg.topic #save the topic on a variable
      valore = str(msg.payload) # save the value with message on this topic on a variable but before convert to stringsededww

      id_topic(topic) #wen findi id of topic on database
      inserire_topic(valore)  #save value of topic within the database on id
      cnx.commit()

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def id_topic (topic1):
       topic3 = ("SELECT idtopic FROM  topic WHERE topic.nome_topic =('%s')") #querry mysql
       cursor.execute(topic3 %(topic1))  #execute of querry
       for row in cursor.fetchall() :
            global id_valore
            id_valore = row[0] #save the id of topic in a variable
            print (id_valore) #print for debug



mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
mqttc.username_pw_set(usernameadminmqtt, passwordadminmqtt)
mqttc.connect(hostmqtt,portamqtt, 60)

cnx = connection.MySQLConnection(user=usermariadb,password=passwordmariadb,
                              host=hostmariadb,
                               database=databasemariadb)  #connect to mariadb database

cursor = cnx.cursor()
def inserire_topic(valore_topic):
  iddati(1) #we take up the id of the data and put it in a variable  global iddativ
  idDati =int(iddativ) +1 #increment id max
  global id_valore
  idtopic = int(id_valore) #we make a whole the id of the variable
  data_valore = datetime.datetime.now() #save de time up to the second
  insert_topic =("INSERT INTO dati "
                 "(iddati,idtopic, valore_topic,data_topic,creatore) "
                 "VALUES (%s,%s,%s,%s,'1')") # querry for save the value in database
  dati_topic=(idDati,idtopic,valore_topic,data_valore) #create arrya with all the data to be saved
  cursor.execute(insert_topic, dati_topic) # execute querry
  emp_no = cursor.lastrowid
  print (dati_topic) #print for debug


def iddati(a): #we take up the id of the data and put it in a variable  global iddativ
    cursor.execute(" SELECT MAX(iddati) FROM dati")
    for row in cursor.fetchall():
        global iddativ
        iddativ=row[0]
        print(iddativ)

def subscribe(c):
    cursor.execute(" SELECT nome_topic,qos  FROM topic" ) #query to take the name of the topic and the value of qos
    for row in cursor.fetchall():
        topic = str(row[0]) #convert topic to string
        qos = row[1]
        mqttc.subscribe(topic, qos) # subscribe at the topic
        print(topic,qos) #print for debug

def unsubscribe(c):
    cursor.execute(" SELECT nome_topic FROM topic" ) #query to take the name of the topic
    for row in cursor.fetchall():
          topic = str(row[0])
          print(topic) #print for debug
          mqttc.unsubscribe(topic) #unsubscribe del topic

if x == 1:
     subscribe(1)
     x = 2


mqttc.loop_forever()
