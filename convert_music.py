import os
import subprocess

# this script traverses the folders starting at
# rootfolder and converts all .wma files to 
# .mp3 using mplayer and LAME
# the overall approach comes from this article:
# https://askubuntu.com/questions/55352/convert-library-of-wma-tracks-to-mp3s
# 
# I've set LAME to use 320 kb variable bitrate via the -V 0 --preset insane
# flags.
# 
# references:
# http://wiki.hydrogenaud.io/index.php?title=LAME
# https://www.lifewire.com/difference-between-cbr-and-vbr-encoding-2438423
#
# There's a bug in that it doesn't handle filenames with single quotes
# properly.  In the bash shell, all whitespace and special charaters
# are escaped but the filenames found via os.walk(...) do not
# Instead of tryping to escape them properly (https://docs.python.org/dev/library/shlex.html#shlex.quote) I simply wrapped the filenames in a single
# quote.  I found later that filenames that already had a single quote
# ended up with a messed up command line.  I probably could have fixed this
# by using a double quote but just fixed those few files by hand.
#
# this is the command to combine mplayer and lame to convert from
# .wma to mp3
#mplayer -vo null -vc dummy -af resample=44100 -ao pcm -ao pcm:waveheader 02\ Jolly\ Old\ St.\ Nicholas.wma && lame -V 0 --preset insane -m s audiodump.wav -o test.mp3
# the source file is 02\ Jolly\ Old\ St.\ Nicholas.wma
# the output file is test.mp3
# the first half of the command i

rootfolder = 'Music'

# convertlist is actually a list of pairs (lists)
# [[file1.wma, file1.mp3], [file2.wma, file2.mp3]]
convertlist = []

for folderName, subfolders, filenames in os.walk(rootfolder):
    for filename in filenames:
        if filename.endswith('wma'):
            # strip the .wma off and append .mp3
            wmaname = os.path.join(folderName, filename)
            noext = os.path.splitext(filename)[0]
            mp3name = noext + '.mp3'
            newfullpath = os.path.join(folderName, mp3name)
            convertlist.append([wmaname,newfullpath])



cmdline1 = "mplayer -vo null -vc dummy -af resample=44100 -ao pcm -ao pcm:waveheader "
cmdline2 = " && lame -V 0 --preset insane -m s audiodump.wav -o "
cmdline = 'hi'

# this has a bug in that it doesn't handle filenames with a single quote
# in them
for conversion in convertlist:
    cmdline = cmdline1 + "'" + conversion[0] + "'" + cmdline2 + "'" + conversion[1] + "'"
    print('Converting ' + conversion[0])
    subprocess.call(cmdline, shell=True)



print('done')



