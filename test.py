import game 
import data
import random
class Test:
    p = game.Game()
    def __init__(self):
        pass


    def select_ag(self):
        for a in range(5):
            try:
                print(p.agent_select(a))

            except IndexError:
                print('No more agents')
    def select_map(self):    
        p.map_select(random.randint(0,2))    

    def omen_ab(self):
        maps = ['ascent', 'bind', 'haven']
        b = random.randint(0,3)
        p.map_select(b) 
        p.initialise('omen')   
        a = random.randint(0,len(data.make_map(maps[b])))
        print(list(data.make_map('ascent').keys()),', ',a+1,'\nYou teleported to', p.player_pos.get_paths()[a])
        p.omen(a)

    def prompt_test(self):
        p.prompt(['Option A', 'Option B', 'Option C','Option 4'],'Test input', False)

    def sage_ab(self):
        a = random.randint(0,len(p.player_pos.get_paths()))
        print(p.player_pos.get_paths(), ', ', a + 1)
        p.sage(a)

    def sova_ab(self):
        a = random.randint(0,len(p.player_pos.get_paths()))
        print(p.player_pos.get_paths(), ', ', a + 1)
        p.sova(a)
        pass
    

p = game.Game()
x = Test()
x.select_ag()
x.select_map()
x.prompt_test()
x.omen_ab()
x.sage_ab()
x.sova_ab()