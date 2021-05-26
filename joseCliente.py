import platform,select, string, sys, os, base64, fcntl, struct, hashlib, socket, time

#---------------------------------------------------------------------------------------------------
#   Aqui Se desarrollan las Distintas llamadas del servidor 

def GetClienteVpnIP(nombre):
    s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s',nombre[:15].encode('utf-8'))
    )[20:24])

#   Se Desarrollan las diferentes llamadas por los comandos
#
    #helloiam
def GetHelloiam(servidorSockets,userName):
    userRegistrarse=("helloiam "+userName)
    servidorSockets.send(userRegistrarse.encode("utf-8"))
    buffer=servidorSockets.recv(1000)
    return buffer.decode();

    #msglen
def GetMsglen(servidorSockets):
    servidorSockets.send("msglen".encode())
    buffer=servidorSockets.recv(1000)
    respuesta= buffer.decode()[0:3]
    tamano=buffer.decode()[3:8]
    return respuesta, tamano

    #givememsg
def GetGivememsg(servidorSockets,puerto):
    comando=("givememsg "+str(puerto))
    servidorSockets.send(comando.encode())
    buffer=servidorSockets.recv(1000)
    return buffer

def GetMensaje(clienteSocket,servidorSockets):
    data, addr =clienteSocket.recvfrom(1000)
    msglen1=base64.b64decode(data)
    msglen2=hashlib.md5(msglen1)
    return msglen1, msglen2 ,data.decode()


def GetChkmsg(msglen2,servidorSockets):
    msglen2=("chkmsg "+msglen2.hexdigest())
    contador = 0
    while contador<=3:
        servidorSockets.send(msglen2.encode())
        servidorSockets.settimeout(1) 
        buffer=servidorSockets.recv(1024)
        if buffer=="ok":
            return buffer.decode()
        elif contador==4: 
            return buffer.decode()
        else:
            contador=contador+1
    return "tiempo agotado, intentos realizados :",contador

def Despidete(servidorSockets):
    contador =0
    while contador <=3:
        servidorSockets.send("bye".encode())
        servidorSockets.settimeout(1)
        buffer=servidorSockets.recv(1024)
        if buffer == "ok": 
            return buffer.decode()
        else:
            contador= contador + 1 
    return "tiempo agotado, intentos realizados :",contador   
            

#-------------------------------------------------------------------------------------------

#   Estas son las funciones que ese ejecutan las diferentes 
#   manera para que el usuario pueda leer los detalles o no 

def GetInfoDetallada(servidorSockets,clienteSocket,userName,puerto):
    
    print("helloiam",userName," Respuesta del servidor :", GetHelloiam(servidorSockets,userName))
    respuesta, tamano=GetMsglen(servidorSockets)
    print("msglen Respuesta del servidor : ",respuesta ,"/","Tamano del mensaje :",tamano)
    print('givememsg respuesta del servidor :',GetGivememsg(servidorSockets,puerto).decode())
    msglen1, msglen2, data=GetMensaje(clienteSocket,servidorSockets)
    print("_______________________________________________________________")
    print("mensaje recibido Codificado :\n" , data)
    print("_______________________________________________________________")
    print(" mensaje decodificado :\n",msglen1)
    print("_______________________________________________________________")
    print("mensaje a checkear\n")
    print("chkmsg "+msglen2.hexdigest(),"\n")
    print("chkmsg - check :",GetChkmsg(msglen2,servidorSockets))
    print("\n_______________________________________________________________")
    print("bye respuesta del servidor :",Despidete(servidorSockets))
    

def GetInfoNoDetallada(servidorSockets,clienteSocket,userName,puerto):
        helloiam=GetHelloiam(servidorSockets,userName)
        givememsg=GetGivememsg(servidorSockets,puerto).decode()
        msglen1, msglen2, data=GetMensaje(clienteSocket,servidorSockets)
        bye=Despidete(servidorSockets)
        print("el mensaje es : \n\n",msglen1)
#---------------------------------------------------------------------------------------------------------------------    


def main():
    #
    #   Inicio de El programa
    #
    print('-----------------------------------------')
    print(' Bienvenido A la actividad Conexion')
    print(' Desarrollada por jose Gonzalez ')    
    print('-----------------------------------------\n')

    entradaConsola= input('\n1-Vpn Determinado\n2-Conexion Local\n3-Vpn Opcional\n\nintrodusca opcion :')
    if entradaConsola == '2':
        servidorIp ="127.0.0.1"
        clienteIP ="127.0.0.1"
        puerto=19876
    elif entradaConsola =='1':
        servidorIp ="10.2.126.2"
        clienteIP = GetClienteVpnIP("tun0")
        puerto=19876
    elif entradaConsola=='3':
        #servidorIp =input(" Introduce la ip del servidor que te quieres conectar:")
        #puerto=input(" Introduce el protocolo que te quieres conectar:")
        #clienteIP = GetClienteVpnIP("tun0")
        print("no lo desarrolle porque no tenia con quien probar esto")
    else:
        print('lo hiciste mal')

    servidorSockets= socket.socket()## socket TPC
    clienteSocket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)# sockedudp


    try:
        servidorSockets.connect((servidorIp,puerto))
        clienteSocket.bind((clienteIP,puerto))
        
    except:
        print("No se puede establer conexion con el Servidor\nCerrando...")    
        sys.exit()

    print("\n IP direccion Cliente : ", clienteIP)
    print(" IP del servidor : ", servidorIp)
    print(" Puerto de conexion : ", puerto)
    print("___________________________________________")
    userName = input(" Por favor Introduce tu usuario ucab :")
    print("___________________________________________\n\n")
    os.system("clear")
    print("_____________________________________________")
    print("| ingresaste con el usuario :", userName,"|")
    print("|___________________________________________|")
    print("|Estatus de conexion : Exitoso              |")
    print("|___________________________________________|")

    entradaConsola= input('\n1- Ver mensaje \n2- Mensjae con detalles de conexiones \n\n introdusca opcion :')
    os.system("clear")

    if entradaConsola =='2':
        #ejecutamos las funciones
        GetInfoDetallada(servidorSockets,clienteSocket,userName,puerto)
    elif entradaConsola =='1':
        #ejecutamos las funciones
        GetInfoNoDetallada(servidorSockets,clienteSocket,userName,puerto)
    else:
        print("no seleccionaste la opcion correcta")    
    
while True:
    main()
    if input("\n Desea repetir ? (Y/N)").strip().upper() !='Y':
        break