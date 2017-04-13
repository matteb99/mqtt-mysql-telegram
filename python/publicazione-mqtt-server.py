from mysql.connector import (connection)
import sys
import datetime
try:
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.publish"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt
    import paho.mqtt.publish as publish
from config import usermariadb, passwordmariadb, hostmariadb, databasemariadb, portamqtt,usernameadminmqtt, passwordadminmqtt, hostmqtt

tempo_last=1
idvarimaxlast=0
b = 0
cnx = connection.MySQLConnection(user=usermariadb,
                              password=passwordmariadb,
                              host=hostmariadb,
                              database=databasemariadb)

def on_message(mqttc, obj, msg): #when recive a message
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload)) #print for debug
    if (msg.topic == "ora" and str(msg.payload)== "pub"): #if topic is ora unsubscribe and subscribe the topic
      iddativ=int(iddati(1))
      creatorev=creatore(iddativ)
      c=int(creatorev)
      id_topicv=id_topic(iddativ)
      idtipo_topicv=idtipo_topic(id_topicv)
      if idtipo_topicv!=3 :
              if c == 1:
                  nome_topicv=nome_topic(id_topicv)
                  valore_topicv=valore_topic(id_topicv)

              else:
                  nome_topicv=valore_topic(iddativ)
                  valore_topicv=last_value_topic(id_topicv)
      qos_topicv=qos_topic(id_topicv)
      idnodo_topicv=idnodo_topic(id_topicv)
      id_utentev=id_utente(idnodo_topicv)
      nome_utentev=nome_utente(id_utentev)
      password_utentev=password_utente(id_utentev)
      publish.single(nome_topicv,valore_topicv,qos=qos_topicv,hostname=hostmariadb,auth={'username':nome_utentev,'password':password_utentev})
      cursor.close()
      cnx.close()
      cnx = connection.MySQLConnection(user=usermariadb,
                                    password=passwordmariadb,
                                    host=hostmariadb,
                                    database=databasemariadb)
      cursor=cnx.cursor()


def iddati(a):
    cursor.execute(" SELECT iddati FROM dati order by iddati desc limit 1")
    for row in cursor.fetchall():
        iddativ=row[0]
    return iddativ

def idvarimax(a):
    cursor.execute(" SELECT MAX(idtopic) FROM topic")
    for row in cursor.fetchall():
        idvarimaxv=row[0]
    return idvarimaxv


def creatore (topic1):
       topic3 = ("SELECT creatore  FROM  dati  WHERE dati.iddati =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            creatorev = row[0]
       return creatorev

def id_topic (topic1):
       topic3 = ("SELECT idtopic FROM  dati  WHERE dati.iddati =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            id_topicv = row[0]
       return id_topicv

def valore_topic (topic1):
       topic3 = ("SELECT valore_topic FROM  dati  WHERE dati.iddati =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            valore_topicv = row[0]
       return valore_topicv


def nome_topic (topic1):
       topic3 = ("SELECT nome_topic  FROM  topic  WHERE topic.idtopic =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            nome_topicv = row[0]
       return nome_topicv

def qos_topic (topic1):
       topic3 = ("SELECT qos  FROM  topic  WHERE topic.idtopic =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            qos_topicv = row[0]
       return qos_topicv


def idnodo_topic (topic1):
       topic3 = ("SELECT idnodo  FROM  topic  WHERE topic.idtopic =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            idnodo_topicv = row[0]
       return idnodo_topicv

def id_utente (topic1):
       topic3 = ("SELECT idutente  FROM nodi  WHERE nodi.idnodi =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            id_utentev = row[0]
       return id_utentev

def nome_utente (topic1):
       topic3 = ("SELECT username  FROM  utente  WHERE utente.idutente =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            nome_utentev = row[0]
       return nome_utentev


def password_utente (topic1):
       topic3 = ("SELECT password  FROM  utente  WHERE utente.idutente =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            password_utentev = row[0]
       return password_utentev


def idtipo_topic (topic1):
       topic3 = ("SELECT  idtipo_topic  FROM  topic  WHERE topic.idtopic =('%s')")
       cursor.execute(topic3 %(topic1))
       for row in cursor.fetchall() :
            idtipo_topicv = row[0]
       return int(idtipo_topicv)

def last_value_topic(id_topicv):
    last_value_topic_querry=("SELECT valore_topic  FROM  dati  WHERE  idtopic.dati=('%s') ORDER BY iddati DESC   LIMIT  1")
    cursor.execute(last_value_topic_querry %iddativ )
    for row in cursor.fetchall():
            last_value_topicv=row[0]
    return last_value_topicv





cursor=cnx.cursor()
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.username_pw_set(usernameadminmqtt, passwordadminmqtt)
mqttc.connect(hostmqtt,portamqtt, 60)
mqttc.subscribe("ora", 2)
mqttc.loop_forever()
