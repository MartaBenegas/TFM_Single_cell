from pathlib import Path

z_fpath = Path("/home/marta/Descargas/SEURAT/10x/detected_cells_zumis_good.txt")
z_fhand = open(z_fpath)
c_path = Path("/home/marta/Descargas/SEURAT/10x/detected_cells_cellranger_good.txt")
c_fhand = open(c_path)


z_cells = [cell.strip() for cell in z_fhand]
c_cells = [cell.strip() for cell in c_fhand]

z_common = open("common_zumis_cells.txt","w")
c_common = open("common_cellranger_cells.txt","w")

common = 0
for c_cell in c_cells:
    c_rev = c_cell[:-2]
    if c_rev in z_cells:
        common += 1
        z_common.write(c_rev+'\n')
        c_common.write(c_cell+'\n')

print("zUMIs detected cells: {}\nCellRanger detected cells: {}\ncommon: {}".format(len(z_cells), len(c_cells), common))

