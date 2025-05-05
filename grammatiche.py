import random

# struttura per creare un albero
# in questo codice viene usato per memorizzare le varie derivazioni
class Nodo:
	def __init__(self, valore, profondità = 0):
		self.valore = valore
		self.profondita = profondità
		self.figli = []

	def aggiungi_figlio(self, figlio):
		self.figli.append(figlio)

class Grammatica:
	def __init__(self):
		"""Inizia l'istanza con tutti i campi vuoti

		Campi:
		non_terminali -- set, non deve essere modificato
		terminali -- set, non deve essere modificato
		regole -- dizionario: chiave -> simbolo non terminale, valore -> tupla di possibili produzioni
		simbolo_iniziale
		radice -- ""
		"""
		self.non_terminali = set()
		self.terminali = set()
		self.regole = dict()
		self.simbolo_iniziale = None
		self.radice = None # radice dell'albero di derivazione

	def add_nt(self, simbolo):
		"""Aggiunge simboli non terminali

		Argomenti:
		simbolo -- il carattere da inserire

		Eccezioni:
		ValueError -- il simbolo è già presente nei terminali
		TypeError -- il simbolo non è una stringa
		"""
		if simbolo in self.terminali:
			raise ValueError(f"{simbolo} è un simbolo terminale")

		if not isinstance(simbolo, str):
			raise TypeError("Devi inserire una stringa")

		self.non_terminali.add(simbolo)

	def add_t(self, simbolo):
		"""Aggiunge simboli terminali

		Argomenti:
		simbolo -- il carattere da inserire

		Eccezioni:
		ValueError -- il simbolo è già presente nei non terminali
		TypeError -- il simbolo non è una stringa
		"""
		if simbolo in self.non_terminali:
			raise ValueError(f"{simbolo} è un simbolo non terminale")

		if not isinstance(simbolo, str):
			raise TypeError("Devi inserire una stringa")

		self.terminali.add(simbolo)

	def set_ini(self, simbolo):  
		"""Definisce il simbolo iniziale

		Argomenti:
		simbolo -- il carattere da inserire

		Eccezioni:
		ValueError -- il simbolo non è fra i non terminali
		TypeError -- il simbolo non è una stringa
		"""
		if simbolo not in self.non_terminali:
			raise ValueError("Deve essere un simbolo non terminale")

		if not isinstance(simbolo, str):
			raise TypeError("Devi inserire una stringa")

		self.simbolo_iniziale = simbolo

	def add_regole(self, chiave, valore):
		"""Aggiunge regole di produzione

		Argomenti:
		chiave -- simbolo non terminale
		valore -- tupla di possibili produzioni

		Eccezioni:
		ValueError -- i simboli inseriti non fanno parte di terminali/non terminali
		TypeError -- gli argomenti non sono del tipo giusto
		"""
		check = False
		for elem in valore:
			#if elem not in self.terminali and elem not in self.non_terminali:
			#non devo guardare elem in se ma i suoi caratteri
			if any(i not in self.terminali and i not in self.non_terminali for i in elem):
				check = True

		if chiave not in self.non_terminali or check:
			raise ValueError("Devi inserire un simbolo presente fra i terminali/non terminali")

		if (not isinstance(chiave, str)
			or not isinstance(valore, tuple)
		):
			raise TypeError("chiave -> stringa, valore -> tupla")

		self.regole[chiave] = valore

	def salva_grammatica(self, filename="config.txt"):
		with open(filename, "w") as file:
			# Scrivi non terminali
			file.write("NON_TERMINALI:\n")
			file.write(",".join(self.non_terminali) + "\n")

			# Scrivi terminali
			file.write("TERMINALI:\n")
			file.write(",".join(self.terminali) + "\n")

			# Scrivi simbolo iniziale
			file.write("SIMBOLO_INIZIALE:\n")
			file.write(str(self.simbolo_iniziale) + "\n")

			# Scrivi regole
			file.write("REGOLE:\n")
			for chiave, produzioni in self.regole.items():
				# Esempio: P -> a | b | aPa
					regola_str = " | ".join(produzioni)
					file.write(f"{chiave} -> {regola_str}\n")

	def carica_grammatica(self, filename="config.txt"):
		with open(filename, "r") as file:
			righe = file.readlines()

		sezione = None
		for riga in righe:
			riga = riga.strip()
			if not riga:
				continue

			if riga == "NON_TERMINALI:":
				sezione = "nt"
				continue
			elif riga == "TERMINALI:":
				sezione = "t"
				continue
			elif riga == "SIMBOLO_INIZIALE:":
				sezione = "ini"
				continue
			elif riga == "REGOLE:":
				sezione = "regole"
				continue

			if sezione == "nt":
				for simbolo in riga.split(","):
					self.add_nt(simbolo)
			elif sezione == "t":
				for simbolo in riga.split(","):
					self.add_t(simbolo)
			elif sezione == "ini":
				self.set_ini(riga)
			elif sezione == "regole":
				if "->" in riga:
					sinistra, destra = riga.split("->")
					sinistra = sinistra.strip()
					produzioni = [p.strip() for p in destra.split("|")]
					self.add_regole(sinistra, tuple(produzioni))

	def genera_stringa(self, maxi=10): 
		"""Genera stringa casuale seguendo le regole della grammatica

		Argomenti:
		maxi -- (opzionale) default 10 numero massimo di iterazioni

		Return:
		ris -- stringa
		"""
		ris = self.simbolo_iniziale  # str
		j = 0
		while any(simbolo in self.non_terminali for simbolo in ris) and j < maxi:
			for i, elem in enumerate(ris):
				if elem in self.non_terminali:
					produzione = random.choice(self.regole[elem])
					ris = ris[:i] + produzione + ris[i+1:]
					break
			j += 1
		if any(simbolo in self.non_terminali for simbolo in ris):
			msg = "Non siamo arrivati ad una stringa valida"
			return msg
		else:
			return ris

	#sfida: generare albero di derivazione
	#calcolare e memorizzare tutte le derivazione diventa 
	#progressivamente più complicato 
	#all'aumentare dei simboli non terminali
	#per guadagnare salute mentale (poca) potremmo cambiare profondità 
	#ad ogni non terminale incontrato e quindi avere una serie
	#di sostituzioni parziali fino ad una certa profondità
	def genera_albero_derivazione(self, profondita_massima=7, profondita=0, nodo_corrente=None):
		"""Genera un albero di derivazione

		Argomenti:
		profondita_massima -- (opzionale) default 7 
		profondita -- viene aumentata ricorsivamente parte da 0
		nodo_corrente -- il nodo su cui sta lavorando la funzione

		Return:
		nodo_corrente -- alla fine della ricorsione si riferisce alla radice
		"""
		if nodo_corrente is None: # se non esiste creo una "radice"
			nodo_corrente = Nodo(self.simbolo_iniziale, profondita)

		if profondita >= profondita_massima:
			return nodo_corrente

		valore_attuale = nodo_corrente.valore

		for i, simbolo in enumerate(valore_attuale):# enumerate() genera una serie di tuple (indice, valore)
			if simbolo in self.non_terminali:
				for produzione in self.regole[simbolo]:
					#[:i]scorre fino ad i(escluso), sostituisce i, [i+1:]scorre da i+1 alla fine
					nuovo_valore = valore_attuale[:i] + produzione + valore_attuale[i + 1:]
					#crea un nuovo nodo
					nuovo_nodo = Nodo(nuovo_valore, profondita + 1)
					#aggiunge il nodo alla lista dei figli
					nodo_corrente.aggiungi_figlio(nuovo_nodo)
					# Ricorsione su ogni nuovo nodo generato
					self.genera_albero_derivazione(profondita_massima, profondita + 1, nuovo_nodo)

		return nodo_corrente

	def add_albero(self, derivazioni = 7):
		"""Aggiunge un albero di derivazione all'istanza

		Argomenti:
		derivazioni -- default 7, profondità di derivazione desiderata

		Eccezioni:
		VaulueError -- se il valore inserito è minore di 1
		"""
		if derivazioni <= 0:
			raise ValueError("Il valore deve essere maggiore di 0")

		nodo = self.genera_albero_derivazione(derivazioni)
		self.radice = nodo

	def stampa_albero(self, nodo = None, prefisso = "", ultimo = True):
		"""Stampa l'albero di derivazione"""
		if nodo is None:
			nodo = self.radice
			
		#simboli per rappresentare i rami
		ramo = "└── " if ultimo else "├── "
		print(prefisso + ramo + f"[{nodo.profondita}] {nodo.valore}")
		
		#se ci sono figli preparo il nuovo prefisso e ri-setto ultimo
		if nodo.figli:
			nuovo_prefisso = prefisso + ("	 " if ultimo else "|	 ")
			for i, figlio in enumerate(nodo.figli):
				ultimo = (i == len(nodo.figli) - 1)
				self.stampa_albero(figlio, nuovo_prefisso, ultimo)

	def genera_nIterazioni_random(self, n = 4):
		"""Genera stringa casuale con (almeno) n iterazioni

		Argomenti:
		n -- (opzionale) default 4, numero minimo di iterazioni

		Return:
		ris -- stringa
		"""
		ris = self.simbolo_iniziale
		count = 0
		#any() e all() valutano una serie di espressioni simile a or e and
		#usati per iterare sui singoli caratteri delle produzioni
		while count < n - 1:
			for j, elem in enumerate(ris):
				if elem in self.non_terminali:
					choice = []
					for i in self.regole[elem]:
						if any(a in self.non_terminali for a in i):
							choice.append(i)
					if choice:
						ris = ris[:j] + random.choice(choice) + ris[j + 1:]
					else:
						ris = ris[:j] + random.choice(self.regole[elem]) + ris[j + 1:]
			count += 1

		#uso da criminali del while, itero finchè c'è almeno un non terminale
		while any(simbolo in self.non_terminali for simbolo in ris):
			for z, elem in enumerate(ris):
				if elem in self.non_terminali:
					choice_t = []#pool di caratteri terminali fra cui scegliere
					for i in self.regole[elem]:
						if all(a not in self.non_terminali for a in i):
							choice_t.append(i)
					choice_nt = []#pool di caratteri non terminali fra cui scegliere
					for j in self.regole[elem]:
						if any(b in self.non_terminali for b in j):
							choice_nt.append(j)
					if choice_t:
						ris = ris[:z] + random.choice(choice_t) + ris[z + 1:]
					else:
						ris = ris[:z] + random.choice(choice_nt) + ris[z + 1:]

		if any(simbolo in self.non_terminali for simbolo in ris):
			msg = "Non siamo arrivati ad una stringa valida: " + ris
			return msg
		else:
			return ris

	def __str__(self):
		out = f"Simbolo iniziale: {self.simbolo_iniziale}\n"
		out += f"Non terminali: {self.non_terminali}\n"
		out += f"Terminali: {self.terminali}\n"
		out += "Regole:\n"
		for k, v in self.regole.items():
			out += f"  {k} -> {v}\n"
		return out

