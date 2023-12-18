# tkdircmp
tkinter app which leverages python's dircmp to assist with comparing directories


## usage:

Supply at least two paths to be compared:

    python tkdircmp.py --path path1 --path path2
	
Addition paths may be supplied. They will be treated combinatorially.  (i.e  paths A, B, and C will be compared as A:B, B:C, A:C)

    python tkdircmp.py --path path1 --path path2 --path path3 ...

(Windows-only) Double clicking an item in a list will open an explorer window with the corresponding file selected.

