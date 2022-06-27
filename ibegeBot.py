import pyautogui as pt
from time import sleep
import pyperclip


from neuralintents import GenericAssistant
from cli_bot import function_for_greetings


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



# VARIAVEIS PARA PYAUTOGUI
sleep(5)
global x, y
# COMECA COM POSICAO EM CIMA DO SMILE
position = pt.locateOnScreen("./whatapp_pixels/smile.png", confidence=.6)
x = position[0]
y = position[1]

# PEGA A MENSAGEM RECEBIDA
def get_received_message():
  # ACHA O SMILE NA TELA
  position = pt.locateOnScreen("./whatapp_pixels/smile.png", confidence=.6)
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
  position = pt.locateOnScreen("./whatapp_pixels/smile.png", confidence=.6)
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
  assistant = initialize_and_train_model()
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
  while True:
    try:
      position = pt.locateOnScreen("./whatapp_pixels/unread.png", confidence = 0.7)
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