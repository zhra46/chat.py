import socket,time,random,msg,threading
'''100:客户端要求注册
   110:服务端要求发送姓名
   120+name:向服务端注册姓名
   130：服务端注册成功，要求客户端重新连接
   140+端口号：服务端通知客户端聊天室通信端口
   150：客户端告知服务端加入聊天室
   160：服务端提示客户端成功加入并通知全体，可以开始聊天
'''
class ChatRoom(object):
    def __init__(self):
        self.nameDict={}
        self.reg_Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.chat_Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.reg_Socket.bind(('',8787))
        self.chat_Socket.bind(('',8788))
        print('老虎聊天室已经启动，等待连接....')
    def reg(self):
        while True:
            msg,addr = self.reg_Socket.recvfrom(1024)
            if msg == b'100':
                print('get100')
                if addr in self.nameDict:
                    cport = addr[1]
                    smsg = '140%s'%cport
                    self.reg_Socket.sendto(smsg.encode('utf-8'),addr)
                else:
                    self.reg_Socket.sendto(b'110',addr)
            if msg[:3] == b'120':
                print('get120')
                name = msg[3:].decode('utf-8')
                self.nameDict[addr] = name
                self.reg_Socket.sendto(b'130',addr)
    def chatEcho(self):
        while True:
            msg,addr = self.chat_Socket.recvfrom(1024)
            if msg == b'150':
                print('get150')
                self.broadcast('[系统提示]%s 加入了聊天室'%self.nameDict[addr])
                self.chat_Socket.sendto(b'160',addr)
            else:
                name = self.nameDict[addr]
                self.broadcast(name+':'+msg.decode('utf-8'))


    def broadcast(self,msg):
        print('broad cast'+msg)
        for addr in self.nameDict:
            print(addr)
            self.chat_Socket.sendto(msg.encode('utf-8'),addr)

if __name__=='__main__':
    chatRoom = ChatRoom()
    t_reg = threading.Thread(target=chatRoom.reg)
    t_chat = threading.Thread(target = chatRoom.chatEcho)
    t_reg.start()
    t_chat.start()