import socket
import threading
import random



#PORT=45853
PORT=18153
SERVER="8.tcp.ngrok.io"
#SERVER="192.168.1.79"
HEADER=8
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECT"
USERNAME="USERNAME"
MESSAGE="MSG"
ERROR="EMPTY_MSG"
ADDR=(SERVER,PORT)


def lenMsg(msg): # Longitud de cualquier mensaje a enviar con .send() codificado en 'utf-8'
  
    msg_length = len(msg.encode(FORMAT))
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length

#conexion con el servior
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
username=input("Username <---: ")

client.send(lenMsg(USERNAME))
client.send(USERNAME.encode(FORMAT))
client.send(lenMsg(username))
client.send(username.encode(FORMAT))


def recvMensaje():# funcion que se mantiene en espera de cualquier mensaje del servidor
  while(True):
    msg=client.recv(HEADER)
    msg=msg.decode(FORMAT)
    if msg:
        msg_len=int(msg)
        msg=client.recv(msg_len).decode(FORMAT)

        if(msg==MESSAGE): #Si se recibio el mensaje entonces procede a recibir el largo y el contenido del mensaje
                        
            try:                
                msg=client.recv(HEADER)#Largo del mensaje(cantidad de bytes)
                msg=msg.decode(FORMAT)

                if(msg):
                    msg_len=int(msg)
                    msg=client.recv(msg_len).decode(FORMAT) #recibe unicamente la cantidad exacta de bytes del mensaje
                
                print("\r"+msg)
                print("--->",end='',flush=True)
            except:
                print(f"[ERROR] {client}")
            
                
                

def enviarMensaje(): #Funcion de envio de mensajes, esta se mantiene en paralelo con la de escucha para no esperar si no se envia nada o si no se escucha nada del servidor
    estado=True
    while(estado):
        outMsg=input("--->")    

        if(outMsg=="exit()"): # ingresar "exit()" para desconectarse del servidor y dejar libre el socket
            print("Desconectando......")
            client.send(lenMsg(DISCONNECT_MESSAGE))
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))            
            estado=False

        elif(outMsg):# El protocolo de intercambio de datos es primero enviar la longitud de los datos(cantidad de bytes) y luego la etiqueta especial para cada tipo de datos, luego mandar la longitud
            #del contenido de los datos y por ultimo enviar el contenido.
            client.send(lenMsg(MESSAGE))
            client.send(MESSAGE.encode(FORMAT))
            client.send(lenMsg(outMsg))
            client.send(outMsg.encode(FORMAT))
        
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    


threadRecv=threading.Thread(target=recvMensaje)
threadRecv.daemon=True
threadRecv.start()


enviarMensaje()