class Grammatica:
    def __init__(self):
        self.non_terminali = set() # array dei simboli non terminali
        self.terminali = set() # array dei simboli terminali
        self.regole = {
                    """
                        dizionario in cui:
                        chiavi -> simboli non terminali
                        valori -> tuple di possibili produzioni (terminali o non)
                    """
                } 
        self.simbolo_iniziale = None

    def add_nt (self, simbolo): # aggiunge simboli non terminali
        if simbolo in self.terminali:
            raise ValueError(f"{simbolo} è un simbolo terminale")

        if not isinistance(simbolo, str):
            raise TypeError("Devi inserire una stringa")

        
        self.non_terminali.add(simbolo)


    def add_t (self, simbolo): # aggiunge simboli terminali
        if simbolo in self.non_terminali:
            raise ValueError(f"{simbolo} è un simbolo non terminale")

        if not isinistance(simbolo, str):
            raise TypeError("Devi inserire una stringa")
        
        self.terminali.add(simbolo)

    def set_ini (self, simbolo): # definisce il simbolo iniziale
        if simbolo not in non_terminali:
            raise ValueError("Deve essere un non terminale")
            
        self.simbolo_iniziale = simbolo
        
 """dubbio su come verificare che la grammatica funzioni (arrivi ad un risultato in un tempo finito)
    controllo in creazione regole:
    imporre almeno un simbolo terminale per ogni produzione/almeno in una produzione?
    
    controllo in generazione stringa:
    limite su iterazioni (es. 20) dopodiche consideriamo le regole non funzionanti?
    massimo lunghezza risultato dopodiche consideriamo le regole non funzionanti?"""
    def add_regole (self, chiave, valore): # aggiunge una regola
        if not isinistance(chiave, str) or valore not isinistance(valore, tuple) or len(valore) < 1:
            raise ValueError("Argomento non valido") #da rivedere
        
        self.regole[chiave] = valore
    
    def genera_stringa(self):
        # import random per scegliere con quale simbolo procedere?
        ris = [self.simbolo_iniziale]
        ctrl = True
        while ctrl:
            for i range(len(ris)):
                if ris[i] in non_terminali:
                    ris[i] = list(random.choice(regole[i]))
           #tutto questo while non funge
           #ris sarà sempre una lista di un solo elemento
           #bisogna lavorare su una stringa usando replace()
           tmp = 0
            for elem in ris:
                if elem in non_terminali:
                    tmp += 1
            ctrl = bool(tmp)
        return ris
    
    def genera_nIterazioni(self, n):
        pnt = self.simbolo_iniziale # puntatore settato al primo elemento

        # lista di stringhe
        lst_tot = []
        lst_ris = []

        for j in range(len(self.regole[pnt])):
            tmp = self.regole[pnt][j]

            # come cazzo faccio?????
            # replace() per sostituire i termini all'interno tmp (stringa)
            # ma come faccio a fare tutte le sostituzione possibili * n volte?

            lst_tot.append(tmp)

    def __str__(self):
