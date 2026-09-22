import tkinter as tk
from PIL import Image, ImageTk
import winsound
import json
import random

class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")#crée le titre
        self.frame = tk.Frame(self.root) #crée une fenêtre 
        self.frame.pack()
        self.game = Game(self.frame) #crée un element de type Game

    def play(self):#lance la partie
        self.game.animation() #lance l'animation
        self.keymanagement() #lance keymanagement
        self.root.bind("<KeyPress-Escape>", self.exitgame) #bind la touche echap a exitgame
        self.root.bind("<KeyPress-k>", self.game.sound2) #bind la touche k a sound2
        self.root.mainloop()

    def exitgame(self, event):#Met fin à la partie
        self.game.defender.alive = False #passe le defender de vie à mort
        self.game.canvas.delete('all') #supprime tout les element du canvas
        self.game.entername() #appel la fonction entername

    def keymanagementRL(self):#permet de gerer les deplacement de droite a gauche
        for key in self.keys: #key sont les clés du dictionnaire keys key=["space", "Right", "Left"]
            if self.keys[key]:#les cles ont pour valeur True or False
                if key == "Right":
                    self.game.defender.move_in(self.game.defender.move_delta)#lance la fonction move_in
                elif key == "Left":
                    self.game.defender.move_in(-self.game.defender.move_delta)#lance la fonction move_in
        self.root.after(15, self.keymanagementRL)#repete la fonction apres 15ms

    def keymanagementSP(self):#permet de gerer les tirs
        for key in self.keys:#key sont les clés du dictionnaire keys key=["space", "Right", "Left"]
            if self.keys[key]:#les cles ont pour valeur True or False
                if key == "space":
                    self.game.defender.fire()#lance la fonction fire de defender
        self.root.after(120, self.keymanagementSP)#repete la fonction apres 120ms contrairement a keymanagementRL afin de ne pas tiré tout les balle d'un seule cout

    def press(self, event):
        self.keys[event.keysym] = True #met la valeur True dans la key qui est l'event

    def release(self, event):
        self.keys[event.keysym] = False #met la valeur False dans la key qui est l'event

    def keymanagement(self): #sert a bind les touches

        self.drn = ["space", "Right", "Left"]
        self.keys = dict.fromkeys(self.drn, False)#creé un dictionaire de clé tableaux avec comme valeurs False

        for key in self.keys:
            self.root.bind("<KeyPress-%s>" % key, self.press)#bind les clés du dictionaire en press pour lancer la fonction press
            self.root.bind("<KeyRelease-%s>" % key, self.release)#bind les clés du dictionaire en release pour lancer la fonction release
                                                                #effectue pour chaque clés

        self.keymanagementRL()#appel keymanagementRL
        self.keymanagementSP()#appel keymanagementSP