#g = Grammatica()
#g.add_nt("P")
#g.add_t("a")
#g.add_t("b")
#g.set_ini("P")
#g.add_regole("P", ("a", "b", "aPa", "bPb"))
#print(g.genera_stringa())

#print(g.genera_nIterazioni_random(15))
#g.add_albero(5)

#g.stampa_albero()

print("Stai per creare una grammatica ")
f = Grammatica()

#nelle funzioni seguenti viene usato strip() per rimuovere
#eventuali spazi bianchi

def aggiungi_nt():
	i = str(input("Inserisci un simbolo, # per terminare ")).strip()
	while i != "#":
		if i != "#":
			f.add_nt(i)
		i = str(input("Inserisci un simbolo, # per terminare ")).strip()
		

def aggiungi_t():
	i = str(input("Inserisci un simbolo, # per terminare ")).strip()
	while i != "#":
		if i != "#":
			f.add_t(i)
		i = str(input("Inserisci un simbolo, # per terminare ")).strip()
		

def aggiungi_regole():
	print("Inserisci le regole, # per terminare ")
	
	i = str(input("Inserisci un simbolo non terminale ")).strip()
	while i != "#":
		produzioni = []
		print("Inserisci possibili produzioni, # per terminare ")
		
		j = str(input("Inserisci un simbolo terminale o non terminale ")).strip()
		while j != "#":
			if j != "#":
				produzioni.append(j)

			j = str(input("Inserisci un simbolo terminale o non terminale ")).strip()

		if i != "#":
			f.add_regole(i, tuple(produzioni))

		i = str(input("Inserisci un simbolo non terminale ")).strip()

