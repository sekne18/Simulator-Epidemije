import risar
import random
from math import pi, sin, cos, radians


class Oseba:

   def __init__(self):
      self.hitrost = round(random.uniform(0,4),2)
      self.kot = random.randint(0,360)
      self.x, self.y = random.randint(4,risar.maxX-4), random.randint(4,risar.maxY-4)
      self.krog = risar.krog(self.x,self.y,5)
      self.okuzen = False
      self.prebolel = False
      self.dnevi_zdravljenja = 0
      self.dnevi_izolacije = 0
      self.v_izoliciji = False

   def premik(self, osebe):
      if self.v_izoliciji:
         self.dnevi_izolacije += 1
         if self.dnevi_izolacije >= 100:

            self.v_izoliciji = False
            self.dnevi_izolacije = 0
            risar.sprazni(self.krog)

         for o in osebe:
            if abs(o.x - self.x) < 20 and abs(o.y - self.y) < 20:
               o.kot -= 180
      else:
         self.kot += random.randint(-20, 20)
         phi = radians(90 - self.kot)
         nx = self.x + self.hitrost * cos(phi)
         ny = self.y - self.hitrost * sin(phi)

         if (nx > risar.maxX - 5 or  nx < 5):
            self.kot = 360 - self.kot
            phi = radians(90 - self.kot)
            nx = self.x + self.hitrost * cos(phi)
            ny = self.y - self.hitrost * sin(phi)

         if (ny > risar.maxY - 5 or ny < 5):
            self.kot = 180 - self.kot
            phi = radians(90 - self.kot)
            nx = self.x + self.hitrost * cos(phi)
            ny = self.y - self.hitrost * sin(phi)

         self.x, self.y = nx, ny
         risar.premakni_na(self.krog, self.x, self.y)

   def okuzi_se(self):
      risar.spremeni_barvo(self.krog, risar.rdeca)
      self.okuzen = True

   def okuzi_bliznje(self, osebe):
      for o in osebe:
         if self.okuzen:
            if o.y != self.y and o.x != self.x:
               if abs(o.x - self.x) < 11 and abs(o.y - self.y) < 11:
                  if not o.okuzen and not o.prebolel:
                     o.okuzi_se()
                     nijz.sporoci_okuzbo()

   def zdravi_se(self):
      if self.okuzen:
         self.dnevi_zdravljenja += 1
         if self.dnevi_zdravljenja >= 150:
            self.okuzen = False
            self.prebolel = True
            risar.spremeni_barvo(self.krog, risar.zelena)
            nijz.sporoci_ozdravitev()

   def vrni_krog(self):
      return self.krog

   def je_izolirana(self):
      return self.v_izoliciji

   def v_izolacijo(self):
      risar.zapolni(self.krog, risar.rumena)
      self.v_izoliciji = True

class NIJZ:
   def __init__(self):
      self.okuženih = 0
      self.ozdravelih = 0
      self.dan = 1
      self.prejsnidan = 0
      self.prejsni_dan_okuzenih = 0
      self.prejsni_dan_ozdravelih = 0

   def sporoci_okuzbo(self):
      self.okuženih += 1

   def sporoci_ozdravitev(self):
      self.ozdravelih += 1
      self.okuženih -= 1

   def porocaj(self):
      self.dan += 1
      risar.crta(self.prejsnidan, risar.maxY - self.prejsni_dan_okuzenih, self.dan, risar.maxY - self.okuženih, risar.rdeca)
      self.prejsnidan = self.dan
      self.prejsni_dan_okuzenih = self.okuženih

      risar.crta(self.prejsnidan, risar.maxY - self.prejsni_dan_ozdravelih, self.dan, risar.maxY - self.ozdravelih, risar.zelena)
      self.prejsni_dan_ozdravelih = self.ozdravelih

nijz = NIJZ()




import risar

def main():

    from unittest.mock import Mock
    from itertools import count

    if hasattr(Oseba, "premik") and Oseba.premik.__code__.co_argcount == 1:
        Oseba.premik = lambda self, osebe, f=Oseba.premik: f(self)

    for method in ("premik", "okuzi_se", "okuzi_bliznje", "zdravi_se"):
        if not hasattr(Oseba, method):
            setattr(Oseba, method, Mock())

    globals().setdefault("nijz", None)

    osebe = [Oseba() for _ in range(100)]
    for oseba in osebe[:5]:
        oseba.okuzi_se()
    for oseba in osebe:
        if hasattr(Oseba, "vrni_krog") and hasattr(Oseba, "v_izolacijo"):
            oseba.vrni_krog().setOnClick(oseba.v_izolacijo)

    for cas in count():
        for oseba in osebe:
            oseba.zdravi_se()
            oseba.okuzi_bliznje(osebe)
            oseba.premik(osebe)
        if nijz and cas % 10 == 0:
            nijz.porocaj()
        risar.cakaj(0.02)

main()

