import PIL
from PIL import Image
import os, sys, shutil
import errno

#------------------------------------------------------------------

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
        print 'Directorio salida creado'
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        else: 
        	os.chdir(path)
        	filelist = [ f for f in os.listdir(".") ]
        	for f in filelist:
        		os.remove(f)
        	print 'Directorio salida limpio'


#------------------------------------------------------------------

def convertImage(f_in, f_out, myheight):
	print ' *** tratando %s' % f_in
	
	img = Image.open(f_in)
	tempFile = ''
	
	#-- los PNG hay que convertirlos primero a JPG
	if os.path.splitext(f_in)[1] == '.png':
		tempFile = os.path.splitext(f_in)[0]+"_temp.jpg"
		bg = Image.new("RGB", img.size, (255,255,255))
		bg.paste(img,img)
		bg.save(tempFile)
		img = bg
		f_in = tempFile
		print '\t- creado temp file %s' % tempFile

	#-- si supera el height indicado se redimensiona la imagen
	if img.size[1] > myheight:
		hpercent = (myheight / float(img.size[1]))
		wsize = int((float(img.size[0]) * float(hpercent)))
		img = img.resize((wsize, myheight), PIL.Image.ANTIALIAS)
		img.save(f_out)	
		print '\t- redimensionado como %s' % f_out

	else:
		#-- hago una copia pero con el nombre correcto
		shutil.copy2(f_in, f_out)	
		print '\t- grabado como %s' % f_out

	#-- si hubo que crear fichero temporal, se borra	
	if tempFile != '':
		os.remove(tempFile)
		print '\t- eliminado temp file %s' % tempFile

#------------------------------------------------------------------


def main():
	if len(sys.argv) != 4:
		print "Usage: python resizer.py <orig_dir> <dest_dir> <start_counter>"
	else:
		origDir = sys.argv[1]
		destDir = sys.argv[2]
		counter = int(sys.argv[3])
		

		absOrigDir = os.path.realpath(origDir)
		absDestDir = os.path.realpath(destDir)

		# print 'absOrigDir: ', absOrigDir
		# print 'absDestDir ', absDestDir

		baseHeight = 600
		baseHeightTb = 90
		imgExts = ['.jpg', '.jpeg', '.png']

		os.chdir(absOrigDir)
		imgList = [f for f in os.listdir(absOrigDir) if os.path.isfile(f) and os.path.splitext(f)[1] in imgExts]
		# print imgList

		make_sure_path_exists(absDestDir)

		#-- creo las imagenes grandes, con numeracion
		for f in imgList:
			convertImage(absOrigDir+'/'+f, absDestDir+'/'+str(counter).zfill(3) + ".jpg", baseHeight)
			counter += 1

		# #-- creo los thumbails
		os.chdir(absDestDir)
		tbList = [f for f in os.listdir(absDestDir) ]
		for f in tbList:
			convertImage(absDestDir+'/'+f, absDestDir+'/tn_'+f, baseHeightTb)

#------------------------------------------------------------------


if __name__ == "__main__": main()	