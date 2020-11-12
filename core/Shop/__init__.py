import json
from core.Colors import bcolors as css

class Shop():
    def __init__(self, engine):
        self.pos=[4,4]
        self.tools=json.loads(open('core/Shop/storage/tools.json').read())
        self.commands=json.loads(open('core/Shop/cmds.json').read())['commands']
        self.engine=engine
        #print(self.tools)
    
    def swindow(self):
        print('[INFO] Tools:')
        for tool in self.tools.keys(): print('-',tool)
    
    def Enter(self):
        self.engine.inshop=True
    
    def Exit(self):
        self.engine.inshop=False
    
    def shop(self, tool:str, prize:int):
        '''add the json-like object in core/cmds.json or core/Character/cmds.json'''
        # modifica locale
        self.engine.commands.append(tool)
        self.engine.subtract_points(prize)
        # modifica i file
        print(tool)
        past=json.loads(open(self.tools[tool]['update_path']).read())
        past['commands'].append(tool)
        past['cheatsheet'].update({tool:self.tools[tool]})
        f=open(self.tools[tool]['update_path'],'w')
        f.write(json.dumps(past))
        f.close()

    def parser(self, money, raw=None):
        if not raw: raw=input('[SHOP] >> ')
        cmd=raw.split()[0].lower()
        params=raw.split()[1:]
        if not cmd in self.commands:
            print('[SHOP][ERR] Unrecognized command:',cmd)
            return
        else:
            if cmd in ['buy', 'shop']:
                toolname=params[0]
                if not toolname in self.tools.keys():
                    print('[SHOP][ERR] {tn} not found.'.format(tn=toolname)); return
                # can you buy it?
                if int(self.tools[toolname]['prize'])>int(money):
                    print('[SHOP][ERR] This tool costs too much!')
                    return
                else:
                    self.shop(toolname, int(self.tools[toolname]['prize']))
            if cmd in ['bye', 'exit']:
                self.engine.inshop=False
