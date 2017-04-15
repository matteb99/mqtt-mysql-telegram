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
    cursor.execute("SELECT idutente FROM utente JOIN telegramuser ON utente.idtelegram = telegramuser.idtelegramuser WHERE iduser='"+id+"'")
    test01='idtelegram'
    for row in cursor.fetchall():
        test01=row[0]
    if(test01=='idtelegram'):
        message='non hai un account collegato a questo account telegram per collegare premere /login'
    else:
        message='hai già un account collegato a questo account telegram'
    return message


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
        text_message='benvenuto in @mqttclientbot \n' + text_message
    chat.send(text_message)
    disconnectmysql(cursor,cnx)




if __name__ == "__main__":
    bot.run()
