import re
from .utils import send_text_message, send_confirm_message, send_buttom_message
from termcolor import colored
from transitions.extensions import GraphMachine


transitions_functions = [
        {
            "trigger": "event_trigger",
            "source": "user",
            "dest": "buying",
            "conditions": "is_going_to_buying",
        },
        {
            "trigger" : "event_trigger",
            "source":"buying",
            "dest":"typename",
            "conditions": "is_type_avaliable"
        
        },
        {
            "trigger" : "event_trigger",
            "source":"typename",
            "dest":"amount",
            "conditions": "is_number_avaliable"
        },
        {
            "trigger" : "event_trigger",
            "source": "amount",
            "dest": "receiver",
            "conditions": "is_name_avaliable"
        },
        {
            "trigger" : "event_trigger",
            "source": "receiver",
            "dest": "address",
            "conditions": "is_address_avaliable"
        },
        {
            "trigger" : "event_trigger",
            "source" : "address",
            "dest":"confirm",
            "conditions":"confirm_condition"
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
            "trigger" : "load_back_user",
            "source" : "loading",
            "dest" : "user"
        },
        {
            "trigger" : "go_back",
            "source": ["buying","loading","confirm"],
            "dest":"user"
        }
]

class Machine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def on_enter_user(self,event):
        self.show_state()
        #event[1].state = 'user'
    
    def is_going_to_buying(self, event):
        print("is going to buying, event = ",event)
        return event[0].message.text == '我想買米'

    def on_enter_buying(self, event):
        if(event != 'load'):
            print("on enter buying, event = ",event)
            self.show_state()
            send_buttom_message(event[0].reply_token, "你想買什麼米", "白米：200 / 斤\n糙米：150 / 斤", [
                {
                    "type":"message",
                    "label":"白米",
                    "text":"白米"
                },
                {
                    "type":"message",
                    "label" : "糙米",
                    "text": "糙米"
                }
                ])

            # send_text_message(event[0].reply_token,"你想買什麼米？")
            event[1].state = "buying" 

    def load_to_last_condition(self, state):
        print("In load to last conditions")
        return state[0] == "load"

    def on_enter_loading(self,state):
        self.show_state()
        if (state[1] == "user"):
            self.load_back_user("load")
        elif(state[1] == "buying"):
            self.load_back_buying("load")
        elif (state[1] == "typename"):
            self.load_back_typename("load")
        elif (state[1] == "amount"):
            self.load_back_amount("load")
        elif state[1] == "receiver":
            self.load_back_receiver("load")
        elif state[1] == "address":
            self.load_back_address("load") 
        else:
            self.go_back(1)

    def is_type_avaliable(self,typename):
        types = ["白米","糙米"]
        return typename[0].message.text in types

    def on_enter_typename(self,typename):
        self.show_state()
        if typename != 'load':
            send_text_message(typename[0].reply_token, "請問您要的數量為？單位為斤")
            if(typename[0].message.text == '白米'):
                product = 'WR'
            elif(typename[0].message.text == '糙米'):
                product = 'BR'

            typename[1].products = product
            typename[1].state = 'typename'
            typename[1].save()
        
        pass

    def is_name_avaliable(self, name):
        return True

    def on_enter_receiver(self,name):
        self.show_state()
        if name != 'load':
            send_text_message(name[0].reply_token, "請問收件地址為？")
            name[1].receiver = name[0].message.text
            name[1].state = 'receiver'
            name[1].save()
        # print("請問收件地址為？")

    def is_address_avaliable(self,address):
        return True

    def on_enter_address(self,address):
        self.show_state()
        if address != 'load':
            product = address[1].products 
            address[1].address = address[0].message.text
            address[1].state = 'address'
            address[1].save()
            send_confirm_message(address[0].reply_token, "訂單如下：\n\t%s %d斤\n\t收件者：%s\n\t收件地址：%s\n\t" % (address[1].products, address[1].amount, address[1].receiver, address[1].address))

    def is_number_avaliable(self,number):
        # judge number is number
        return True
    
    def on_enter_amount(self,number):
        if number != 'load':
            self.show_state()
            send_text_message(number[0].reply_token, "好的～那請問收件者的姓名是什麼呢？")
            number[1].amount = int(number[0].message.text)
            number[1].state = 'amount'
            # print("好的～那請問收件者的姓名是什麼呢？")
    
    def confirm_condition(self, confrim):
        print(colored("in confirm condition","red"))
        return confrim[0].message.text in ["是","否"]

    def on_enter_confirm(self,confirm):
        self.show_state()
        confirm[1].user_confirm = True
        confirm[1].state = 'confirm'
        self.go_back()
        send_text_message(confirm[0].reply_token, "感謝您的訂購")
            

    def show_state(self):
        text = "now state is in %s " % colored(self.state,"green")
        text = colored(text,"red")
        print(text)



if __name__ == '__main__':
    machine = Machine(
            states=["user", "buying", "typename", "amount", "receiver", "address", "loading","confirm"],
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
    #response = machine.load(["load","user"])
    # machine.event_trigger("我想買米")
    machine.get_graph().draw("graph.png",prog="dot",format="png")
    

