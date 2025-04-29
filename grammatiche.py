import random

#template per commentare funzioni (da implementare):
"""Breve descrizione
Argomenti: descrizione degli argomenti

Return: cosa restituisce la funzione

Eccezioni: quali errori lancia la funzione
"""

# struttura per creare un albero
# in questo codice viene usato per memorizzare le varie derivazioni
class Nodo:
    def __init__(self, valore, profondità = 0):
        self.valore = valore
        self.profondita = profondità
        self.figli = []

    def aggiungi_figlio(self, figlio):
        self.figli.append(figlio)
        
# funzione per stampare l'albero, per ora la lasciamo globale 
def stampa_albero(nodo, livello=0):
    print(" " * livello * 2 + str(nodo.profondita) +" "+ str(nodo.valore))
    for figlio in nodo.figli:
        stampa_albero(figlio, livello + 1)

class Grammatica:
    def __init__(self):
        self.non_terminali = set()  # array dei simboli non terminali
        self.terminali = set()  # array dei simboli terminali
        # dizionario con:
        # chiave -> simbolo non terminale
        # valore -> tupla di possibili produzioni 
        self.regole = dict()  
        self.simbolo_iniziale = None
        self.radice = None # radice dell'albero di derivazione
        
	# aggiunge simboli non terminali
    def add_nt(self, simbolo):  
    	# i controlli sono da rivedere
        if simbolo in self.terminali:
            raise ValueError(f"{simbolo} è un simbolo terminale")

        if not isinstance(simbolo, str):
            raise TypeError("Devi inserire una stringa")

        self.non_terminali.add(simbolo)
        
	# aggiunge simboli terminali
    def add_t(self, simbolo):  
    	# i controlli sono da rivedere
        if simbolo in self.non_terminali:
            raise ValueError(f"{simbolo} C( un simbolo non terminale")

        if not isinstance(simbolo, str):
            raise TypeError("Devi inserire una stringa")

        self.terminali.add(simbolo)

    def set_ini(self, simbolo):  # definisce il simbolo iniziale
        if simbolo not in self.non_terminali:
            raise ValueError("Deve essere un non terminale")

        self.simbolo_iniziale = simbolo
        
	# aggiunge una regola
    def add_regole(self, chiave, valore):  
        if (
            not isinstance(chiave, str)
            or not isinstance(valore, tuple)
            or len(valore) < 1
        ):
            raise ValueError("Argomento non valido")  # da rivedere

        self.regole[chiave] = valore
        
	# genera stringa casuale seguendo le regole della grammatica
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
    #calcolare e memorizzare tutte le derivazione diventa 
    #progressivamente più complicato 
    #all'aumentare dei simboli non terminali
    #per guadagnare salute mentale (poca) potremmo cambiare profondità 
    #ad ogni non terminale incontrato e quindi avere una serie
    #di sostituzioni parziali fino ad una certa profondità
   def genera_albero_derivazione(self, profondita_massima=7, profondita=0, nodo_corrente=None):
        if nodo_corrente is None: # se non esiste creo una "radice"
            nodo_corrente = Nodo(self.simbolo_iniziale, profondita)
    
        if profondita >= profondita_massima:
            return nodo_corrente
    
        valore_attuale = nodo_corrente.valore
    
        for i, simbolo in enumerate(valore_attuale):# enumerate() genera una serie di tuple (indice, valore)
            if simbolo in self.non_terminali:
                for produzione in self.regole[simbolo]:
                    nuovo_valore = valore_attuale[:i] + produzione + valore_attuale[i + 1:]
                    nuovo_nodo = Nodo(nuovo_valore, profondita + 1)
                    nodo_corrente.aggiungi_figlio(nuovo_nodo)
                    # Ricorsione su ogni nuovo nodo generato
                    self.genera_albero_derivazione(profondita_massima, profondita + 1, nuovo_nodo)
        return nodo_corrente

	# genera stringa casuale con (almeno) n iterazioni
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
