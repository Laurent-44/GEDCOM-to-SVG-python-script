import gedcompy
import drawsvg as dw
from PIL import Image, ImageFont
import datetime
import os
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gedcom", type=str, help="GEDCOM file")
parser.add_argument("-i", "--indi", type=str, help="INDI number of the root of the tree, default = \"I1\"")
parser.add_argument("-r", "--root", type=int, help="renumber the root number", default = 1)
parser.add_argument("-s", "--size", type=str, help="tree size : 'A4', 'A3', 'A2', 'A2', 'A1', 'A0' or 'custom0'/1")
parser.add_argument("-c", "--color", type=bool, help="colorize the tree", default=True)
parser.add_argument("-n", "--number", type=bool, help="add the anhentafel numbers", default=True)
parser.add_argument("-p", "--photo", type=bool, help="add the photo", default=True)
# Parse the command-line arguments
args = parser.parse_args()

# Configuration choices
#
if args.gedcom :
  gedcom_name = args.gedcom
else :
  gedcom_name = 'gedcom_file.ged'

if args.indi :
  root_indi = args.indi
else :
  root_indi = 'I1'

if args.root :
  root_number = args.root
else :
  root_number = 1

if args.size :
  tree_size = args.size
else :
  tree_size = 'A0'

if args.color :
  with_color = args.color
else :
  with_color = True

if args.number :
  with_number = args.number
else :
  with_number = True

if args.photo :
  with_photo = args.photo
else :
  with_photo  = True

xtrasize = 1
fontf = 'Arial'
fontc = 'ARIALNB.TTF'
fonti = 'ARIALNI.TTF'
mborn = 'né'
fborn = 'née'
at = ' à '

# end of configuration
################################################

if with_color :
  xcolor = ('800000','C05000','800080','000080','003050','600040','005080','300050','404080','603000','305080','000000','603030')
else:
  xcolor = ('000000','000000','000000','000000','000000','000000','000000','000000','000000','000000','000000','000000','000000')

if tree_size == 'custom1':
  tree_width = 90.0
  tree_height = 130.0
  max_gen = 12
  xpos  = (0.8,1.6,2.5,3.5,4.5,7,13.5,18.5,28,39,51.5,69.5)

if tree_size == 'custom2':
  tree_width = 116.0
  tree_height = 188.0
  max_gen = 13
  xpos  = (0.8,1.6,2.5,3.5,4.5,7,13.5,18.5,28,39,52,72,95)

if tree_size == 'A0':
  tree_width = 84.0
  tree_height = 108.8
  max_gen = 12
  xpos  = (0.8,1.6,2.5,3.5,4.5,10,16.5,22,31,41.5,52.5,66.5)
if tree_size == 'A1':
  tree_width = 59.4
  tree_height = 84
  max_gen = 10
  xpos  = (0.8,1.6,2.5,3.5,4.5,10.5,16.5,26,36,46.5)
if tree_size == 'A2':
  tree_width = 42.0
  tree_height = 59.4
  max_gen = 8
  xpos  = (0.7,1.6,2.5,4.5,7,13.5,20,31)
if tree_size == 'A3':
  tree_width = 29.7
  tree_height = 42.0
  max_gen = 6
  xpos  = (0.7,2.5,4.5,7,14.5,22)
if tree_size == 'A4':
  tree_width = 21.0
  tree_height = 29.7
  max_gen = 5
  xpos  = (0.7,2,3.5,6,13)

##############################################################################