class Game(object):
    def __init__(self, frame):
        self.frame = frame
        self.fleet = Fleet()#cree un element de type Fleet
        self.defender = Defender()#cree un element de type Defender
        self.scores = score("a", 0)#cree un element de type score avec comme nom 'a' et score 0
        self.resultats = resultat()#cree un element de type resultat
        self.score = 0 
        self.height = 800 #hauteur de la frame
        self.nbalienalive = self.fleet.fleet_size #permet de connaitre le nombre d'alien en vie
        self.width = self.fleet.get_width() #permet de récuperer la taille de la width definie dans la fonction get_width dans la class Fleet
        self.canvas = tk.Canvas(
            self.frame, height=self.height, width=self.width, bg="black")#crée le fond noir
        self.txtscore = self.canvas.create_text(
            20, 30, text="Score : "+str(self.score), fill="white", font=("Game over", 60), anchor='w')#creer le texte avec le score
        self.shipimgmin = Image.open("ship.png")#----------------\
        self.photoshipmin = ImageTk.PhotoImage(self.shipimgmin)#-/Permet l'utilisation d'une image au format png/jpeg/jpg
        self.rect_idmin1 = self.canvas.create_image(
            self.width-1*(self.fleet.alien_width/2), self.fleet.alien_width/2, image=self.photoshipmin)#----\
        self.rect_idmin2 = self.canvas.create_image(
            self.width-3*(self.fleet.alien_width/2), self.fleet.alien_width/2, image=self.photoshipmin)#----|---->crée des mini image du defender en haut a droite de l'ecrans correspondant au vie restante qui sont de 3 au depart
        self.rect_idmin3 = self.canvas.create_image(
            self.width-5*(self.fleet.alien_width/2), self.fleet.alien_width/2, image=self.photoshipmin)#----/
        self.fleet.install_in(self.canvas) #lance l'instalation des fleet
        self.defender.install_in(self.canvas) #lance l'instalation du Defender
        self.sound()#lance le fonction soud qui lance du son
        self.canvas.after(5, self.touchmanagement) #lance la fonction touchmanagement apres 5ms
        self.canvas.pack()

    def sound(self):#sert a lancé du son
        winsound.PlaySound("1.wav", winsound.SND_ASYNC)
        self.canvas.after(327005, self.sound)#relance sound apres 327005ms soit le temps de la musique

    def sound2(self, event):#sert a lancé du son apres un event
        winsound.PlaySound("2mdr.wav", winsound.SND_ASYNC)# winsound.SND_ASYNC permet de jouer la musique et de lancer le jeux en meme temps
        self.canvas.after(168005, self.sound)#relance sound apres 168005ms soit le temps de la musique

    def animation(self):#effectue l'animation
        self.fleet.move_in(self.canvas)#effectue le movement du fleet
        self.canvas.after(10, self.animation)#relance animation après 10ms
#Rayan
    def inscripscores(self):#sert a inscrire le score
        self.resultats2 = self.resultats.fromFile("scores.json") #crée un tableaux de dictionnaire a partir de scores.json
        self.resultats2.ajout(self.scores) #ajoute scores au tableaux
        self.resultats2.toFile("scores.json") #met le tableaux dans le fichier scores.json
        self.affichescores() #lance affichescores

    def affichescores(self):#sert a afficher les scores dans l'ordre croisant et jusqu'a 10 maximum
        chaine = ""
        resultat3 = self.resultats.fromFile("scores.json") #met le tableaux de score.json dans resultat3
        nomjmax = ""
        nbpointmax = -10
        if (len(resultat3.lesscores) <= 10):#----------------------------------Permet de prendre les scores dans l'ordre croissant si il y moin de 10 score
            for i in range(len(resultat3.lesscores)):
                for j in range(len(resultat3.lesscores)):
                    if (resultat3.lesscores[j].nbpoint >= nbpointmax):
                        nbpointmax = resultat3.lesscores[j].nbpoint
                        nomjmax = resultat3.lesscores[j].nomj
                        a = j
                chaine += str(nomjmax)+"  "+str(nbpointmax)+"\n"
                resultat3.lesscores[a].nbpoint = -10
                resultat3.lesscores[a].nomj = ""
                nbpointmax = -10#-----------------------------------------------
        else:#------------------------------------------------------------------Permet de prendre les 10 meilleurs scores dans l'ordre croissant
            for i in range(10):
                for j in range(len(resultat3.lesscores)):
                    if (resultat3.lesscores[j].nbpoint >= nbpointmax):
                        nbpointmax = resultat3.lesscores[j].nbpoint
                        nomjmax = resultat3.lesscores[j].nomj
                        a = j
                chaine += str(nomjmax)+"  "+str(nbpointmax)+"\n"
                resultat3.lesscores[a].nbpoint = -10
                resultat3.lesscores[a].nomj = ""
                nbpointmax = -10#-----------------------------------------------
        self.canvas.create_text(100, 100, anchor="nw", text="Best Scores : ", font=(
            "Game over", 75), fill="white")#ecris best scores :
        self.canvas.create_text(410, 105, anchor="nw", text=chaine, font=(
            "Game over", 70), fill="white")#ecris chaine qui est les meilleurs scores

    def death(self):#s'execute sous certaine condition dans touchmanagement
        self.defender.alive = False
        self.fleet.stopfunction = 1 #sert a areter des boucles sur des fonction dans fleet
        self.defender.stopfunction = 1 #sert a areter des boucles sur des fonction dans defender
        self.canvas.delete('all') #delete toute les objet du canvas
        self.entername() #lance la fonction entername
