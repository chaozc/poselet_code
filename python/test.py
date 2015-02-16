import os
from mlabwrap import mlab
mlab.path(mlab.path(), '../matlab')
hog = mlab.get_HOG('../seed_patches/1970393557375786_185_178_112_168.jpg')
print hog