def add_person_4lin(dwg, person, gen, n, with_number, xtra, x, y):
  ftsz = ftsz = 19 - gen
  if person.photo is not None and with_photo:
    image = person.photo
    width, height = Image.open(image).size
    # print(image,'size :',str(width),'x',str(height))
    font = ImageFont.truetype(fontc, ftsz+1+xtra)
    xtb = x + font.getlength(ahnentafel[i].name[0]+' '+ahnentafel[i].name[1])
    if height>width:
      ytb = y-2*ftsz
    else :
      ytb = y-ftsz/2-min(80,int(90*height/width))/2
    dwg.append(dw.Image(xtb, ytb, min(int(80*width/height),90), min(80,int(90*height/width)), image, embed=True))
  title = ''
  if 'TITL' in person and gen < 8:
    if person.title is not None :
      title = ' , ' + person.title[:36]
  txt = dw.Text('', x=x, y=y, font_size=8)
  txt.append(dw.TSpan((person.name[0]+' '+person.name[1])[:40],
    font_size=ftsz+1+xtra, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  txt.append(dw.TSpan(title, font_size=ftsz, font_weight='normal', font_style='italic', style='fill:#'+xcolor[gen-1]))
  dwg.append(txt)
  if with_number :
    dwg.append(dw.Text("("+str(n)+")", x=x-18, y=y,
      font_size=16-gen, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  if gen==8 :
    y = y + ftsz
    ystep = ftsz
  else :
    y = y + ftsz*1.1
    ystep = ftsz*1.05
  if 'OCCU' in person :
    if person.occu is not None :
      dwg.append(dw.Text(person.occu[:42], x=x+12, y=y,
        font_size=ftsz, font_style='italic', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
      y = y + ystep
  bir = ''
  if 'BIRT' in person :
    if person.is_male:
      bir = mborn
    if person.is_female:
      bir = fborn
    if 'DATE' in person.birth :
        bir = bir + french(person.birth.date)
    if 'PLAC' in person.birth :
        bir = bir + at + person.birth.place
    dwg.append(dw.Text(bir, x=x, y=y,
      font_size=ftsz, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
    y = y + ystep
  det = ''
  if 'DEAT' in person :
    det = '†'
    if 'DATE' in person.death :
      det = det + french(person.death.date)
    if 'PLAC' in person.death :
      det = det + at + person.death.place
    dwg.append(dw.Text(det, x=x, y=y,
      font_size=ftsz, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))


def add_person_3lin(dwg, person, gen, n, with_number, xtra, x, y):
  ftsz = 9
  occupation = ''
  if 'OCCU' in person :
    if person.occu is not None :
      occupation = ' , ' + person.occu[:(50-int(1.2*len(person.name[0]+person.name[1])))]
  else :
    if 'TITL' in person :
      occupation = ' , ' + person.title[:(50-int(1.2*len(person.name[0]+person.name[1])))]
  if person.photo is not None and with_photo:
    image = person.photo
    width, height = Image.open(image).size
    font = ImageFont.truetype(fontc,ftsz+xtra)
    font1 = ImageFont.truetype(fonti, ftsz-1)
    xtb = (x + font.getlength(ahnentafel[i].name[0]+' '+ahnentafel[i].name[1])
               + font1.getlength(occupation))
    if height>width:
      ytb = y-2*ftsz
    else :
      ytb = y-ftsz/2-min(80,int(90*height/width))/2
    dwg.append(dw.Image(xtb, ytb, min(80*width/height,90), min(80,90*height/width), image, embed=True))
  txt = dw.Text('', x=x, y=y, font_size=ftsz)
  txt.append(dw.TSpan(person.name[0]+' '+person.name[1],
    font_size=ftsz+xtra, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  txt.append(dw.TSpan(occupation, font_size=ftsz-1, font_weight='normal', font_style='italic', style='fill:#'+xcolor[gen-1]))
  dwg.append(txt)
  if with_number :
    dwg.append(dw.Text("("+str(n)+")", x=x-18, y=y,
      font_size=ftsz-1, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  y = y + ftsz-1
  bir = ''
  if 'BIRT' in person :
    if person.is_male:
      bir = mborn
    if person.is_female:
      bir = fborn
    if 'DATE' in person.birth :
        bir = bir + french(person.birth.date)
    if 'PLAC' in person.birth :
        bir = bir + at + person.birth.place
    dwg.append(dw.Text(bir[:60], x=x, y=y,
      font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
    y = y + ftsz-1
  det = ''
  if 'DEAT' in person :
    det = '†'
    if 'DATE' in person.death :
      det = det + french(person.death.date)
    if 'PLAC' in person.death :
      det = det + at + person.death.place
    dwg.append(dw.Text(det[:60], x=x, y=y,
      font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))


def add_person_2lin(dwg, person, gen, n, with_number, xtra, x, y):
  ftsz = 9
  occupation = ''
  if 'OCCU' in person :
    if person.occu is not None :
      occupation = ' , ' + person.occu[:(52-int(1.2*len(person.name[0]+person.name[1])))]
  else :
    if 'TITL' in person :
      occupation = ' , ' + person.title[:(52-int(1.2*len(person.name[0]+person.name[1])))]
  if person.photo is not None and with_photo:
    image = person.photo
    width, height = Image.open(image).size
    xtb = (x + font.getlength(ahnentafel[i].name[0] + ' ' + ahnentafel[i].name[1])
           + font1.getlength(occupation))
    if height>width:
      ytb = y-2*ftsz
    else :
      ytb = y-ftsz/2-min(80,int(90*height/width))/2
    dwg.append(dw.Image(xtb, ytb, min(80*width/height,80), min(80,80*height/width), image, embed=True))
  txt = dw.Text('', x=x, y=y, font_size=ftsz)
  txt.append(dw.TSpan(person.name[0] + ' ' + person.name[1],
                      font_size=ftsz + xtra, font_weight='bold', font_stretch='condensed',
                      style='fill:#' + xcolor[gen - 1]))
  txt.append(dw.TSpan(occupation, font_size=ftsz - 1, font_weight='normal', font_style='italic',
                      style='fill:#' + xcolor[gen - 1]))
  dwg.append(txt)
  if with_number :
    dwg.append(dw.Text("("+str(n)+")", x=x-19, y=y,
      font_size=ftsz-1, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  y = y + ftsz-2.5
  bir = ''
  if 'BIRT' in person :
    if person.is_male:
      bir = mborn
    if person.is_female:
      bir = fborn
    if 'DATE' in person.birth :
        bir = bir + french(person.birth.date)
    if 'PLAC' in person.birth :
        bir = bir + at + person.birth.place
  det = ''
  if 'DEAT' in person :
    det = '†'
    if 'DATE' in person.death :
      det = det + french(person.death.date)
    if 'PLAC' in person.death :
      det = det + at + person.death.place
    if 'BIRT' in person :
      dwg.append(dw.Text(bir[:40]+" "+det[:50], x=x, y=y,
        font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
    else :
      dwg.append(dw.Text(det, x=x, y=y,
        font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  else :
    dwg.append(dw.Text(bir, x=x, y=y,
      font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))


def add_person_2linshort(dwg, person, gen, n, with_number, xtra, x, y):
  ftsz = 9
  dwg.append(dw.Text((person.name[0]+' '+person.name[1])[:32], x=x, y=y,
    font_size=ftsz+xtra, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  if with_number :
    dwg.append(dw.Text("("+str(n)+")", x=x-19, y=y,
      font_size=ftsz-1, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  y = y + ftsz-2
  bir = ''
  if 'BIRT' in person :
    if person.is_male:
      bir = mborn
    if person.is_female:
      bir = fborn
    if 'DATE' in person.birth :
        bir = bir + ' ' + num(person.birth.date)
    if 'PLAC' in person.birth :
        bir = bir + ', ' + person.birth.place[:19]
  det = ''
  if 'DEAT' in person :
    det = '†'
    if 'DATE' in person.death :
      det = det + ' ' + num(person.death.date)
    if 'PLAC' in person.death :
      det = det + ', ' + person.death.place[:19]
    if 'BIRT' in person :
      dwg.append(dw.Text(bir[:25]+" "+det[:30], x=x, y=y,
        font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
    else :
      dwg.append(dw.Text(det[:55], x=x, y=y,
        font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  else :
    dwg.append(dw.Text(bir[:55], x=x, y=y,
      font_size=ftsz-1, font_style='normal', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))


def add_person_1lin(dwg, person, gen, n, with_number, xtra, x, y):
  ftsz = 9
  bir = '\u00A0 ('
  if 'BIRT' in person :
    if 'DATE' in person.birth :
        bir = bir + num(person.birth.date) + ' '
  det = '†'
  if 'DEAT' in person :
    if 'DATE' in person.death :
      det = det + num(person.death.date)
  txt = dw.Text('', x=x, y=y, font_size=ftsz)
  txt.append(dw.TSpan((person.name[0]+' '+person.name[1])[:30]+' ',
    font_size=ftsz+xtra, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))
  txt.append(dw.TSpan(bir[:25]+det[:25] + ')', font_size=ftsz-1, font_weight='normal', style='fill:#'+xcolor[gen-1]))
  dwg.append(txt)
  if with_number :
    dwg.append(dw.Text("("+str(n)+")", x=x-19, y=y,
      font_size=ftsz-1, font_weight='bold', font_stretch='condensed', style='fill:#'+xcolor[gen-1]))


def french(date):
  french_date = date
  if (('JAN' in date) or ('FEB' in date) or ('MAR' in date) or ('APR' in date) or
      ('MAY' in date) or ('JUN' in date) or ('JUL' in date) or ('AUG' in date) or
      ('SEP' in date) or ('OCT' in date) or ('NOV' in date) or ('DEC' in date)) :
    french_date = 'le' + french_date
  french_date = french_date.replace('JAN', 'janv')
  french_date = french_date.replace('FEB', 'févr')
  french_date = french_date.replace('MAR', 'mars')
  french_date = french_date.replace('APR', 'avrl')
  french_date = french_date.replace('MAY', 'mai ')
  french_date = french_date.replace('JUN', 'juin')
  french_date = french_date.replace('JUL', 'juil')
  french_date = french_date.replace('AUG', 'août')
  french_date = french_date.replace('SEP', 'sept')
  french_date = french_date.replace('OCT', 'oct')
  french_date = french_date.replace('NOV', 'nov')
  french_date = french_date.replace('DEC', 'déc')
  french_date = french_date.replace('AFT', 'après')
  french_date = french_date.replace('BEF', 'avant')
  french_date = french_date.replace('CIR', 'env ')
  french_date = french_date.replace('ABT', 'env ')
  french_date = french_date.replace('BET', 'entre')
  french_date = french_date.replace('FROM', 'entre')
  french_date = french_date.replace('AND', 'et')
  french_date = french_date.replace('TO', 'et')
  return french_date

def num(date):
  num_date = date
  num_date = num_date.replace(' JAN ', '.1.')
  num_date = num_date.replace(' FEB ', '.2.')
  num_date = num_date.replace(' MAR ', '.3.')
  num_date = num_date.replace(' APR ', '.4.')
  num_date = num_date.replace(' MAY ', '.5.')
  num_date = num_date.replace(' JUN ', '.6.')
  num_date = num_date.replace(' JUL ', '.7.')
  num_date = num_date.replace(' AUG ', '.8.')
  num_date = num_date.replace(' SEP ', '.9.')
  num_date = num_date.replace(' OCT ', '.10.')
  num_date = num_date.replace(' NOV ', '.11.')
  num_date = num_date.replace(' DEC ', '.12.')
  num_date = num_date.replace('AFT', '>')
  num_date = num_date.replace('BEF', '<')
  num_date = num_date.replace('CIR', '~')
  num_date = num_date.replace('ABT', '~')
  num_date = num_date.replace('BET', '')
  num_date = num_date.replace(' FROM ', '')
  num_date = num_date.replace(' AND ', '/')
  num_date = num_date.replace('AND', '/')
  num_date = num_date.replace(' TO ', '/')
  return num_date

###############################################################################
#
#  sort the person of the database in Ahnentafel order
#

# Parse your file
gedcomfile = gedcompy.parse(gedcom_name)

# Parameters Initialization
root = gedcomfile['@' + root_indi + '@']
# root = list(gedcomfile.individuals)[0]

ahnentafel = [root]
ahnumber = [1]
generation = 1
ahnstop=0

while generation < max_gen:
  ahnstart = ahnstop
  ahnstop = len(ahnentafel)
  if ahnstart == ahnstop : # no new person found, all ancestors are then listed
    generation = generation-1
    break
  for i in range(ahnstart, ahnstop):
    if ahnentafel[i].father is not None:
      ahnentafel.append(ahnentafel[i].father)
      ahnumber.append(2*ahnumber[i])
    if ahnentafel[i].mother is not None:
      ahnentafel.append(ahnentafel[i].mother)
      ahnumber.append(2*ahnumber[i]+1)
  generation = generation + 1

###############################################################################
#
#  build the tree with max_gen generations of persons
#

gen    = 0
xshift = 0
yshift = 15
fac    = 38  # points to cm conversion factor
Tree_SVG = dw.Drawing(tree_width*fac, tree_height*fac, font_family=fontf)

# Title of the tree at the bottom left :
tree_height = tree_height*fac
Tree_SVG.append(dw.Text('arbre généalogique', x=30, y=tree_height-61,
                   font_size=17, font_style='italic', fill='black'))
Tree_SVG.append(dw.Text('sur '+str(max_gen)+' générations, le '+datetime.date.today().strftime("%d %b %Y"), x=30, y=tree_height-46,
                   font_size=11, font_style='italic', fill='black'))
Tree_SVG.append(dw.Text('de '+ahnentafel[0].name[0]+' '+ahnentafel[0].name[1], x=30, y=tree_height-30,
                   font_size=15, font_style='italic', fill='black'))

if tree_size=='A4':
  xpos = xpos + (21,)
if tree_size=='A3':
  xpos = xpos + (29.7,)

for i in range(0,len(ahnentafel)):
  if ahnentafel[i] is not None :
    xshift=0
    yshift=15
    xshftlin=0
    yshftlin=0
    xshftstart=0
    yshftend=0
    yoccu=0
    if ahnumber[i]>=2**gen :
      gen = gen +1
      print ('-----',gen,'ème génération --------------------')
    # update the Ahnentafel number with root_number :
    ahnentfel_number = root_number * 2**(gen-1) + ahnumber[i] % 2**(gen-1)

    if tree_size=='A2' and gen>=7 and ahnentafel[i].is_female :
      xshift = fac*4.1
    if tree_size=='A1' and gen>=7 and ahnentafel[i].is_female :
      xshift = fac*4.1
    if tree_size=='A0' and gen>=8 and ahnentafel[i].is_female :
      xshift = fac*4.1
    if tree_size[:4]=='cust' and gen>=8 and ahnentafel[i].is_female :
      xshift = fac*4.5
    if gen==9 :
      xshift = xshift*1.2
    if gen==10 :
      xshift = xshift*1.3

    # Tree branches drawing
    #-------------------------
    red   = int(192+ gen * (148-192) / max_gen)
    green = int(96 + gen * (192- 96) / max_gen)
    blue  = int(32 + gen * (140- 32) / max_gen)
    treeColor = "#%02X%02X%02X" % (red, green, blue)
    x = fac * xpos[gen - 1] + xshift
    y = (tree_height - 35) * (1 / 2 ** gen + (ahnumber[i] - 2 ** (gen - 1)) / 2 ** (gen - 1)) + yshift
    if gen<=9  or gen < max_gen:
      yend = (tree_height-35)*(1/2**(gen+1)+(ahnumber[i]*2-2**gen)/2**gen)+yshift
      occupation = ''
      if 'OCCU' in ahnentafel[i] :
        if ahnentafel[i].occu is not None and gen <6 :
          yoccu = 16-gen
        if ahnentafel[i].occu is not None and gen==9 :
          occupation = ahnentafel[i].occu[:42]
      if 0 < gen < 6:
        xtb  = (xpos[gen-1]+xpos[gen])*fac/2
        xstart = min(xtb,xpos[gen]*fac-25)
        if ahnumber[i]*2 in ahnumber :
          p = dw.Path(stroke=treeColor, fill='none', stroke_width=3-gen/4)
          Tree_SVG.append(p.M(xstart, y-15+gen).Q(xstart+5, yend+10, xpos[gen]*fac-10, yend+10))
        if ahnumber[i]*2+1 in ahnumber :
          ystart = y+yoccu+30-gen+max_gen
          if gen<5 :
            yend = 2*y-yend-11
          else:
            yend = 2*y-yend+10
          p = dw.Path(stroke=treeColor, fill='none', stroke_width=3-gen/4)
          Tree_SVG.append(p.M(xstart, ystart).Q(xtb+5, yend, xpos[gen]*fac-10, yend))

      if gen>=6 and (gen<8 or ((tree_size=='A0' or tree_size[:4]=='cust') and gen<=9)):
        ystart = y-10+gen
        yshftend = -6
        font = ImageFont.truetype(fontc, max(20-gen+xtrasize,9))
        xtb = x + font.getlength(ahnentafel[i].name[0]+' '+ahnentafel[i].name[1])
        if gen == 9:
          occupation = ''
          if 'OCCU' in ahnentafel[i]:
            if ahnentafel[i].occu is not None:
              occupation = '  , ' + ahnentafel[i].occu[:(50-int(1.2*len(ahnentafel[i].name[0]+ahnentafel[i].name[1])))]
          else:
            if 'TITL' in ahnentafel[i]:
              occupation = '  , ' + ahnentafel[i].title[:(50-int(1.2*len(ahnentafel[i].name[0]+ahnentafel[i].name[1])))]
          font = ImageFont.truetype(fontc,9+xtrasize)
          font1 = ImageFont.truetype(fonti, 9)
          xtb = (x + font.getlength(ahnentafel[i].name[0]+' '+ahnentafel[i].name[1])
                 + font1.getlength(occupation))
        yshftlin = -35
        if not((tree_size=='A0' or tree_size[:4]=='cust') and gen==6) :
          xshftlin = fac*4.1 + 20
        if tree_size[:4]=='cust' and gen>7:
          xshftlin = fac * 4.5 + 35
        xstart = min(xtb,xpos[gen]*fac-25)
        if ahnumber[i]*2 in ahnumber :
          p = dw.Path(stroke=treeColor, fill='none', stroke_width=1)
          Tree_SVG.append(p.M(xstart, ystart).Q(xstart+5, yend+10+yshftend, xpos[gen]*fac-10, yend+10+yshftend))
        else :
          xshftlin = xshftlin - yshftlin/2
        if ahnumber[i]*2+1 in ahnumber :
          if gen==9:
            yshftend = -9
          yend = 2*y-yend+10+yshftend
          p = dw.Path(stroke=treeColor, fill='none', stroke_width=1)
          Tree_SVG.append(p.M(xstart, ystart).Q(xtb-yshftlin+5, yend, xpos[gen]*fac-10+xshftlin, yend))

    # Person writing
    #------------------
    if gen<9 :
      add_person_4lin(Tree_SVG, ahnentafel[i], gen, ahnentfel_number, with_number, xtrasize, x, y)
    if gen==9 :
      x = fac*xpos[gen-1]+xshift
      y = (tree_height-35)*(1/2**gen+(ahnumber[i]-2**(gen-1))/2**(gen-1))+yshift
      add_person_3lin(Tree_SVG, ahnentafel[i], gen, ahnentfel_number, with_number, xtrasize, x, y)
    if gen==10 :
      x = fac*xpos[gen-1]+xshift
      y = (tree_height-35)*(1/2**gen+(ahnumber[i]-2**(gen-1))/2**(gen-1))+yshift
      add_person_2lin(Tree_SVG, ahnentafel[i], gen, ahnentfel_number, with_number, xtrasize, x, y)
    if gen==11 :
      if tree_size[:4]=='cust':
        xshift = (ahnumber[i] - 4*int(ahnumber[i]/4)) * fac*4.3
      else :
        xshift = (ahnumber[i] - 4*int(ahnumber[i]/4)) * fac*3.4
      yshift = yshift + (ahnumber[i] - 4*int(ahnumber[i]/4)) * -2
      x = fac*xpos[gen-1]+xshift
      y = (tree_height-35)*(1/2**gen+(ahnumber[i]-2**(gen-1))/2**(gen-1))+yshift
      add_person_2linshort(Tree_SVG, ahnentafel[i], gen, ahnentfel_number, with_number, xtrasize, x, y)
    if gen>=12 :
      if tree_size[:4]=='cust':
        xshift = (ahnumber[i] - 4*int(ahnumber[i]/4)) * fac*5.1
      else :
        xshift = (ahnumber[i] - 4*int(ahnumber[i]/4)) * fac*4.25
      yshift = yshift + (ahnumber[i] - 4*int(ahnumber[i]/4)) * -1.1
      x = fac*xpos[gen-1]+xshift
      y = (tree_height-35)*(1/2**gen+(ahnumber[i]-2**(gen-1))/2**(gen-1))+yshift
      add_person_1lin(Tree_SVG, ahnentafel[i], gen, ahnentfel_number, with_number, xtrasize, x, y)

# convert units to cm for entire document
Tree_SVG.svg_args['width'] = f'{Tree_SVG.width/fac}cm'
Tree_SVG.svg_args['height'] = f'{Tree_SVG.height/fac}cm'
# save the SVG file
Tree_SVG.save_svg(gedcom_name.replace('ged', 'svg'))
