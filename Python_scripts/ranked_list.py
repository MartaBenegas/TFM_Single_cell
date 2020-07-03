from pathlib import Path
from math import log10

markers_dir = Path("/home/marta/Descargas/FUNCTIONAL_ANNOT/10x/cellranger_markers_by_clust")

def signum(num):
    if num < 0: return -1
    elif num > 0: return 1
    else: return 0


def rank(logfc, pval):
    return signum(logfc)*(-log10(pval))


def ranked_list(fpath):
    fhand = open(fpath)

    clust = str(fhand).split("/")[-1].split('_')[0]		#cluster name
    fname = str(markers_dir) + '/' + clust + '_ranked.txt'	#new file name
    ranked = open(fname, 'w')

    for line in fhand:
        line = line.strip().split()
        gene_id = line[0][1:-1]
        logfc = float(line[2])
        pval = float(line[1])
        r = rank(logfc, pval)
        line = gene_id + '\t' + str(r) + '\n'
        ranked.write(line)


def main():
    for fpath in markers_dir.iterdir():
        if ".txt" not in str(fpath): continue
        ranked_list(fpath)

main()