#Rayan
    def getname(self): #permet de récupérer le nom du joueur avec certaine condition
        self.name = self.entry1.get() #recupere la valeur dans entry1 et la met dans self.name
        if (len(self.name) < 3 or len(self.name) > 15): #verifie si le nom est composé de 3 caractaire ou plus et de 15 caractaire ou moin
            label3 = tk.Label(
                self.root1, text='accept any name with : name>1 and name<=15')#afficher un message pour indiquer que le nom ne correspond pas au condition requise de validation
            label3.config(font=('helvetica', 10))
            self.canvas1.create_window(200, 220, window=label3)
        else:#si la condition sont bonne 
            self.root1.destroy()#detruit la fenetre demandans le nom
            self.scores.set_nomj(self.name)#inscript le nom dans l'element de type score
            self.inscripscores()#appel inscripscore

    def entername(self):#lance la fentetre pour rentrer son nom
        self.root1 = tk.Tk()
        self.canvas1 = tk.Canvas(
            self.root1, width=400, height=300, relief='raised')#creer une fenetre
        self.canvas1.pack()
        label2 = tk.Label(self.root1, text='Get your name:')
        self.canvas1.create_window(200, 100, window=label2)#creer un texte
        self.entry1 = tk.Entry(self.root1)#creer une entry pour inser un nom
        self.canvas1.create_window(200, 140, window=self.entry1)#place l'entry dans la fenetre
        button1 = tk.Button(self.root1, command=self.getname, text='Get your name',
                            bg='brown', fg='white', font=('helvetica', 9, 'bold'))#creer un bouton qui quand appuiyer lance self.getname fonction du dessus
        self.canvas1.create_window(200, 180, window=button1)#place le texte dans la fenetre

    def actscore(self):#permet dactualiser le score
        self.canvas.delete(self.txtscore)#detruit le texte du score
        self.txtscore = self.canvas.create_text(
            20, 30, text="Score : "+str(self.score), fill="white", font=("Game over", 60), anchor='w')#recrer un nouveaux texte du score avec la valeur ajour
        self.scores.set_nbpoint(self.score)#inscript cette nouvelle valeur dans l'element de type score

    def nextround(self):#permet de lancerune nouvelle vague de fleet apres la mort de tout les alien
        self.fleet.stopfunction = 1 #permet d'areter les fonction de fleet
        self.fleet = Fleet() #remplace l'element de type Fleet par un nouvelle element de type Fleet
        self.fleet.aliens_inner_gap += 1 #augment la vittesse des alien apres chaque vague
        for i in self.defender.fired_bullets: 
            self.canvas.delete(i.rect_id) #delete les bullet
            i.coord_y=-30   #
            i.coord_x=0     #les remet a la position de depart
            i.install_in(self.canvas) # reinstale les bullets
        self.fleet.install_in(self.canvas) #install le nouveaux Fleet
        
    def touchmanagement(self): #permet de gerer les colision et donc les conditions de fin de partie
        self.max_alien_y = -10              #
        for i in self.fleet.aliens_fleet:   #
            if (i.y >= self.max_alien_y):   # Permet de connaitre le y max des aliens
                self.max_alien_y = i.y      #
        if (self.fleet.stopfunction==0 and 
            (self.defender.nbvie == 0 or 
            (self.max_alien_y+self.fleet.alien_height/2 >= self.defender.coorddefender_y-self.defender.height/2 and 
            self.defender.alive==True))):#permet de verifier le nombre de vie et de savoir si le Fleet a ateit le y du Defender
            self.death() #appel la fonction death
        for bullet in self.defender.fired_bullets:
            for alien in self.fleet.aliens_fleet:
                if ((bullet.coord_x > alien.x-self.fleet.alien_width/2 and
                    bullet.coord_x < alien.x+self.fleet.alien_width/2 and
                    bullet.coord_y > alien.y-self.fleet.alien_height/2 and
                    bullet.coord_y < alien.y+self.fleet.alien_height/2 and
                    alien.alive == True and bullet.alive == True) or (
                    bullet.coord_x+bullet.width > alien.x-self.fleet.alien_width/2 and
                    bullet.coord_x-bullet.width < alien.x+self.fleet.alien_width/2 and
                    bullet.coord_y+bullet.width > alien.y-self.fleet.alien_height/2 and
                    bullet.coord_y-bullet.width < alien.y+self.fleet.alien_height/2 and
                    alien.alive == True and bullet.alive == True)): #permet de gerer les colision entre les bullets du defender et les alien a condition que les 2 soit vivant

                    alien.alive = False
                    self.score += 10
                    self.actscore() #appel actscore qui actualise le score
                    alien.canvas.delete(alien.rect_id) #delete l'alien
                    alien.x = -10 #move c'est coordonnées en dehors de l'écrans
                    alien.y = -10 #move c'est coordonnées en dehors de l'écrans
                    bullet.alive = False #le met en mort
                    bullet.canvas.delete(bullet.rect_id) #delete le bullet
                    bullet.coord_y = -30 #move c'est coordonnées en dehors de l'écrans
                    bullet.install_in(self.canvas) #reinstale le bullet
                    bullet.alive = True #le remet en vie et donc utilisable
                    self.nbalienalive -= 1 #elever 1 au nombre d'alien vivant
                    if (self.nbalienalive == 0): #si le nombre d'alien ateint 0
                        self.nbalienalive = self.fleet.fleet_size #on remet au nombre d'alien
                        self.nextround() #on lance nextround
        for bullet in self.fleet.bullet:
            if ((bullet.coord_x > self.defender.coorddefender_x-self.defender.width/2 and
                bullet.coord_x < self.defender.coorddefender_x+self.defender.width/2 and
                bullet.coord_y > self.defender.coorddefender_y-self.defender.width/2 and
                bullet.coord_y < self.defender.coorddefender_y+self.defender.width/2 and
                bullet.alive == True) or (
                bullet.coord_x+bullet.width > self.defender.coorddefender_x-self.defender.width/2 and
                bullet.coord_x < self.defender.coorddefender_x+self.defender.width/2 and
                bullet.coord_y > self.defender.coorddefender_y-self.defender.width/2 and
                bullet.coord_y+bullet.width < self.defender.coorddefender_y+self.defender.width/2 and
                    bullet.alive == True)):#permet de gerer les colision entre les bullets alien et le defender a condition la balle soit vivante

                self.defender.nbvie -= 1 #ont enleve un point de vie au defender
                if (self.defender.nbvie == 2):
                    self.canvas.delete(self.rect_idmin3)#suprime la mini image du defender afin de nen laisser que 2
                if (self.defender.nbvie == 1):
                    self.canvas.delete(self.rect_idmin2)#suprime la mini image du defender afin de nen laisser que 1
                bullet.alive = False
                bullet.canvas.delete(bullet.rect_id) #delete la bullet
                bullet.coord_y = 900 #met cest coordonée en dehord de l'écrans
                bullet.install_in(self.canvas) # et le reinstale 
                bullet.alive = True #puis revient a la vie
        self.canvas.after(10, self.touchmanagement) #cette fonction s'appelle elle meme toute les 10ms