#loop infinito per il menu
ins = -1
while ins != 0:
	print(
		"""
		0 per uscire
		1 per aggiungere simboli non terminali
		2 per aggiungere simboli terminali
		3 per settare il simbolo iniziale
		4 per inserire le regole
		5 per generare una stringa con max n iterazioni
		6 per generare una stringa casuale facendo almeno n iterazioni
		7 per generare un albero di derivazione con n profondità
		8 per stampare la struttura grammaticale
		9 per salvare la grammatica
		10 per caricare una grammatica
		"""
	)
	try:
		ins = int(input("Inserisci la tua scelta "))
	except ValueError:
		print("Inserisci un numero valido ")
		continue

	match ins:
		case 0:
			print("Ciao")
			ins = 0
		case 1:
			try:
				aggiungi_nt()
			except ValueError as err:
				print(err)
				continue
			except TypeError as err:
				print(err)
				continue
				
		case 2:
			try:
				aggiungi_t()
			except ValueError as err:
				print(err)
				continue
			except TypeError as err:
				print(err)
				continue
		case 3:
			try:
				f.set_ini(str(input("Inserisci il simbolo iniziale ")).strip())
			except ValueError as err:
				print(err)
				continue
		case 4:
			aggiungi_regole()
		case 5:
			print(f.genera_stringa(int(input("Inserisci il massimo di iterazioni "))))
		case 6:
			print(f.genera_nIterazioni_random(int(input("Inserisci il numero minimo di iterazioni "))))
		case 7:
			try:
				f.add_albero(int(input("Inserisci la profondità dell'albero ")))
			except ValueError as err:
				print(err)
				continue
			else:
				f.stampa_albero()
		case 8:
			print(f)
		case 9:
			f.salva_grammatica()
		case 10:
			f.carica_grammatica()
		case -1: #ignoro il -1
			pass
		case _:
			print("Simbolo non valido")
