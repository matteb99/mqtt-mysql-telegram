import botogram
from mysql.connector import (connection)
import sys
import datetime
from config  import tokenbot,usermariadb, passwordmariadb, hostmariadb, databasemariadb
bot = botogram.create(tokenbot)
bot.owner = "@matteob99"
def disconnectmysql(cursor,cnx):
    emp_no = cursor.lastrowid
    cnx.commit()
    cursor.close()
    cnx.close()

def connectmysql():
    cnx = connection.MySQLConnection(user=usermariadb,
                                  password=passwordmariadb,
                                  host=hostmariadb,
                                  database=databasemariadb)
    cursor=cnx.cursor()
    return cursor, cnx

def checkuser(cursor,id):
    cursor.execute("SELECT idutente FROM utente JOIN telegramuser ON utente.idtelegram = telegramuser.idtelegramuser WHERE iduser='"+str(id)+"'")
    test01='idtelegram'
    for row in cursor.fetchall():
        test01=row[0]
    if(test01=='idtelegram'):
        message='non hai un account collegato a questo account telegram per collegare premere /login'
    else:
        message='hai già un account collegato a questo account telegram'
    return message

def idutente(cursor,id):
    querry="SELECT idutente FROM utente JOIN telegramuser ON utente.idtelegram = telegramuser.idtelegramuser WHERE iduser='"+str(id)+"'"
    cursor.execute(querry)
    for row in cursor.fetchall():
        idutentev=row[0]
    return idutentev


@bot.process_message


@bot.command('listtopic')
def listtopic_command(chat, message,args):
    sender = message.sender
    cursor, cnx = connectmysql()
    cursor.execute("SELECT nome_topic FROM utente JOIN  nodi on utente.idutente = nodi.idutente LEFT JOIN topic ON nodi.idnodi = topic.idnodo LEFT JOIN telegramuser ON utente.idtelegram = telegramuser.idtelegramuser WHERE iduser='"+str(sender.id)+"'")
    text_message = ''
    rows = cursor.fetchall()
    for row in rows:
        text_message += '\n' + str(row[0])
    if(text_message==' '):
            text_message= checkuser(cursor,sender.id)
            if(text_message=='hai già un account collegato a questo account telegram'):
                text_message='non hai nessun topic per crearne premere /creatopic'

    chat.send(text_message,syntax="HTML")
    disconnectmysql(cursor,cnx)
@bot.command('listtipotopic')
def listtipotopic_command(chat,message,args):
    cursor, cnx = connectmysql()
    cursor.execute("SELECT * FROM tipo_topic ")
    text_message=""
    for row in cursor.fetchall():
        text_message+='\n'+str(row[1])+"\t: "+str(row[2])
    disconnectmysql(cursor,cnx)
    chat.send(text_message,syntax="HTML")

@bot.command('listtiponodi')
def listtiponodi_command(chat,message,args):
    cursor, cnx = connectmysql()
    cursor.execute("SELECT nome_tipo_nodo FROM tipo_nodo ")
    text_message=""
    for row in cursor.fetchall():
        text_message+='\n'+str(row[0])
    chat.send(text_message,syntax="HTML")
    disconnectmysql(cursor,cnx)

@bot.command('creatopic')
def creatopic_command(chat,message,args):
    sender=message.sender
    cursor, cnx = connectmysql()
    if str(message.text)=="/creatopic":
        text_message="invia il nome del topic  con questa sintassi <strong> /creatopic  nometopic:nodo:tipotopic </strong>  <b> importante un solo spazio </b>"
    else:
        nometopic,nodo,tipotopic=message.text[11:].split(':')
        if "/" or '@' or '#' not in nometopic:
            idutentev=idutente(cursor,sender.id)
            nometopic=str(idutentev)+"/"+str(nometopic)
            querry="SELECT idnodi FROM nodi JOIN tipo_nodo ON nodi.idtipo_nodo = tipo_nodo.idtipo_nodo WHERE idutente='"+str(idutentev)+"' AND nome_tipo_nodo='"+str(nodo)+"'"
            cursor.execute(querry)
            idnodo=" "
            for row in cursor.fetchall():
                idnodo=str(row[0])
            if(idnodo != ' '):
                querry="SELECT idtipo_topic FROM tipo_topic WHERE tipo_tipo='"+str(tipotopic)+"'"
                idtipotopic=' '
                cursor.execute(querry)
                for row in cursor.fetchall():
                    idtipotopic=row[0]
                if(idtipotopic != ' '):
                    querry="INSERT INTO topic (nome_topic,idnodo,idtipo_topic) VALUES ('"+str(nometopic)+"','"+str(idnodo)+"','"+str(idtipotopic)+"')"
                    cursor.execute(querry)
                    text_message="topic creato con successo "+nometopic+" nel nodo "+nodo+" di tipo "+tipotopic
                else:
                    text_message="tipo di topic inesistente per vedere una lista di tipo topic /tipotopic"
            else:
                text_message="nodo inesistente per creare un nodo /creanodo"
        else:
            text_message="nel nome del topic non ci devono essere caratteri speciali (/,@,#,)"
    chat.send(str(text_message),syntax="HTML")
    disconnectmysql(cursor,cnx)

