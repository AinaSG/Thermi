from threading import Timer
from RandomMovie.RandomMovie import RandomMovie
from Tools import Print

if __name__ == "__main__":
    rmovie = RandomMovie()
    rmovie.debug('RM_Main', 'Begining RandMovie')

    outfile = rmovie.generate()
    Print.from_file(outfile)
