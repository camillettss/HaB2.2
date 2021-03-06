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
            if '-h' in params:
                self.docs(cmd)
                return
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
            elif cmd in ['bye', 'exit']:
                self.engine.inshop=False
            elif cmd in ['swindow', 'show']:
                if '-q' in params:
                    # solo gli acquistabili
                    for tmode in self.tools: # globals, locals
                        print(css.OKCYAN+'[INFO]'+css.ENDC+' type:',tmode)
                        if not len(self.tools[tmode]):
                            print(' - no tools here.')
                        for tool in self.tools[tmode]:
                            if int(self.tools[tmode][tool]['prize'])>int(money):
                                pass
                            else:
                                print(css.OKBLUE+'-'+css.ENDC,tool)
                else:
                    for tmode in self.tools: # globals, locals
                        print(css.OKCYAN+'[INFO]'+css.ENDC+' type:',tmode)
                        if not len(self.tools[tmode]):
                            print(' - no tools here.')
                        for tool in self.tools[tmode]:
                            print(css.OKBLUE+'-'+css.ENDC,tool)
            elif cmd=='help':
                if not len(params):
                    print(css.HEADER+'[H]'+css.ENDC+' List of commands:')
                    [print('-',c) for c in self.commands]; print(css.HEADER+'[H]'+css.ENDC+' type "cmd -h" for additiona help about "cmd"')
                else:
                    try:
                        self.docs(params[0])
                    except:
                        print(css.FAIL+'[ERR]'+css.ENDC+' Unknown command', cmd)
            elif cmd in ['desc', 'info']:
                if cmd=='desc':
                    if not len(params): print(css.FAIL+'[ERR]'+css.ENDC+' No tool spceified.'); return
                    if '-tool' in params:
                        tool=params[params.index('-tool')+1]
                    else:
                        tool=params[0]
                    self.Tdocs(tool)
                else:
                    if not len(params):
                        for tool in self.tools:
                            self.Tdocs(tool)
                    else:
                        if '-tool' in params:
                            tool=params[params.index('-tool')+1]
                        else:
                            tool=params[0]
                        self.Tdocs(tool)
    
    def Tdocs(self, man):
        data=json.loads(open('core/Shop/storage/tools.json').read())
        for tmode in data:
            if not man in data[tmode]: continue
            [print(key,css.WARNING+'->'+css.ENDC,data[tmode][man][key]) for key in data[tmode][man]]
    
    def docs(self, man):
        data=json.loads(open('core/Shop/cmds.json').read())
        for key in data['cheatsheet'][man]:
            print(key,css.WARNING+'->'+css.ENDC,data['cheatsheet'][man][key])