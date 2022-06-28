import pyautogui as pt
from time import sleep
import random
import pyperclip
import threading
import time
import keyboard

from neuralintents import GenericAssistant

event = threading.Event()

def stop():
    event.set()
    print("stopped")

keyboard.add_hotkey("ctrl+f1", stop)


# RETORNA MENSAGEM BASEDA NO TEMPO, RECEBE SAUDAÇAO PARA O PERIODO COMO PARAMETRO
def return_msg_based_on_time(period):
    random_choice = random.randrange(0, 3, 1)
    messages = [
        "em que posso ajudar??",
        "em que posso ajuda-lo??",
        "em que posso ser util a voce??",
        "como posso ser util a voce"
    ]

    fullMessage = f'{period}, {messages[random_choice]}'
    return fullMessage


## RESPONDER SAUDAÇAO DE ACORDO COM HORARIO DO DIA
def function_for_greetings(message, response):

    print(f'MSG RECEBIDA: {message} -- TAG/IDENTIFICADOR: SAUDAÇÃO')
    actual_hour = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()).split()[1][0:2]
    actual_hour = int(actual_hour)
    if(actual_hour >= 0 and actual_hour <= 5):
        return_message = return_msg_based_on_time('Boa Madrugada')
    elif(actual_hour >= 6 and actual_hour <  12):
        return_message = return_msg_based_on_time('Bom Dia')
    elif(actual_hour >= 12 and actual_hour < 18):
        return_message = return_msg_based_on_time('Boa Tarde')
    elif(actual_hour >= 18 and actual_hour <= 23):
        return_message = return_msg_based_on_time('Boa Noite')
    else:
        return response
    return return_message

def initialize_and_train_model():
  # MAPEAMENTO DAS FUNCOES PARA TAGS/IDENTIFICADORES
  mappings = {'saudacoes': function_for_greetings}

  # INICIA A ASSISTENTE, PASSANDO DADOS DE TREINAMENTO, METODOS PARA OS DADOS CLASSIFICADOS, E NOME PARA O MODELO
  assistant = GenericAssistant('intents.json', intent_methods=mappings, model_name="ibegeBotModel")
  # INICIA TREINO DE MODELO
  assistant.train_model()
  # SALVA O MODELO
  assistant.save_model()
  return assistant

assistant = initialize_and_train_model()


# VARIAVEIS PARA PYAUTOGUI
sleep(5)
global x, y
# COMECA COM POSICAO EM CIMA DO SMILE
position = pt.locateOnScreen("whatsapp_pixels/smile.png", confidence=.6)
x = position[0]
y = position[1]

# PEGA A MENSAGEM RECEBIDA
def get_received_message():
  # ACHA O SMILE NA TELA
  position = pt.locateOnScreen("whatsapp_pixels/smile.png", confidence=.6)
  # DEFINE X,Y ATRAVES DA POSICAO DO SMILE
  x = position[0]
  y = position[1]
  #MOVE PARA A MENSAGEM
  pt.moveTo(x+100, y-45, duration=0.5)
  # DA UM CLIQUE TRIPLO NA MENSAGEM
  pt.tripleClick()
  # DA UM CLIQUE DIREITO NA MENSAGEM
  pt.rightClick()
  # MOVE O MOUSE PARA A OPÇAO DE COPIAR
  pt.moveRel(100, -280)
  # CLICA, COPIANDO O TEXTO DA MENSAGEM
  pt.click()
  # SETA RECEIVED_MESSAGE COM TEXTO COPIADO
  received_message = pyperclip.paste()
  print(f'Received Message: {received_message}')
  # RETORNA O TEXTO DA MENSAGEM
  return received_message

# ENVIADO MENSAGEM
def send_message(message):
  # ACHA O SMILE NA TELA
  position = pt.locateOnScreen("whatsapp_pixels/smile.png", confidence=.6)
  # DEFINE X,Y ATRAVES DA POSICAO DO SMILE
  x = position[0]
  y = position[1]
  # MOVE O MOUSE PARA O INPUT QUE ENVIA MENSAGENS
  pt.moveTo(x+160, y+20, duration=0.5)
  # CLICA NO INPUT
  pt.click()
  # ESCREVE A MENSAGEM
  pt.typewrite(message, interval = 0.01)
  # MANDA A MENSAGEM COM ENTER
  pt.typewrite("\n", interval = 0.01)

def process_response(message):
  # INICIA O MODELO, E TREINA, RETORNANDO MODELO TREINADO
  # VERIFICA SE É POPULAÇAO OU POPULAÇÃO E TRANSFORMA EM POPULACAO
  # DEPOIS CHAMA O ASSISTENT COM A MENSAGEM COMO PARAMETRO
  # RECEBENDO O VALOR DE RESPOSTA EQUIVALENTE
  # ENVIA A RESPOSTA MASTIGADA
  if 'população' in message.lower():
    msg = message.lower().replace('população', 'populacao')
    print(msg)
    return assistant.request(msg)
  elif 'populaçao' in message.lower():
    msg = message.lower().replace('populaçao', 'populacao')
    return assistant.request(msg)
  else: return assistant.request(message)



def check_for_unread_messages():
  while not event.is_set():
    try:
      position = pt.locateOnScreen("whatsapp_pixels/unread.png", confidence = 0.7)
      if position is not None:
        pt.moveTo(position)
        pt.moveRel(-100,0)
        pt.click()
        sleep(1)
    except(Exception):
      print("No new messages")
    if pt.pixelMatchesColor(int(x+100), int (y-35), (32, 44, 51), tolerance = 10):
      print("is_white - new message")
      received_message = get_received_message()
      message_to_send = process_response(received_message)
      send_message(message_to_send)

    else:
      print("no new message")





check_for_unread_messages()