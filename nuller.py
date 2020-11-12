import json

# standard variables
dumped_dat='eyJmaXJzdGxhdW5jaCI6IDF9'
userdata_dat='e30='
global_cmds='''{
    "commands":[
        "select",
        "show",
        "notes",
        "help",
        "bye",
        "reset",
        "shop"
    ],
    "cheatsheet":{
        "select":{
            "params":["-m", "--method"],
            "output":"seleziona un oggetto usando un metodo specifico",
            "notes":"puoi selezionare per id o pos, id->botID, pos->x,y"
        }, "show":{
            "params":["id", "pos", "null"],
            "output":"mostra uno specifico valore sulla mappa",
            "notes":"non puoi mostrare sia pos che id insieme."
        },
        "notes":{
            "params":["add","append","new", "show"],
            "output":"aggiungi o mostra una nota",
            "notes":"le note sono stringhe salvate per dopo, magari un algoritmo."
        },
        "help":{
            "params":[],
            "output":"mostra la lista di comandi.",
            "notes":""
        },
        "bye":{
            "params":[],
            "output":"go back to title screen",
            "notes":""
        },
        "reset":{
            "params":["-w"],
            "output":"delete a saved variable ( specified by -w)",
            "notes":"-w values: * for everything, usrname or usr for change ur name and score to set score=0"
        },
        "shop":{
            "params":["-buy", "-sw", "-e"],
            "output":"entra nello shop o compra direttamente qualcosa.",
            "notes":"se -sw è specificato mostra la vetrina. -buy precede il tool da comprare. usa -e per non entrare nello shop"
        }
    }
}'''
bot_cmds='''{
    "commands": [
        "help",
        "hack",
        "scan",
        "destroy",
        "shutdown",
        "hash",
        "translater",
        "encoder",
        "decoder",
        "exit"
    ],
    "cheatsheet": {
        "hack": {
            "params": [
                "port"
            ],
            "output": "se port \u00c3\u00a8 sbloccata usala per disattivare i sistemi di sicurezza del bot"
        },
        "scan": {
            "params": [
                "port"
            ],
            "output": "restituisce una lista delle porte attive o disabilitate",
            "notes": "se port \u00c3\u00a8 specificato scansionala"
        },
        "destroy": {
            "params": [],
            "output": "elimina il bot",
            "notes": "devi avere l'accesso al bot, ottienilo hackerandolo"
        },
        "shutdown": {
            "params": [],
            "output": "elimina il bot",
            "notes": "devi avere l'accesso al bot, ottienilo hackerandolo"
        },
        "hash": {
            "params": [
                "-res",
                "-port"
            ],
            "output": "usa una chiave per bypassare una porta o ottieni le hash della chiave",
            "notes": "-res bypassa una porta sfruttando un hash decodificato, -port p mostra l'hash codificato di p"
        },
        "encoder": {
            "params": [
                "-text"
            ],
            "output": "codifica una stringa",
            "notes": "-text t codifica t"
        },
        "decoder": {
            "params": [
                "-text"
            ],
            "output": "codifica una stringa",
            "notes": "-text t codifica t"
        },
        "translater": {
            "params": [
                "-text",
                "-mode"
            ],
            "output": "codifica o decodifica una stringa",
            "notes": "-text t codifica/decodifica t, -mode 1 = codifica, -mode 2 = decodifica"
        },
        "exit": {
            "params": [],
            "output": "torna alla mappa",
            "notes": ""
        }
    }
}'''

# azzera lo shop
f=open('core/Shop/storage/tools.json','w')
f.write('''{
    "0":{

    },
    "1": {
        "crack": {
            "params": [
                "-port"
            ],
            "output": "bypass a port without an hash",
            "notes": "-port port to bypass",
            "prize": "10",
            "update_path": "core/Characters/cmds.json"
        },
        "skip":{
            "params": [
                "-man"
            ],
            "output": "bypass a port without an hash",
            "notes": "-port port to bypass",
            "prize": "10",
            "update_path": "core/Characters/cmds.json"
        }
    }
}''')
f.close()

# azzera lo score e il nome
f=open('data/userdata.txt','w')
f.write(userdata_dat)
f.close()

# setta firstlaunch a 1
f=open('data/dumped.dat','w')
f.write(dumped_dat)
f.close()

# azzera gli acquisti globali
f=open('core/cmds.json','w')
f.write(global_cmds)
f.close()

# azzera gli acquisiti locali
f=open('core/Characters/cmds.json','w')
f.write(bot_cmds)
f.close()

print('[*] Formatted.')