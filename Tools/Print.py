import datetime
import subprocess


def from_file(file_name):
    debug('Print_FF_Tool', 'File: %s' %file_name)
    image = create_image(file_name)
    print_image(image)
   
def create_image(file_name):
    debug('Print_FF_Tool', 'Creating image')
    p = subprocess.Popen('wkhtmltoimage --width 384 ' + file_name + ' ./tmp/tmp_print.png', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in p.stdout.readlines():
        #print line,
    retval = p.wait()
    return './tmp/tmp_print.png'
    
def print_image(file_name):
    debug('Print_FF_Tool', 'Printing Image')
    p = subprocess.Popen('lp -o media=Custom.48x200mm -o fit-to-page -o position=top -d ZJ-58 '+ file_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in p.stdout.readlines():
        #print line,
    retval = p.wait()
    
    
def debug(section, log):
        date = datetime.datetime.today()
        print '[%s - %s] %s' % (date.strftime('%Y-%m-%d %H:%M:%S'),
                                section, log)