class Fleet(object):
    def __init__(self):
        self.stopfunction = 0 #permet d'areter des fonction/enpecher le déclanchement
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 1 #vittesse
        self.aliens_direction = 1 #direction   Gauche=-1/Droite=1
        self.alien_x_delta = 73/2 #posistion d'origine du 1er l'alien
        self.alien_y_delta = 100  #posistion d'origine du 1er l'alien
        self.alien_height = 53 #taille de l'image de l'alien
        self.alien_width = 73  #taille de l'image de l'alien
        self.fleet_size = self.aliens_lines * self.aliens_columns #nombre d'alien
        self.aliens_fleet = []
        self.bullet = []
        self.bullet_size = 4 #nombre de bullet donc 4 tirs max simultané
        self.shootability = [-10]*self.aliens_columns #crées un tableau de taille 10 remplis de -10 qui serviras a connaitre l'indice des alien cappable de tirer soit l'alien le plus bas de chaque colone
        for i in range(0, self.bullet_size): #remplis le tableaux self.bullet de bullet  blanc
            self.bullet.append(Bullet())
            self.bullet[i].collor = "white"
        for i in range(0, self.fleet_size): #remplis le tableaux self.aliens_fleet d'alien
            self.aliens_fleet.append(Alien())
        

    def get_width(self): #permet de connaitre la width du canvas
        return ((self.aliens_columns*self.alien_width)*(3/2)) #la taille est de 1.5 fois la taille du fleet

    def install_in(self, canvas):#permet d'installer le fleet
        self.canvas = canvas
        a = 1 #compteur
        for m in self.aliens_fleet:
            if (a % (self.aliens_columns) == 0): #permet de verifier si on doit retourner a la ligne 
                m.install_in(self.canvas, self.alien_x_delta,
                             self.alien_y_delta)#installe l'alien
                m.x = self.alien_x_delta #met les coordonées de self.alien_x_delta dans les coordonées de l'alien 
                m.y = self.alien_y_delta #met les coordonées de self.alien_x_delta dans les coordonées de l'alien
                self.alien_y_delta += self.alien_height #augmente le y car retour a la ligne
                self.alien_x_delta = self.alien_width/2 #augmente le x pour poser le prochaine alien

            else:
                m.install_in(self.canvas, self.alien_x_delta,
                             self.alien_y_delta)#installe l'alien
                m.x = self.alien_x_delta #met les coordonées de self.alien_x_delta dans les coordonées de l'alien
                m.y = self.alien_y_delta #met les coordonées de self.alien_x_delta dans les coordonées de l'alien
                self.alien_x_delta += self.alien_width #augmente le x pour poser le prochaine alien
            m.id = a #met le compteur en tant que id
            a += 1 #incrementation du compteur
        for i in self.bullet: #ont instale les bullet du fleet
            i.install_in(self.canvas) #install la bullet
            self.canvas.move(i.rect_id, 0, 900) #la move en dehors de l'écrans
            i.coord_y = 900 #met ces coordonées en dehor de l'écrans

        self.fire()#lance la fonction fire

    def move_in(self, canvas):#permet le movement des aliens
        self.canvas = canvas
        y = 0 #le movement efectuer a chaque tape sur le bord
        self.minx = 800 #valeurs absurde afin de garantir de trouver un x min
        self.maxx = 0 #valeurs absurde afin de garantir de trouver un x max
        for i in self.aliens_fleet:#permet de trouver le x max et le x min parmit les aliens vivant
            if (i.alive == True):
                if (i.x < self.minx):
                    self.minx = i.x
                if (i.x > self.maxx):
                    self.maxx = i.x
        if (self.minx-self.alien_width/2 < 0): #modifie la direction et fait augmenter le movement en y quand on tape le bord de gauche
            self.aliens_inner_gap *= -1
            y = 30
        if (self.maxx+self.alien_width/2 > self.get_width()):#modifie la direction et fait augmenter le movement en y quand on tape le bord de droite
            self.aliens_inner_gap *= -1
            y = 30
        self.aliens_inner_gap *= self.aliens_direction #multiplie la vittese par la direction
        for m in self.aliens_fleet: #effectue le movement seulement sur les aliens vivant
            if (m.alive == True):
                m.move_in(self.canvas, self.aliens_inner_gap, y)#effectue le movement

    def fire(self):#permet le tire
        for j in range(0, self.aliens_columns):#remplit le tableaux self.shootability avec l'indice du tableux fleet des alien en fin de colone ou -10 si il y a plus d'alien dans la colone
            maxx = -10
            for i in range(j, self.fleet_size, self.aliens_columns):
                if (self.aliens_fleet[i].y > maxx and self.aliens_fleet[i].alive == True):
                    maxx = self.aliens_fleet[i].id-1
                self.shootability[j] = maxx
                
        a = random.randint(0, 9) #permet de selectioner un element de shootability au hasard
        b = random.randint(1250, 2000) #permet de réexecuter la fonction après b ms afin que les tirs ne soir pas trop régulier
        self.canvas_height = int(self.canvas.cget("height"))
        tmp = 0 #sert a executer une seule fois le if à chaque boucle
        for i in self.bullet:
            if (i.coord_y > self.canvas_height+50 and i.alive == True and tmp == 0): #la balle est consider comme valide si elle est en dehors du canvas en dessous
                tmp = 1 #sert a executer une seule fois le if à chaque boucle
                x = self.aliens_fleet[self.shootability[a]].x-5-i.coord_x #calcule le movement a faire pour déplacer la balle jusqu'a l'alien
                y = self.aliens_fleet[self.shootability[a]].y+53-i.coord_y #calcule le movement a faire pour déplacer la balle jusqu'a l'alien
                i.coord_x = self.aliens_fleet[self.shootability[a]].x-5 #met les nouvelle coordonées de la balle calcul fait juste avant
                i.coord_y = self.aliens_fleet[self.shootability[a]].y+53 #met les nouvelle coordonées de la balle calcul fait juste avant
                self.canvas.move(i.rect_id, x, y) #bouge la balle grace au calcul faite avant
                i.anim() #lance l'animation de movement de la balle
        if (self.stopfunction == 0): #sert a areter la fonction afin quel ne se répete pas
            self.canvas.after(b, self.fire) #repete la fonction après b ms


