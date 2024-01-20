import telebot
from telebot.types import Message
import re
import time
import threading
import random
import schedule

from keep_alive import keep_alive

BOT_TOKEN = '6735522008:AAGdECJSZkelv5wKzd6qEF5jIb33E_Mdt3g'
CANAL_USERNAME = 'SharClub702'  # Remplacez par le nom d'utilisateur du canal
CANAL_ID = -1002072366730
GROUPE_ALEA = -1002050969919

# Créez une instance de bot
bot = telebot.TeleBot(BOT_TOKEN)

# Gérez la commande /start
@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    command_text = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else ''  # Extraire le texte après /start

    # Utiliser une expression régulière pour extraire l'identifiant du message
    match = re.match(r'^(\d+)$', command_text)

    if match:
        message_id = int(match.group(1))

        # Envoyer 10 documents en utilisant les liens extraits
        for i in range(650):
            # Construire le lien
            message_link = f"https://t.me/{CANAL_USERNAME}/{message_id + i}"

            try:
                # Vérifier si le message transféré est une photo ou un document
                sent_message = None
                
                sent_message = bot.send_document(chat_id, message_link)
                sent_message = bot.send_document(CANAL_ID, message_link)
               

                if sent_message.sticker:
                    continue
                else:
                    time.sleep(50)

            except telebot.apihelper.ApiException:
                continue
    else:
        # En cas de commande mal formée
        bot.send_message(chat_id, "Commande mal formée. Utilisez /start avec le format : /start=identifiant_message")


def send_random_message():
    random_messages = [
        "#Message aléatoire 1",
        "#Message aléatoire 2",
        "#Message aléatoire 3",
        # Ajoutez autant de messages aléatoires que nécessaire
    ]
    
    random_message = random.choice(random_messages)
    bot.send_message(GROUPE_ALEA, random_message)

# Planifie l'envoi du message aléatoire toutes les 4 minutes
schedule.every(50).seconds.do(send_random_message)

# Fonction pour exécuter périodiquement les tâches planifiées
def run_periodic_tasks():
    while True:
        schedule.run_pending()
        time.sleep(2)
        
# Démarrer la tâche périodique dans un thread en arrière-plan
threading.Thread(target=run_periodic_tasks, daemon=True).start()

# Exécutez le bot
keep_alive()
if __name__ == '__main__':
    bot.polling()
