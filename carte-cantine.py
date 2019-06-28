#-*- coding:utf-8 -*-
import unicodedata
import os
import sys


COLORS = {"11h30":"\\cellcolor{green}", "12h00":"\\cellcolor{yellow}", "12h30":"\\cellcolor{orange}", "13h00":"\\cellcolor{red}"}

# ELEVE = [
#     "6eme1;nom1;prenom1;11h30;11h30;11h30;11h30;11h30;11h30;11h30;11h30",
#     "6eme1;nom1;prenom1;11h30;12h30;12h00;11h30;13h00;11h30;11h30;11h30"
# ]

def obtainData(filename):
    if not filename in os.listdir("."):
        print("no filename %s available. Exiting.")
        sys.exit()
    file = open(filename, "r")
    content = []
    for line in file.readlines():
        content.append(line.replace("\n", "").replace("\"", ""))
    file.close()
    return content

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def make_carte(content):
    '''L'argument line est de la forme :
    classe ; nom ; prenom ; lundi SA ; lundi SB ;...
    '''
    print(content)
    line = content.split(";")
    infos = strip_accents(" ".join(line[0:3]))
    return '''
\\begin{minipage}{0.5\\linewidth}
  \\qrcode[height=10cm]{%s}
\\end{minipage}
\\begin{minipage}{0.5\\linewidth}
  \\fontsize{60}{70}\\selectfont
  %s\\\\
  %s\\\\
  %s
\\end{minipage}

\\begin{minipage}{0.9\\linewidth}
  \\renewcommand{\\arraystretch}{8}
\\begin{tabular}{|*{4}{p{0.25\\linewidth}|}}
%s & %s & %s & %s \\\\
\\hline
%s & %s & %s & %s
\\end{tabular}
\\end{minipage}

'''%(infos, line[0], line[1], line[2], COLORS[line[3]], COLORS[line[4]], COLORS[line[5]], COLORS[line[6]], COLORS[line[7]], COLORS[line[8]], COLORS[line[9]], COLORS[line[10]])

def make_preamble():
    return '''
\\documentclass[landscape]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[svgnames]{xcolor}
\\usepackage{colortbl}
\\usepackage{qrcode}
\\usepackage[margin=1cm]{geometry}
\\pagestyle{empty}
\\usepackage{anyfontsize}
\\renewcommand{\\familydefault}{\\ttdefault}
\\begin{document}
'''

def make_postamble():
    return '''
\\end{document}
'''



ELEVE = obtainData("eleves.csv")
string = make_preamble()
for eleve in ELEVE:
    string += make_carte(eleve)
string += make_postamble()

print(string)
