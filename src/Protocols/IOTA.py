import random
import sys
from Messages.Message import Message
from Util.Util import *
from Util.Tangle import *
# import matplotlib.pyplot as plt



class IOTA:
    name = "IOTA Protocol"

    def __init__(self, **kargs):

        self.env = kargs["env"]
        self.pki = kargs["pki"]
        self.pki.register(self)
        self.input = None
        self.Tangle = Tangle.init_with_fork(self.env.get_seed())
        self.belief = 0
        self.plotdata=[]
        self.running_rounds=self.env.controller.running_rounds
        self.mine = kargs["IOTAMine"]

    def run_node(self):
        round = self.env.get_round()
        if round > self.running_rounds:
            return
        if round == self.running_rounds:
            self.env.put_output(self, self.plotdata)
            return
        myid = self.env.get_id(self)
        msgs = self.env.get_input_msgs(self)
        for msg in msgs:
            if (not self.pki.verify(msg)):
                raise RuntimeError
            if msg.sender == myid:
                continue
            new_site = msg.get_extraction().copy()
            if not new_site:
                raise RuntimeError
            self.Tangle.insert_site(new_site)
        my_pow = self.mine.POW(round,myid)
        if my_pow:
            selected_tips=self.Tangle.random_walk()
            if selected_tips[0].vote!=selected_tips[1].vote:
                raise RuntimeError
            if selected_tips[0]==selected_tips[1]:
                del selected_tips[1]
            father_id_list = []
            father_list = []
            for tip in selected_tips:
                father_id_list.append(tip.id)
            for tip in selected_tips:
                father_list.append(tip)
            new_site = self.pki.sign(
                self, Tangle_Site(father_id_list, [], myid, selected_tips[0].vote,father_list,0))
            for tip in selected_tips:
                if new_site in tip.children_list:
                    continue
                tip.children_list.append(new_site)
            new_site.update_weight()
            self.Tangle.id_node_map[new_site.id]=new_site
            self.env.put_broadcast(self, self.pki.sign(
                self, Message(myid, new_site, round)))
        self.update_plotdata()

    # def put_output(self):
    #     self.env.put_output(self,
    #                         self.plotdata)
    #     if (self.env.get_id(self)!=0):
    #         return
    #     print(self.plotdata)
    #     plt.plot(self.plotdata, 'ro')
    #     plt.show()
    def receive_messages(self):
        return
        msgs = self.env.get_input_msgs(self)
        for msg in msgs:
            if (not self.pki.verify(msg)):
                raise RuntimeError
            new_site = msg.get_extraction().copy()
            if not new_site:
                raise RuntimeError
            self.Tangle.insert_site(new_site)
        

    def update_plotdata(self):
        myid = self.env.get_id(self)
        if myid != 0 :
            return
        self.plotdata.append(self.Tangle.genesis_site.children_list[0].calculate_cumulative_weight()/self.Tangle.genesis_site.children_list[1].calculate_cumulative_weight())
        # print(self.Tangle.genesis_site.children_list[0].calculate_cumulative_weight())
        # print(self.Tangle.genesis_site.children_list[1].calculate_cumulative_weight())
        # print(' ')

