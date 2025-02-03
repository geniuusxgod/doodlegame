# **GDD DoodleGame**

Tento repozitar obsahuje hru, ktorú som vytvoril pre tento projekt, je to prototyp existujúcej hry DoodleJump pre telefóny, ja som ju vytvoril pre počítače.

**Autor**: Afanasiev Pavlo

**Vybraná téma**: One level, but constantly changing

---
## **1. Úvod**
V tejto hre musíme donekonečna stúpať hore, to je cieľom hry, hráč stúpa hore, aby získal čo najväčší počet bodov, cestou ho čakajú platformy, ktoré sa môžu pohybovať aj rúcať, čakajú ho príšery, s ktorými musí bojovať. Hra je robená v koncepte témy, vždy máme jednu úroveň, ale tá sa neustále mení.

### **1.1 Inšpirácia**
<ins>**DoodleJump**</ins>

Doodlejump je hra na telefóny, v ktorej hráč musí donekonečna liezť po platformach, pričom hra má vždy ***jednu úroveň, ktorá sa neustále mení***. Táto hra ma úplne inšpirovala, prevzal som nápad a rozhodol som sa vytvoriť počítačovú verziu tejto hry s niekoľkými menšími zmenami.

<p align="center">
  <img src="https://github.com/geniuusxgod/doodlegame/blob/master/Doodle-Jump.jpg" alt="DoodleJump">
  <br>
  <em>Obrázok 1 Ukážka hry DoodleJump</em>
</p>

### **1.2 Herný zážitok**
Cieľom hry je dostať sa čo najvyššie, skákať po platformach, zjednocovať príšery a nespadnúť, pričom zjednotenie príšery možno vykonať pomocou posilňovača alebo zabitím príšery.

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk.
- **PyCharm 2024.1**: vybrané IDE.

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč sa ovláda pomocou klávesnice. Skáče donekonečna, odstrkuje sa z platform, na platformach sú boostery, ktoré mu pomáhajú dostať sa rýchlejšie vyššie, a mince, za ktoré si neskôr môžete v obchodoch kúpiť štít, ktorý zachraňuje pred príšerami.

### **2.2 Interpretácia témy (Swarms - príklad témy)**
**One level, but constantly changing** - hra má len jednu úroveň, ktorá sa neustále mení, čo sa realizuje náhodným objavovaním platforiem, náhodným generovaním boostrov, mincí a príšer. To je celá pointa, že úroveň sa mení v priebehu jej prechádzania.

### **2.3 Základné mechaniky**
- **Platformy** - na mape sa nachádzajú platformy, ktoré pomáhajú hráčovi pohybovať sa nahor. Generujú sa náhodne a existujú tri typy platforiem (statické, pohyblivé a rozbíjajúce sa).
- **Bonusové predmety**: hráč môže na mape zbierať predmety, ktoré mu pridajú *rychlost*. Sú tri typy: *jetpack, trampolína a pružina*.
- **Mince** - za mince v obchode si môžete kúpiť užitočné predmety.
- **Hráč môže likvidovať nepriateľov**: hráč strieľa guľky, keď guľka zasiahne príšeru, tá zomrie.

### **2.4 Návrh tried**
- **Game**: trieda, v ktorej sa bude nachádzať hlavná herná logika (úvodná obrazovka, herná slučka, vyhodnotenie hry, ...).
- **Player**: trieda reprezentujúca hráča, ovládanie hráča, vykreslenie postavy a schopnosti.
- **Monsters**: trieda nepriateľov, ich herná logika a pohyb smerom k hráčovi, vykreslenie postáv a schopnosti.
- **Power_ups**: trieda boosterov, ich vykreslenie a schopnosti.
- **Coins**: trieda coinov, ich vyskreslenie.
- **Main_menu**: trieda, ktorá popisuje prechody do hry alebo do obchodu.
- **Shop**: trieda, v ktorej si môžete kúpiť boostery.
- **Play_again_menu**: trieda, v ktorej môžeme po strate postavy začať hru znova.
- **Platforms**: trieda, ktorá popisuje logiku pohybu platforiem a ich kreslenie.

---
## **3. Grafika**

### **3.1 Interpretácia témy (Swarms - príklad témy)**
Hra je veľmi minimalistická, assety použité ako v pôvodnej hre, že monštrá, že hráč a platformy, pridané nové objekty(mince) ktoré nie sú v pôvodnej, ich sprites boli prevzaté z itch.io. Vykonané v 2D. 

<p align="center">
  <img src="https://github.com/geniuusxgod/doodlegame/blob/master/assets/player/right.png" alt="Player">
  <br>
  <em>Obrázok 2 Ukážka spritu hraca</em>
</p>

<p align="center">
  <img src="https://github.com/geniuusxgod/doodlegame/blob/master/monster.png" alt="Monster">
  <br>
  <em>Obrázok 3 Ukážka spritu monstra</em>
</p>

<p align="center">
  <img src="https://github.com/geniuusxgod/doodlegame/blob/master/booster.png" alt="Monster">
  <br>
  <em>Obrázok 4 Ukážka spritu boostera</em>
</p>

### **3.2 Dizajn**
V hre sa použili assety spritov z pôvodnej hry, ktoré som našiel (https://www.spriters-resource.com/mobile/doodlejump/sheet/51424/), pre mince sa použili sprites z itchio assetu (https://totuslotus.itch.io/pixel-coins), ktoré celkom dobre zapadajú do konceptu hry.

<p align="center">
  <img src="https://github.com/geniuusxgod/doodlegame/blob/master/game.png" alt="Game dizajn">
  <br>
  <em>Obrázok 5 Ukážka dizajnu hry</em>
</p>

---
## **4. Zvuk**

### **4.1 Zvuky**
Zvuky v hre boli podobne orientované na originalne zvuky z hry, pričom boli opätovne použité voľne dostupné assety vo forme (https://www.sounds-resource.com/mobile/doodlejump/sound/1636/), z ktorých boli vybrane vsetci zvuky.

---
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
Používateľské rozhranie bolo orientované do ostatného grafického štýlu a úvodná obrazovka obsahovuje možnosť spustiť a ukončiť hru, a prejst do obchodu.

<p align="center">
  <img src="https://github.com/geniuusxgod/doodlegame/blob/master/menu.png" alt="Menu dizajn">
  <br>
  <em>Obrázok 6 Ukážka dizajnu menu</em>
</p>

### **5.2 Ovládanie**
<ins>**Klávesnica**</ins>
- **Klávesy šípok**: pohyb hráča po mape.
- **Medzernik**: vystrel.
- **Z**: aktivivat booster z obchodu.

<ins>**Myš**</ins> 
- **Ľavé tlačidlo**: výstrel.
