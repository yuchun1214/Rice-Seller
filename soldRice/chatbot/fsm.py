import re
from .utils import send_text_message, send_confirm_message, send_buttom_message
from termcolor import colored
from transitions.extensions import GraphMachine

relations = {
    "WR" : "白米",
    "BR" : "糙米"
}


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
            "trigger" : "go_to_check",
            "source":["typename","address","amount","receiver"],
            "dest" : "check"
        },
        {
            "trigger" : "event_trigger",
            "source" : "check",
            "dest":"confirm",
            "conditions":"confirm_condition"
        },
        {
            "trigger" : "event_trigger",
            "source" : "check",
            "dest" : "not_confirm",
            "conditions" : "not_confirm_condition"
        },
        {
            "trigger" : "event_trigger",
            "source" : "not_confirm",
            "dest" : "receiver",
            "conditions" : "is_modifing_address"
        },
        {
            "trigger" : "event_trigger",
            "source" : "not_confirm",
            "dest" : "buying",
            "conditions" : "is_modifing_product"
        },
        {
            "trigger" : "event_trigger",
            "source":"not_confirm",
            "dest":"typename",
            "conditions" : "is_modifing_amount"
        },
        {
            "trigger" : "event_trigger",
            "source":"not_confirm",
            "dest":"amount",
            "conditions" : "is_modifing_receiver"
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
            "trigger" : "load_back_not_confirm",
            "source":"loading",
            "dest":"not_confirm"
        },
        {
            "trigger":"load_back_check",
            "source" : "loading",
            "dest" : "check"
        },
        {
            "trigger" : "go_back",
            "source": ["buying","loading","confirm"],
            "dest":"user"
        },
        
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
            event[1].state = 'buying'

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
        elif state[1] == "not_confirm":
            self.load_back_not_confirm("load")
        elif state[1] == "product_modified":
            self.load_back_product_modified("load")
        elif state[1] == "check":
            self.load_back_check("load")
        else:
            self.go_back(1)

    def is_type_avaliable(self,typename):
        types = ["白米","糙米"]
        return typename[0].message.text in types

    def on_enter_typename(self,typename):
        self.show_state()
        print(colored(typename,'green'))
        if typename != 'load':
            if typename[1].state == 'buying':
                if(typename[0].message.text == '白米'):
                    product = 'WR'
                elif(typename[0].message.text == '糙米'):
                    product = 'BR'
                print(colored(product, 'green'))
                typename[1].products = product
                if(typename[1].user_confirm):
                    self.go_to_check(typename)
                else:
                    typename[1].state = 'typename'
                    send_text_message(typename[0].reply_token, "請問您要的數量為？單位為斤")
            else:
                typename[1].state = 'typename'
                send_text_message(typename[0].reply_token,  "請問您要的數量為？單位為斤")
                

    def is_name_avaliable(self, name):
        return True

    def is_modifing_receiver(self,name):
        return name[0].message.text == '收件人'

    def on_enter_receiver(self,name):
        self.show_state()
        if name != 'load':
            if name[1].state == 'amount':
                name[1].receiver = name[0].message.text
                if name[1].user_confirm:
                    self.go_to_check(name)
                else:
                    send_text_message(name[0].reply_token, "請問收件地址為？")
                    # name[1].receiver = name[0].message.text
                    name[1].state = 'receiver'
            else:
                send_text_message(name[0].reply_token, "請問收件地址為？")
                name[1].state = 'receiver'

        

    def is_address_avaliable(self,address):
        return True

    def on_enter_address(self,address):
        self.show_state()
        if address != 'load':
            address[1].address = address[0].message.text
            address[1].state = 'address'
            self.go_to_check(address)

    def on_enter_check(self,customer):
        self.show_state()
        if customer != "load":
            content = "訂單如下：\n\n%s %.3f斤\n收件者：%s\n收件地址：%s\n" % (relations[customer[1].products], customer[1].amount, customer[1].receiver, customer[1].address) 
            customer[1].order = content
            customer[1].user_confirm = True
            customer[1].state = "check"
            send_confirm_message(customer[0].reply_token, content)

    def is_modifing_amount(self,amount):
        return amount[0].message.text == '數目'

    def is_modifing_address(self, address):
        return address[0].message.text == '收件地址'

    def is_number_avaliable(self,number):
        # judge number is number
        pattern = r'[0-9].[0-9]+|[0-9]+'
        result = re.search(pattern, number[0].message.text)
        if result == None:
            return False
        else:
            number[0].message.text = result.group(0)
            return True
    
    def on_enter_amount(self,number):
        if number != 'load':
            self.show_state()
            if number[1].state == 'typename':
                number[1].amount = float(number[0].message.text)
                if number[1].user_confirm:
                    self.go_to_check(number)
                else:
                    send_text_message(number[0].reply_token, "好的～那請問收件者的姓名是什麼呢？")
                    number[1].state = 'amount'
            else:
                send_text_message(number[0].reply_token, "好的～那請問收件者的姓名是什麼呢？")
                number[1].state = 'amount'

            # print("好的～那請問收件者的姓名是什麼呢？")
    
    def not_confirm_condition(self,confirm):
        return confirm[0].message.text == "否"

    def on_enter_not_confirm(self, confirm):
        self.show_state()
        print(colored(confirm, "green"))
        if confirm != 'load' :
            confirm[1].state = 'not_confirm'
            send_buttom_message(confirm[0].reply_token, "您想修改什麼"," ",[
                {
                    "type":"message",
                    "label":"商品",
                    "text" :"商品",
                },
                {
                    "type" : "message",
                    "label":"數目",
                    "text" : "數目"
                },
                {
                    "type" : "message",
                    "label" : "收件人",
                    "text": "收件人"

                },
                {
                    "type" : "message",
                    "label" : "收件地址",
                    "text" : "收件地址"
                },
            ])

    def modified_order_condition(self, things):
        
        return

    def is_modifing_product(self, things):
        return things[0].message.text == '商品'

    def on_enter_product_modified(self, product):
        # print(colored(product,"red"))
        if (product != 'load'):
            product[1].state='product_modified'
            send_buttom_message(product[0].reply_token, "請重新輸入想要的項目", "白米：200 / 斤\n糙米：150 / 斤", [
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
        
        pass

    def confirm_condition(self, confrim):
        print(colored("in confirm condition","red"))
        return confrim[0].message.text  == "是"


    def on_enter_confirm(self,confirm):
        self.show_state()
        # confirm[1].user_confirm = True
        confirm[1].state = 'user'
        confirm[1].user_confirm = False
        self.go_back(confirm)
        send_text_message(confirm[0].reply_token, "感謝您的訂購~~~")
            
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
    

