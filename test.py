import game 
import data
import random
class Test:
    p = game.Game()
    def __init__(self):
        pass


    def select_ag(self):
        '''selects all the agents in the list'''
        for a in range(5):
            try:
                print(p.agent_select(a))

            except IndexError:
                print('No more agents')
                
    def select_map(self):
        '''selects all maps in the list'''
        for a in range(3):
            try:
                p.map_select(a)    
            except IndexError:
                print('No more maps')
                
    def omen_ab(self):
        '''teleports to a random location 10 times per map, 3 maps'''
        maps = ['ascent', 'bind', 'haven']
        for b in range(3):
            print(maps[b][0].upper()+maps[b][1:],'\n')
            p.map_select(b) 
            data.make_map(maps[b])
            p.initialise('omen')  
            for c in range(10):
                try:
                    a = random.randint(0,len(p.player_pos.get_paths())-1)
                    print('You teleported to', p.player_pos.get_paths()[a],'\n')
                    p.omen(a)
                except IndexError:
                    print('No more rooms')
    def prompt_test(self):
        p.prompt(['Option A', 'Option B', 'Option C','Option 4'],'Test input', False)

    def sage_ab(self):
        '''blocks off all paths to the current room'''
        for a in range(5):
            try:
                print(p.player_pos.get_paths())
                p.sage(0)
            except IndexError:
                print('No other paths to block\n')
                break
                
    def sova_ab(self):
        '''reveals information in all paths'''
        for a in range(5):
            try:
                print('\n'+str(p.player_pos.get_paths()), ', ', a + 1)
                p.sova(a)
            except IndexError:
                print('No more paths\n\n')
                break

p = game.Game()
x = Test()
x.select_ag()
x.select_map()
x.prompt_test()
x.omen_ab()
x.sova_ab()
x.sage_ab()