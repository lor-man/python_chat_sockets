import socket
import threading


PORT=45853
#SERVER=socket.gethostbyname(socket.gethostname())
SERVER="127.0.0.1"
ADDR=(SERVER,PORT)
FORMAT='utf-8'
DISCONNECT_MESSAGE="DISCONNECT"
USERNAME="USERNAME"
MESSAGE="MSG"
HEADER=8


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

clients=[]

def lenMsg(msg):
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length

def clienteMensaje(msg,connection,username):
    #print(clients)
    for client in clients:
        if(client!=connection):
            try:      
                #print(username+msg)
                msgSend=username+msg #msgSend="["+str(username)+"]:"+msg
                client.send(lenMsg(MESSAGE.encode(FORMAT)))    
                client.send(MESSAGE.encode(FORMAT))
                client.send(lenMsg(msgSend.encode(FORMAT)))
                client.send(msgSend.encode(FORMAT))
            except:
                clients.remove(client)
                client.close()

def manejoCliente(conn,addr):
    print(f"[new connection] {addr} connected.")
    username=""
    userRegister=False
    messageIn=False
    connected= True
    while(connected):
    
        msg_length=conn.recv(HEADER)    
        
        msg_length=msg_length.decode(FORMAT)
    
        if msg_length:
            msg_length=int(msg_length)
            
            msg=conn.recv(msg_length).decode(FORMAT)
            
            if(userRegister): #Registra al usuario con un nombre de usuario
                userRegister=False
                username="["+msg+"]"              

            if (messageIn):#Muestra el mensaje

                clienteMensaje(msg,conn,username)
                messageIn=False

            if (msg==USERNAME): #El siguiente mensaje indica que sera el apodo escogido por el cliente
                userRegister=True
            
            if(msg==DISCONNECT_MESSAGE):
                connected=False
                clienteMensaje("Desconectado",conn,username)

            if (msg==MESSAGE):                
                messageIn=True

            print(f"[{addr}] Recibido")
        
    clients.remove(conn)  
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)        
        thread = threading.Thread(target=manejoCliente, args=(conn, addr))
        thread.daemon=True
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()