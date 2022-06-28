from neuralintents import GenericAssistant
import time
import random

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


def initialize_and_return_trained_model():
    # mappings = {'saudacoes': function_for_greetings} //intent_methods=mappings,
    mappings = {'saudacoes': function_for_greetings}

    assistant = GenericAssistant('intents.json', intent_methods=mappings, model_name="ibegeBotModel")
    assistant.train_model()
    assistant.save_model()
    return assistant



assistant = initialize_and_return_trained_model()

def init_cli_bot(assistant):
    while True:
        message = input("Enter a message: ")
        if message == "STOP":
            False
        else:
            if 'populaçao' in message.lower():
                msg = message.lower().replace('populaçao', 'populacao')
                print(msg)
                print('resposta: \n', assistant.request(msg))
            elif 'população' in message.lower():
                msg = message.lower().replace('população', 'populacao')
                print(msg)
                print('resposta: \n', assistant.request(msg))
            else:
                print('resposta: \n', assistant.request(message))

init_cli_bot(assistant)