class Alien(object):
    def __init__(self):
        self.id = None
        self.alive = True
        self.height = 53 #hauter de l'image de l'alien
        self.width = 73 #largeur de l'image de l'alien
        self.x = 0 #coordonée x de l'alien
        self.y = 0 #coordonée y de l'alien

    def install_in(self, canvas, x, y): #permet d'instaler l'image de alien en x,y passer en parametre
        self.canvas = canvas
        self.image = tk.PhotoImage(file='Alien.gif', master=self.canvas)
        self.rect_id = self.canvas.create_image(x, y, image=self.image)

    def move_in(self, canvas, gap, y): #permet le movement de gap,y passer en parametre
        self.canvas = canvas
        self.canvas.move(self.rect_id, gap, y)#effectue le mouvement
        self.x += gap #recalcule les nouvelle coordonées
        self.y += y #recalcule les nouvelle coordonées

#Rayan
class Defender(object):
    def __init__(self):
        self.alive = True
        self.stopfunction = 0 #permet d'areter des fonction/enpecher le déclanchement
        self.nbvie = 3 #nombre de vie
        self.width = 50 #taille de l'image du defender
        self.height = 48 #taille de l'image du defender
        self.move_delta = 10 #mouvement à faire
        self.bulletDirection = -1 #direction des bullet  de Haut En Bas=1/Bas En Haut=-1
        self.max_fired_bullets = 8 #nombre max de bullet simultané
        self.fired_bullets = [] 
        self.coorddefender_x = 0 #coordonées du defender
        self.coorddefender_y = 0  #coordonées du defender
        for i in range(0, self.max_fired_bullets): #remplis le tableaux self.fired_bullet de bullet et fixe leur direction
            self.fired_bullets.append(Bullet())
            self.fired_bullets[i].direction = self.bulletDirection

    def install_in(self, canvas):#permet d'instaler le defender et ces bullet
        self.canvas = canvas
        self.canvas_width = int(canvas.cget("width"))
        self.canvas_height = int(canvas.cget("height"))

        self.shipimg = Image.open("ship.png")#permet d'utiliser une image png/jpeg/jpg garce a la bibliothéque Pillow
        self.photoship = ImageTk.PhotoImage(self.shipimg)
        self.rect_id = self.canvas.create_image(
            self.canvas_width/2, self.canvas_height-50, image=self.photoship)#place le defender au centre en bas du canvas

        self.coorddefender_x = self.canvas_width/2 #enregiste les coordonées du defender
        self.coorddefender_y = self.canvas_height-50 #enregiste les coordonées du defender
        a = 0
        for i in self.fired_bullets:#instale les bullet
            i.id = a
            i.install_in(self.canvas)#instale la bullet
            a += 1

    def move_in(self, dx):#permet le mouvement du defender
        if (self.coorddefender_x+self.width/2+dx <= self.canvas_width and self.coorddefender_x+dx-self.width/2 >= 0):#permet d'éviter que le defender ne depasse des bords
            self.canvas.move(self.rect_id, dx, 0)#bouge le defender de dx qui correspond a self.move_delta ou -self.move_delta
            self.coorddefender_x += dx #recalcul les nouvelle coordonées

    def fire(self):#permet le tire du defender
        if (self.stopfunction == 0): #permet d'empecher les tirs
            a = 0 #permet de passer une seule fois dans le if a chaque boucle
            for i in self.fired_bullets:
                if (i.coord_y < -21 and i.alive == True and a == 0): #si les balle sont en dehors du canvas en haut alors la balle est utilisable
                    a = 1 #permet de passer une seule fois dans le if a chaque boucle
                    x = (self.coorddefender_x-5)-i.coord_x #calcul le mouvement a faire pour aller jusqu'aux defender
                    y = (self.coorddefender_y-40)-i.coord_y #calcul le mouvement a faire pour aller jusqu'aux defender
                    i.coord_x = self.coorddefender_x-5 #met le coordonées de la bullet au niveaux du defender
                    i.coord_y = self.coorddefender_y-40 #met le coordonées de la bullet au niveaux du defender
                    self.canvas.move(i.rect_id, x, y) #effectue le mouvement calculer avant
                    i.anim() #lance l'animation