@bot.command('creanodo')
def creanodo_command(chat,message,args):
    sender=message.sender
    cursor, cnx = connectmysql()
    if str(message.text)=="/creanodo":
        tiponodo='server'
    else:
        tiponodo=str(message.text[10:])
    querry="SELECT COUNT(idtipo_nodo) FROM tipo_nodo"
    cursor.execute(querry)
    for row in cursor.fetchall():
        numberrow=row[0]
    querry="SELECT nome_tipo_nodo FROM tipo_nodo"
    control01=0
    control02=0
    cursor.execute(querry)
    for row in cursor.fetchall():
        if(str(tiponodo)==str(row[0])):
            control01=1
        elif(control02==numberrow-1):
            control01=2
        control02+=1

    if (control01==1):
        querry="SELECT idtipo_nodo FROM tipo_nodo WHERE nome_tipo_nodo='"+tiponodo+"'"
        cursor.execute(querry)
        for row in cursor.fetchall():
            idtiponodo=row[0]
        idutentev=idutente(cursor,sender.id)
        querry="INSERT INTO nodi (idutente, idtipo_nodo) VALUES ('"+str(idutentev)+"', '"+str(idtiponodo)+"')"
        cursor.execute(querry)
        querry="SELECT idnodi from nodi WHERE idutente='"+str(idutentev)+"' AND idtipo_nodo='"+str(idtiponodo)+"'"
        cursor.execute(querry)
        for row in cursor.fetchall():
            control02=1
        if(control02==1):
            text_message="nodo creato con succeso il tipo di nodo è "+str(tiponodo)
    elif(control01==2):
        text_message="non è stato possibile creare il nodo perchè il tipo di nodo non esiste"
    else:
        text_message="errore generale per favore contatta il creatore del bot @matteob99"
    chat.send(str(text_message),syntax="HTML")
    disconnectmysql(cursor,cnx)

@bot.command('login')
def login_command(chat,message,args):
    sender = message.sender
    cursor, cnx = connectmysql()
    #inserire controllo login già effettuato
    if str(message.text)=="/login":
        text_message="invia l'username e la password con questa sintassi <strong> /login username:password </strong> <b> importante un solo spazio </b>"
    else:
        usertest,passwordtest=message.text[7:].split(':')
        querry="SELECT * FROM utente WHERE username='"+usertest+"' AND password='"+passwordtest+"'"
        control01=0
        cursor.execute(querry)
        for row in cursor.fetchall():
            control01=1
            idutente=row[0]
        if(control01==0):
            querry="SELECT * FROM utente WHERE username='"+usertest+"'"
            control02=0
            cursor.execute(querry)
            for row in cursor.fetchall():
                control02=1
            if(control02==1):
                text_message="<b>password</b> errata"
            else:
                text_message="<b>username inesistente </b>"
        else:
            querry="SELECT idtelegramuser FROM telegramuser WHERE iduser='"+str(sender.id)+"'"
            cursor.execute(querry)
            for row in cursor.fetchall():
                idtelegramuser=row[0]
            querry="UPDATE utente SET idtelegram='"+str(idtelegramuser)+"' WHERE idutente='"+str(idutente)+"'"
            cursor.execute(querry)
            text_message="login effettuato con successo"
    chat.send(str(text_message),syntax="HTML")
    disconnectmysql(cursor,cnx)

@bot.command('start')
def start_command(chat,message,args):
    sender = message.sender
    cursor, cnx = connectmysql()
    cursor.execute("SELECT iduser FROM telegramuser WHERE iduser='"+str(sender.id)+"'")
    idsender=' '
    for row in cursor.fetchall():
        idsender=row[0]

    if (str(sender.id)==str(idsender)):
        text_message="ti sei già insritto a questo bot \n"+checkuser(cursor,sender.id)
    elif(idsender==' '):
        cursor.execute('SELECT MAX(idtelegramuser) FROM telegramuser')
        for row in cursor.fetchall():
            idtelegram=1+row[0]
        dati=(str(idtelegram),str(sender.id))
        cursor.execute("INSERT INTO telegramuser (idtelegramuser,iduser,posizione) VALUES (%s,%s,'0');",dati)

        text_message= checkuser(cursor,sender.id)
        text_message='benvenuto in @mqttclientbot per i vari comandi /help \n' + text_message
    else:
        text_message="errore generale contattare @matteob99"
    chat.send(text_message,syntax="HTML")
    disconnectmysql(cursor,cnx)

if __name__ == "__main__":
    bot.run()
