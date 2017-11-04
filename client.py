import socket,threading
class ChatClient(object):
    def __init__(self):
        self.regudp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.chatudp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.reg_sevraddr = ('127.0.0.1',8787)

    def connect_reg(self):
        self.regudp.sendto(b'100',self.reg_sevraddr)
        while True:
            msg,addr = self.regudp.recvfrom(1024)
            if msg[:3] == b'140':

                self.myport = int(msg[3:].decode('utf-8'))
                self.regudp.close()
                self.chat_sevraddr = ('127.0.0.1',8788)
                self.connect_chat()

            if msg == b'110':

                self.name = input('看来老虎并不认识你，请输入你的名字：\n')
                self.regudp.sendto(('120%s'%self.name).encode('utf-8'),self.reg_sevraddr)
            if msg == b'130':

                self.regudp.sendto(b'100',self.reg_sevraddr)
    def connect_chat(self):
        print(self.myport)
        self.chatudp.bind(('',self.myport))
        self.chatudp.sendto(b'150',self.chat_sevraddr)
        while True:
            msg,addr = self.chatudp.recvfrom(1024)
            if msg == b'160':
                print('成功进入聊天室')
                t_enter = threading.Thread(target=self.enter_content)
                t_enter.start()

            else:
                print(msg.decode('utf-8'))

    def enter_content(self):
        while True:
            msg = input('输入：')
            if msg == 'quit!':
                return
            else:
                self.chatudp.sendto(msg.encode('utf-8'),self.chat_sevraddr)
if __name__ == '__main__':
    c = ChatClient()
    c.connect_reg()