#Rayan
class Bullet(object):
    def __init__(self):
        self.collor = "red"
        self.width = 10 #taille de la bullet / radius
        self.speed = 6 #vitesse de la balle
        self.id = None
        self.coord_x = 0 #coordonée x de la balle
        self.coord_y = -30 #coordonée y de la balle
        self.direction = 1 #direction du tir de Haut En Bas=1/Bas En Haut=-1
        self.alive = True

    def install_in(self, canvas):#permet l'instaltion des bullet
        self.canvas = canvas
        self.canvas_height = int(self.canvas.cget("height"))
        self.rect_id = self.canvas.create_oval(
            self.coord_x, self.coord_y, self.coord_x+self.width, self.coord_y+self.width, fill=self.collor)#cree la balle

    def anim(self):#permet l'animation du bullet
        self.move_in()#bouge la bullet
        self.coord_y += self.speed*self.direction #recalcule les nouvelle coordonée de la bullet
        if (self.coord_y >= -20 and self.coord_y <= self.canvas_height+50): #si la bullet est toujour a l'écrans alors relacer la fonction
            self.canvas.after(10, self.anim)#relance la fonction après 10ms

    def move_in(self):#permet le move de la bullet
        self.canvas.move(self.rect_id, 0, self.speed*self.direction)#bouge la bullet


