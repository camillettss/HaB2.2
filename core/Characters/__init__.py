import random, time
import json
random.seed(time.time())
from core.Errors import *
from core.Colors import bcolors as css
import base64

def GenKey():
    return

class Kernel():
    def __init__(self):
        self.islocked=True
        self.is_active=True
        self.ports={'80':1, '443':1}
        self.hashes={}
        [self.hashes.update({port:base64.b64encode(''.join([chr(random.randint(97,122)) for _ in range(5)]).encode()).decode()}) for port in self.ports.keys()]

class Robot():
    def __init__(self, cols:int, rows:int, Engine, image='R'):
        self.hp=100
        self.dict_pos={'x':random.randint(0,cols-1),'y':random.randint(0,rows-1)}
        self.pos=list(self.dict_pos.values())
        self.image=image
        self.commands=json.loads(open('core/Characters/cmds.json').read())['commands']
        self.id=str(random.randint(0,100))
        self.state=css.FAIL+'locked'+css.ENDC
        # ---
        self.kernel=Kernel()
        self.Engine=Engine
    
    def move(self, pos:dict): raise NotImplementedError

    def parser(self, cmd):
        _cmd=cmd.split()[0].lower()
        params=cmd.split()[1:]
        if '-h' in params:
            self.docs(_cmd)
            return
        #params=[arg.casefold() for arg in params]
        # se _cmd necessita di più parametri ritorna subito un errore
        if (_cmd in ['hack']) and len(params)<=0:
            print(css.FAIL+'[ERR]'+css.ENDC+' Some parameters are missing.'); return
        if not _cmd in self.commands:
            raise CommandError(cmd)
        else:
            if _cmd=='hack':
                #print(self.kernel.__dict__, params, sep='--')
                if self.kernel.ports[params[0]]==1:
                    raise HackError()
                else:
                    print(css.OKCYAN+'[..]'+css.ENDC+' Hacking on port:',params[0])
                    self.kernel.islocked=False
                    self.state=css.OKGREEN+'unlocked'+css.ENDC
                    time.sleep(0.5)
                    print(css.OKCYAN+'[*]'+css.ENDC+css.OKGREEN+' Successfully hacked.'+css.ENDC)
            elif _cmd=='help':
                print(css.HEADER+'[H]'+css.ENDC+' List of commands:'); [print('-',cmd) for cmd in self.commands]
                print(css.HEADER+'[H]'+css.ENDC+' Type "cmd -h" for info about cmd.')
            elif _cmd=='scan':
                print(css.OKCYAN+'[..]'+css.ENDC+' Scanning...')
                print('[*] Found ports:')
                for port in self.kernel.ports.keys():
                    if self.kernel.ports[port] in ['1',1]:
                        print('-',css.HEADER+port,css.ENDC+' status:'+css.FAIL,self.kernel.ports[port],css.ENDC)
                    else:
                        print('-',port,' status:'+css.OKGREEN,self.kernel.ports[port], css.ENDC)
            elif _cmd in ['destroy', 'shutdown']:
                if self.kernel.islocked: raise HackError()
                print(css.FAIL+'[..]'+css.ENDC+' Self-Destruction Enabled..')
                self.kernel.is_active=False
                self.Engine.robots.remove(self)
                time.sleep(0.4)
                print(css.HEADER+'[*]'+css.ENDC+' Bot killed.')
            elif _cmd=='hash':
                if params[0]=='-port':
                    # show mode, mostra la cifratura della porta
                    try:
                        print(css.OKCYAN+'[HASH]'+css.ENDC,params[1],self.kernel.hashes[str(params[1])])
                    except Exception:
                        [print(css.OKCYAN+'[HASH]'+css.ENDC,key,self.kernel.hashes[key]) for key in self.kernel.hashes.keys()]
                elif params[0]=='-res':
                    # map commands like: {param:val}
                    mappedparams={}
                    ncmd=cmd.lower().split()[1:]
                    for p in ncmd:
                        if not p.startswith('-'): continue
                        try:
                            mappedparams.update({p:ncmd[ncmd.index(p)+1]})
                        except: break
                    if mappedparams['-res']==base64.b64decode(self.kernel.hashes[mappedparams['-port']]).decode():
                        self.kernel.ports[mappedparams['-port']]=0
                        print(css.HEADER+'[*]'+css.ENDC+' Port {p} Successfully bypassed.'.format(p=mappedparams['-port']))
                    else:
                        print(css.FAIL+'[!!] Failed.'+css.ENDC)
                else:
                    try:
                        print(css.OKGREEN+'[HASH]'+css.ENDC,params[1],self.kernel.hashes[str(params[1])])
                    except Exception:
                        [print(css.OKGREEN+'[HASH]'+css.ENDC,key,self.kernel.hashes[key]) for key in self.kernel.hashes.keys()]
            elif _cmd in ['translater', 'encoder', 'decoder']:
                if _cmd=='encoder':
                    s=params[params.index('-text')+1]
                    print(css.HEADER+'[*]'+css.ENDC+' Encoded text: '+css.OKBLUE, base64.b64encode(s).decode(),css.ENDC)
                elif _cmd=='decoder':
                    s=params[params.index('-text')+1]
                    print(css.HEADER+'[*]'+css.ENDC+' Decoded text: '+css.OKBLUE, base64.b64decode(s).decode(),css.ENDC)
                elif _cmd=='translater':
                    if not '-mode' in params:
                        if 'encode' in params or 'decode' in params:
                            if 'encode' in params:
                                s=params[params.index('-text')+1]
                                print(css.HEADER+'[*]'+css.ENDC+' Encoded text: ', base64.b64encode(s).decode())
                            else:
                                s=params[params.index('-text')+1]
                                print(css.HEADER+'[*]'+css.ENDC+' Decoded text: ', base64.b64decode(s).decode())
            elif _cmd == 'exit':
                self.Engine.selected=None
    
    def docs(self, man):
        data=json.loads(open('core/Characters/cmds.json').read())
        for key in data['cheatsheet'][man]:
            print(key,'->',data['cheatsheet'][man][key])