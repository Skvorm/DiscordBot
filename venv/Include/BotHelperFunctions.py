import discord
import random


class BotHelperFunctions:
    def get_roll_range(self, input_string, max_val=10000, max_die=1000):
        # parses input from !roll command
        # outputs list of[min,max,# of die]
        end = 100
        num_die = 1
        param = input_string.replace('!roll', '')
        param = param.strip()
        if param.find('d') != -1:
            param = param.split('d')
            print(param)
            start = 1
            # if parameters greater than limits, uses max values
            # if less, uses default parameters
            if len(param) > 1:
                if param[0] == '':
                    param[0] = 1
                if param[1] == '':
                    param[1] = 6
                    try:
                        end = int(param[1])
                        num_die = int(param[0])
                    except ValueError:
                        end=100
                        num_die=1
                if end >= max_val:
                    end=max_val
                elif end <= 0:
                    end = 100
                if num_die > max_die:
                    num_die=max_die
                elif num_die <= 0:
                    num_die = 1
            else:
                end = int(param[0])
            out = [start, end, num_die]
        elif param.find('-') != -1:
            param = param.split('-')
            start = int(param[0])
            end = int(param[1])
            out = [start, end, 1]
        else:
            # min,max,times rolled
            out = [1, 100, 1]
        return out

    def parse_poll(self, input_string,delimiter="!~"):
        quest = ""
        ans = []
        parse_list=[]
        param = input_string.replace('!poll', '')
        param = param.strip()
        if param.find(delimiter) != -1:
            param = param.split(delimiter)
            if len(param) > 1:
                quest = param[0]
                ans = param[1:len(param)]
        else:
            quest = param
            ans = ["Yes","No"]
        parse_list=[quest,ans]
        return parse_list

    def parse_song(self,input_string):
        param = input_string.replace('!music', '')
        param = param.strip()
        param = param.split(" ")[0]
        try:
            param=int(param)
            if param <=0:
                param=-1
        except ValueError:
            param=-1
        return param






if __name__ == '__main__':
    d = BotHelperFunctions()
    #print(d.get_roll_range("!roll 1-100"))
    #print(d.get_roll_range("!roll 2-59"))
    #print(d.parse_poll("We will win?"))
    #print(d.get_roll_range("!roll"))
    #print('wor-d'.split('-'))
    # print(d.get_roll_range("!roll"))
    #tmp=0
    tmp = d.parse_song("!music 9")
   # print(str(tmp)+":"+str(d.parse_song("!music 9")))
  #  tmp = d.parse_song(("!music 2  2 2 2"))
   # print(str(tmp)+":"+str(d.parse_song("!music 2  2 2 2")))
    tmp = d.parse_song("!music")
    print(str(tmp)+":"+str(d.parse_song("!music")))
    tmp = d.parse_song("!music song")
   # print(str(d.parse_song("!music song")))
   # print(str(d.parse_song("!music 2.5")))
   # print(str(d.parse_song("!music song 2  23 a")))
   # print(str(d.parse_song("!music -2")))

   # print(d.get_roll_range("!roll boulder"))
