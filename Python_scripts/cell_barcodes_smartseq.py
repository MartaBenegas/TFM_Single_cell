from pathlib import Path

### get artificial barcodes list
barcodes_file = Path("/home/marta/Descargas/barcodes.txt")
barcodes_list = [line.strip() for line in open(barcodes_file)]


### generate index fastq files
directory = Path("/home/marta/Descargas/smarseq_adapted_data")
quality = len(barcodes_list[0])*'I'
n=0
for file in directory.iterdir():
    barcode = barcodes_list[n]
    idx_fname = str(file).split('/')[-1].split('.')[0]+'_idx.fastq'
    print(idx_fname,'\t',barcode)
    idx_file  = open(idx_fname, 'w')
    ofile = open(file, 'r')
    
    while True:
        header,seq = ofile.readline().strip(), ofile.readline().strip() 
        sep,qual = ofile.readline().strip(), ofile.readline().strip()
        if not header: break
        new_record = header+'\n'+barcode+'\n'+sep+'\n'+quality+'\n'
        idx_file.write(new_record)
    n+=1
    

