# GEDCOM to SVG family tree (python script)

It is now very cheap to print a A1 or A0 format sheet at any copy shop, between 10 and 20 $ or €.

So, it is a good ooportunity to draw a family tree in a compact way with many generations.

I recommend you to ask them what is the best size and use a customised format.



This python script allows to draw a family tree in different formats :
* **A4** : 5 generations
* **A3** : 6 generations
* **A2** : 8 generations
* **A1** : 10 generations
* **A0** : 12 generations
* **custom** : up to 13 in an exemple

The reason to use SVG format as an output is because the family tree is never drawn perfectly as we imagine it.
It always needs some fine tuning, and SVG format can easily be modify for example with Inkscape or any other freeware.
Then, after all the small adjusment, you can save this family tree in PDF format to print it.

## usage
`python gedcompy_tree.py -g your_gedcom_file.ged`

or you can use some options:

`-g or --gedcom` : GEDCOM file

`-i or --indi` : INDI number of the root of the tree, default = "I1"

`-r or --root` : renumber the root number", default = 1

`-s or --size` : tree size : 'A4', 'A3', 'A2', 'A2', 'A1', 'A0' or 'custom1' , default = 'A0'

`-c or --color` : colorize the tree", default=True

`-n or --number` : add the anhentafel numbers, default=True

`-p or --photo` : add the photo", default=True

Most of the text is in French, but they are easy to change to your own language.