class score(object):#permet d'enregistrer le score
    def __init__(self, nomj, nbpoint):
        self.nomj = nomj
        self.nbpoint = nbpoint

    def set_nomj(self, nomj):
        self.nomj = nomj

    def set_nbpoint(self, nbpoint):
        self.nbpoint = nbpoint

    def get_nomj(self):
        return self.nomj

    def get_nbpoint(self):
        return self.nbpoint

    def toFile(self, nomfichier):#ecris dans le fichier
        f = open(nomfichier, "w")
        json.dump(self.__dict__, f)
        f.close()

    @classmethod
    def fromFile(cls, nomfichier): #lis le fichier et le place dans scorenew
        f = open(nomfichier, "r")
        d = json.load(f)
        scorenew = score(d["nomj"], d["nbpoint"])
        f.close()
        return scorenew


class resultat(object):#permet d'enregister plusieur scores
    def __init__(self):
        self.lesscores = []

    def ajout(self, score):
        self.lesscores.append(score)

    def __str__(self):
        chaine = str(self.lesscores[0])
        for e in self.lesscores[1:]:
            chaine = chaine + "," + str(e)
        return chaine

    def toFile(self, nomfichier):#permet d'écrire sur le ficher avec un tableaux de dictionaire
        f = open(nomfichier, "w")
        tab = []
        for l in self.lesscores:
            d = {}
            d["nomj"] = l.nomj
            d["nbpoint"] = l.nbpoint
            tab.append(d)
        json.dump(tab, f)
        f.close()

    @classmethod
    def fromFile(cls, nomfichier): #permet la lecture du fichier en le mettant dans une variable
        f = open(nomfichier, "r")
        jsp = json.load(f)
        tab = []
        for d in jsp:
            j = score(d["nomj"], d["nbpoint"])
            tab.append(j)
        resultats = resultat()
        resultats.lesscores = tab
        f.close()
        return resultats

SpaceInvaders().play()