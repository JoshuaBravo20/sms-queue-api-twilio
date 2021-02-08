import os
from twilio.rest import Client

class Queue: # CLASE PRINCIPAL

    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID'] # DEFINIR SID
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN'] # DEFINIR AUTH TOKEN
        self.client = Client(self.account_sid, self.auth_token) # CREAR INSTANCIA DE CLIENTE
        self._queue = [] # DEFINIR FILA
        self._mode = 'FIFO' # MODO POR DEFECTO

    def enqueue(self, item): # METER EN FILA

        self._queue.append(item) # INGRESAR A FILA

        message = self.client.messages.create(
         body='Hi, ' + str(item['name']) + ', there are ' + str(self.size()) + " people ahead of you",
         from_='+19713154952',
         to='+56930734399'
        ) # MANDAR SMS

        return message.sid # RETORNAR

    def dequeue(self): # SACAR DE FILA
        if self.size() > 0:
            if self._mode == 'FIFO': # SI ES FIFO, ELIMINAR EL ULTIMO
                deQ = self._queue.pop()
                return deQ
            elif self._mode == 'LIFO': # SI ES LIFO, ELIMIAR EL PRIMERO
                deQ = self._queue.pop(0)
                return deQ
        else:
            return 'no one in line...'

    def get_queue(self): # RETORNAR FILA COMPLETA
        return self._queue

    def size(self): # RETORNAR TAMANO DE FILA
        return len(self._queue)