#coding: utf-8
from __future__ import print_function
import time

import crappy

save_path = "biotens_data/"
timestamp = time.ctime()[:-5].replace(" ","_")
save_path += timestamp+"/"
# Creating F sensor
effort = crappy.blocks.IOBlock("Comedi",channels=[0], gain=[-48.8],labels=['t(s)','F(N)'])
# grapher
graph_effort = crappy.blocks.Grapher(('t(s)','F(N)'))
crappy.link(effort,graph_effort)
# and saver
save_effort = crappy.blocks.Saver(save_path+"effort.csv")
crappy.link(effort,save_effort)
b = crappy.actuator.Biotens()
b.open()
b.reset_position()
b.set_position(5,50)
# Creating biotens technical
biotens = crappy.blocks.Machine([{'type':'biotens','port':'/dev/ttyUSB0','pos_label':'position1','cmd':'cmd'}])  # Used to initialize motor.
graph_pos= crappy.blocks.Grapher(('t(s)', 'position1'))
crappy.link(biotens,graph_pos)
# And saver
save_pos= crappy.blocks.Saver(save_path+'position.csv')
crappy.link(biotens,save_pos)

# To pilot the biotens
signal_generator = crappy.blocks.Generator([{'type':'constant','condition':'F(N)>90','value':5}],freq=100)
crappy.link(effort,signal_generator)
crappy.link(signal_generator,biotens)

# VideoExtenso
extenso = crappy.blocks.Video_extenso(camera="XimeaCV", white_spots=False)
# Saver
save_extenso = crappy.blocks.Saver(save_path+'extenso.csv',labels=['t(s)','Exx(%)','Eyy(%)'])
crappy.link(extenso, save_extenso)
# And grapher
graph_extenso = crappy.blocks.Grapher(('t(s)', 'Exx(%)'), ('t(s)', 'Eyy(%)'))
crappy.link(extenso, graph_extenso)

#And here we go !
crappy.start()
