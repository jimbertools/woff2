import os
import subprocess

path = 'src'
include = 'include'
brotli = 'brotli/c/include/'
brotlibin = 'brotli/bin/obj/em/'
files = []
# r=root, d=directories, f = files

bzList = []
print("Starting emscripten build")

for r, d, f in os.walk(path):
    for file in f:
         if 'woff2_compress.cc' in file or 'woff2_decompress.cc' in file or 'woff2_info.cc' in file or 'bindings.cc' in file or 'convert_woff2ttf_fuzzer_new_entry.cc' in file or 'convert_woff2ttf_fuzzer.cc' in file:
            continue
         if '.c' in file:
            fullname = os.path.join(r, file)
            print("Building {}".format(fullname))
            #/bin/obj/[PADZONDER/c/maar/EM/].bc
            os.system('mkdir -p bin/obj/em/{}'.format(r))
            bzName = "bin/obj/{}".format(fullname.replace( "src/", 'em/', 1).replace('.cc', '.bc').replace('.c', '.bc'))
            bzList.append(bzName)
            os.system('emcc  -std=c++11 -I{} -I{} {} -o {}'.format(include,brotli, fullname,bzName))


for r, d, f in os.walk(brotlibin):
   for file in f:
      print("Adding lib file {}".format(file))
      bzName = fullname = os.path.join(r, file)
      bzList.append(bzName)


print("Emscripten compiling...")
bzs = ' '.join(bzList)

os.system("mkdir -p bin/js")
os.system("emcc -s MODULARIZE -s EXPORT_NAME=\"'WOFF2'\" -Iinclude --bind src/em/bindings.cc " + bzs +  ' -o ' +  "bin/js/woff2.js" )

os.system("cp src/em/*.js src/em/*.html bin/js ")
os.system("paplay /usr/share/sounds/gnome/default/alerts/glass.ogg")
print("All done")