import re
from termcolor import colored
from transitions.extensions import GraphMachine

transitions_functions = [
        {
            "trigger": "sold",
            "source": "user",
            "dest": "buying",
            "conditions": "is_going_to_buying",
        },
        {
            "trigger" : "select_type",
            "source":"buying",
            "dest":"typename",
            "conditions": "is_type_avaliable"
        
        },
        {
            "trigger" : "set_amount",
            "source":"typename",
            "dest":"amount",
            "conditions": "is_number_avaliable"
        },
        {
            "trigger" : "set_receiver",
            "source": "amount",
            "dest": "receiver",
            "conditions": "is_name_avaliable"
        },
        {
            "trigger" : "set_address",
            "source": "receiver",
            "dest": "address",
            "conditions": "is_address_avaliable"
        },
        # load back part
        {
            "trigger" : "load",
            "source": "user",
            "dest": "loading",
            "conditions": "load_to_last_condition",
        },
        {
            "trigger": "load_back_buying",
            "source":"loading",
            "dest":"buying"
        },
        {
            "trigger" : "load_back_typename",
            "source" : "loading",
            "dest":"typename",
        },
        {
            "trigger" : "load_back_amount",
            "source" : "loading",
            "dest": "amount"
        },
        {
            "trigger": "load_back_receiver",
            "source" : "loading",
            "dest" : "receiver"
        },
        {
            "trigger" :  "load_back_address",
            "source" : "loading",
            "dest" : "address"
        },
        {
            "trigger" : "go_back",
            "source": ["buying","loading"],
            "dest":"user"
        }
]

class Machine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_buying(self, event):
        return event == '我想買米'

    def on_enter_buying(self, event):
        self.show_state()
        print("您想買什麼米呢？")

    def load_to_last_condition(self, state):
        print("In load to last conditions")
        return state[0] == "load"

    def on_enter_loading(self,state):
        self.show_state()
        if(state[1] == "buying"):
            self.load_back_buying(1)
        elif (state[1] == "typename"):
            self.load_back_typename(1)
        elif (state[1] == "amount"):
            self.load_back_amount(1)
        elif state[1] == "receiver":
            self.load_back_receiver(1)
        elif state[1] == "address":
            self.load_back_address(1) 
        else:
            self.go_back()

    def is_type_avaliable(self,typename):
        return True

    def on_enter_typename(self,typename):
        self.show_state()
        print("請問您要的數量為？單位為斤") 
        pass

    def is_name_avaliable(self, name):
        return True

    def on_enter_receiver(self,name):
        self.show_state()
        print("請問收件地址為？")

    def is_address_avaliable(self,address):
        return True

    def on_enter_address(self,address):
        self.show_state()

    def is_number_avaliable(self,number):
        # judge number is number
        return True
    
    def on_enter_amount(self,numer):
        self.show_state()
        print("好的～那請問收件者的姓名是什麼呢？")
     
    def show_state(self):
        text = "now state is in %s " % colored(self.state,"green")
        text = colored(text,"red")
        print(text)



if __name__ == '__main__':
    machine = Machine(
            states=["user", "buying", "typename", "amount", "receiver", "address", "loading"],
            transitions = transitions_functions,
            initial = "user",
            auto_transitions=False,
            show_conditions=False,
    )
    # machine.sold("我想買米")
    # machine.select_type(1)
    # machine.set_amount(5)
    # machine.set_receiver("糙米")
    # machine.set_address("wwwww")
    response = machine.load(["load","address"])
    machine.get_graph().draw("graph.png",prog="dot",format="png")
    

