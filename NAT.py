import random
from gettext import translation


# устройство NAT которое умеет выполнять нужные преобразования
# у такого устройства должен быть свой ip для выхода в инет
# он доджен уметь генерировать порт
# Также он должен хранить таблицу с пришедшими ip и портом и замененный ip и порт

class NAT:
    def __init__(self, outer_ip):
        self.__outer_ip = outer_ip
        self.translation_table = []

    def add_translation(self, inner_ip, inner_port):
        outer_port = self.gen_free_port()
        self.translation_table.append([inner_ip, inner_port, self.__outer_ip, outer_port])
        print(self.translation_table)
        return (self.__outer_ip, outer_port)

    def gen_free_port(self):
        outer_port = random.randint(49152, 65535)
        if self.translation_table and any(outer_port == translation[3] for translation in self.translation_table):
            self.gen_free_port()
        else:
            return outer_port

    def handle_inner_packet(self, outer_ip, outer_port):
        for translation in self.translation_table:
           if (outer_ip == translation[2]) and (outer_port == translation[3]):
               return (translation[0], translation[1])
        return 'Чужое сообщение'

def simulate_NAT():
    devices = ['192.168.1.10', '192.168.1.20', '192.168.1.30']
    nat = NAT('10.10.10.10')

    sent_packages = []
    for device in devices:
        inner_port = random.randint(49152, 65535)
        print(f'Create message {device} - {inner_port}')
        out_package = nat.add_translation(device, inner_port)
        print(f'Send message {out_package}')
        sent_packages.append(out_package)

    for out_package in sent_packages:
        in_package = nat.handle_inner_packet(*out_package)
        print(f'Receive message {in_package}')

if __name__ == '__main__':
    simulate_NAT()
