import botogram
from mysql.connector import (connection)
import sys
import datetime
from config  import tokenbot,usermariadb, passwordmariadb, hostmariadb, databasemariadb
bot = botogram.create(tokenbot)

def disconnectmysql(cursor,cnx):
    cursor.close()
    cnx.close()

@bot.process_message
@bot.command("hello")
def hello_command(chat, message, args):
    """Say hello to the world!"""
    chat.send("Hello world"+str(message)+str(args)+str(chat))
    print("Helloworld"+str(message)+str(args)+str(chat))

@bot.command("test01")
def test01_command(chat, message, args):
    cnx = connection.MySQLConnection(user=usermariadb,
                                  password=passwordmariadb,
                                  host=hostmariadb,
                                  database=databasemariadb)
    cursor=cnx.cursor()
    cursor.execute(" SELECT * FROM dati order by iddati desc limit 1")
    for row in cursor.fetchall():
        iddativ=row[0]
        chat.send(str(iddativ))
#"NewAccount",  "NewNodo", "NewVariabile","TipoNodo","TipoVariabile","ListVariabileUtente","ListNodoUtente","ListSceneUtente","ListTriggerSceneUtente", "StampDatoTimeLast","StampDatoTimeCron","StampDatoRange","NewScena");

    cursor.close()
    cnx.close()

@bot.command('listtopic')
def listtopic_command(chat, message,args):
    cnx = connection.MySQLConnection(user=usermariadb,
                                      password=passwordmariadb,
                                      host=hostmariadb,
                                      database=databasemariadb)
    cursor=cnx.cursor()
    cursor.execute("SELECT nome_topic FROM utente JOIN  nodi on utente.idutente = nodi.idutente LEFT JOIN topic ON nodi.idnodi = topic.idnodo ;")
    iddativ=' '
    for row in cursor.fetchall():
        iddativ=(
#                str(iddativ)
#                str(row[0])
#                str('  ')
#                )
         testo_messaggio = ( # In caso di messaggi complessi, consiglio sempre di utilizzare una variabile per comporre il testo, e in seguito inviare il messaggio
          "<b>Informazioni su di te" # Il Markdown e l'HTML sono ovviamente supportati, consiglio di utilizzare fin da subito l'HTML. Botogram riconosce automaticamente HTML e Markdown
         "<b>Nome</b>: {nome}" # Per andare a capo basta utilizzare
         "<b>Username</b>: @{username}" # L'username fornito da Telegram è senza @ (e commerciale)
         "<b>ID</b>: {id}"
         "<b".format(nome=sender_name, username=sender_username, id=sender_id)
    chat.send(str(iddativ),syntax="HTML")
    disconnectmysql(cursor,cnx)
@bot.command("me")
 2 def me(chat, message, args):
     sender = message.sender # Sender è l'oggetto che identifica colui che sta inviando il messaggio
     sender_name = sender.name
     sender_username = sender.username
     sender_id = sender.id
     testo_messaggio = (
         "<b>Informazioni su di te" # Il Markdown e l'HTML sono ovviamente supportati, consiglio di utilizzare fin da subito l'HTML. Botogram riconosce automaticamente HTML e Markdown
         "<b>Nome</b>: {nome}" # Per andare a capo basta utilizzare
         "<b>Username</b>: @{username}" # L'username fornito da Telegram è senza @ (e commerciale)
         "<b>ID</b>: {id}".format(nome=sender_name, username=sender_username, id=sender_id)
         )
     chat.send(testo_messaggio, syntax="HTML")

if __name__ == "__main__":
    bot.run()
