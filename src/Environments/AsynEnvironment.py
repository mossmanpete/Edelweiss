class AsynEnvironment:

    name = "Asynchronous Environment"

    def __init__(self, con):
        self.controller = con

    def get_n(self):
        return self.controller.n

    def get_f(self):
        return self.controller.f

    def get_tf(self):
        return self.controller.tf

    def get_round(self):
        return self.controller.round

    def get_id(self, sk):
        return self.controller.node_id[sk]

    def get_input(self, node):
        if type(self.controller.input) is list:
            return self.controller.input[node]
        else:
            return self.controller.input

    def get_input_msg(self, sk):
        return self.controller.get_message(sk)

    # def drain_message_buffer(self,sk):
    #     return self.controller.drain_message_buffer(sk)

    def put_broadcast(self, sk, id, msg):
        self.controller.put_broadcast(id, msg)
    
    def dispatch_message(self):
        self.controller.dispatch_message()

    def put_packet(self, sk, msg, target):
        self.controller.put_packet(msg, target)

    def put_output(self, sk, output):
        self.controller.put_output(sk, output)

    def check_corrupt(self, sk):
        return self.controller.is_corrupt(sk)

    def get_k(self):
        return self.controller.k
    
    def insert_block(self,block):
        return self.controller.insert_block(block)

