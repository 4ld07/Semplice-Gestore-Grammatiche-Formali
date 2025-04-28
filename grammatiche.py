import random

class Nodo:
    def __init__(self, valore, profondità = 0):
        self.valore = valore
        self.profondita = profondità
        self.figli = []

    def aggiungi_figlio(self, figlio):
        self.figli.append(figlio)

def stampa_albero(nodo, livello=0):
    print(" " * livello * 2 + str(nodo.profondita) +" "+ str(nodo.valore))
    for figlio in nodo.figli:
        stampa_albero(figlio, livello + 1)

class Grammatica:
    def __init__(self):
        self.non_terminali = set()  # array dei simboli non terminali
        self.terminali = set()  # array dei simboli terminali
        self.regole = dict()  # dizionario
        self.simbolo_iniziale = None
        self.radice = None

    def add_nt(self, simbolo):  # aggiunge simboli non terminali
        if simbolo in self.terminali:
            raise ValueError(f"{simbolo} è un simbolo terminale")

        if not isinstance(simbolo, str):
            raise TypeError("Devi inserire una stringa")

        self.non_terminali.add(simbolo)

    def add_t(self, simbolo):  # aggiunge simboli terminali
        if simbolo in self.non_terminali:
            raise ValueError(f"{simbolo} C( un simbolo non terminale")

        if not isinstance(simbolo, str):
            raise TypeError("Devi inserire una stringa")

        self.terminali.add(simbolo)

    def set_ini(self, simbolo):  # definisce il simbolo iniziale
        if simbolo not in self.non_terminali:
            raise ValueError("Deve essere un non terminale")

        self.simbolo_iniziale = simbolo

    def add_regole(self, chiave, valore):  # aggiunge una regola
        if (
            not isinstance(chiave, str)
            or not isinstance(valore, tuple)
            or len(valore) < 1
        ):
            raise ValueError("Argomento non valido")  # da rivedere

        self.regole[chiave] = valore

    def genera_stringa(self, maxi=10):

        ris = self.simbolo_iniziale  # str
        i = 0
        while any(simbolo in self.non_terminali for simbolo in ris) and i < maxi:
            for elem in ris:
                if elem in self.non_terminali:
                    ris = ris.replace(elem, random.choice(self.regole[elem]))
        i += 1

        return ris

    # sfida: generare albero di derivazione
    def genera_albero_derivazione(self, n = 4, profondità = 0, figlio = 0, pnt = None, base = "nodo"):
        while profondità < n:
            if pnt == None:
                # nome di variabile dinamico, perso 2 ore solo per questo 
                #(locals() dizionario di variabili locali, globals() globali)
                globals()['%s%d_%d' % (base,profondità,figlio)] = Nodo(self.simbolo_iniziale, profondità)
                pnt = globals()['%s%d_%d' % (base,profondità,figlio)]
            else:
                profondità = pnt.profondita + 1 
                #calcolare e memorizzare tutte le derivazione diventa 
                #progressivamente più complicato 
                #all'aumentare dei simboli non terminali
                #per guadagnare salute mentale (poca) potremmo cambiare profondità 
                #ad ogni non terminale incontrato e quindi avere una serie
                #di sostituzioni parziali fino ad una certa profondità
                tmp = pnt.valore
                j = 0 
                for char in tmp:
                    if char in self.non_terminali:
                        prod = set(self.regole[char])
                        i = 0
                        tmp_set = set()
                        for elem in prod:
                            tmp = pnt.valore.replace(char, elem)
                            if not tmp_set or tmp not in tmp_set:
                                tmp_set.add(tmp)
                                globals()['%s%d_%d' % (base,profondità,i+j)] = Nodo(tmp, profondità)
                                new = globals()['%s%d_%d' % (base,profondità,i+j)]
                                pnt.aggiungi_figlio(new)
                            
                                i += 1
                        j += 1 
                
                if pnt.figli:
                    for i in range(len(pnt.figli)):
                        self.genera_albero_derivazione(n, profondità, i, pnt.figli[i])
                else:
                    break
        
        return pnt #ritorno la radice alla fine se il cosmo si è allineato perfettamente

    def genera_nIterazioni_random(self, n = 4):
        ris = self.simbolo_iniziale
        count = 0

        while count < n - 1:
            for elem in ris:
                if elem in self.non_terminali:
                    choice = []
                    for i in self.regole[elem]:
                        if any(a in self.non_terminali for a in i):
                            choice.append(i)
                    ris = ris.replace(elem, random.choice(choice))
            count += 1
        for elem in ris:
            if elem in self.non_terminali:
                choice2 = []
                for i in self.regole[elem]:
                    if all(a not in self.non_terminali for a in i):
                        choice2.append(i)
                ris = ris.replace(elem, random.choice(choice2))
        return ris

    def __str__(self):
        pass


g = Grammatica()
g.add_nt("P")
g.add_t("a")
g.add_t("b")
g.set_ini("P")
g.add_regole("P", ("a", "b", "aPa", "bPb"))
print(g.genera_stringa())

print(g.genera_nIterazioni_random(15))
a = g.genera_albero_derivazione(3)
stampa_albero(a)
