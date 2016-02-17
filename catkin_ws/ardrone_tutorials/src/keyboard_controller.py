#!/usr/bin/env python
# Le code principal de contrôle du drône via le clavier
import roslib; roslib.load_manifest('ardrone_flip')
import rospy
# On charge la classe DroneController, qui gère les échanges avec le drone,et la classe DroneVideoDisplay, qui gère l'affichage de la vidéo
from drone_controller import BasicDroneController
from drone_video_display import DroneVideoDisplay
# Les librairies de GUI
from PySide import QtCore, QtGui
# Ici on fait le mapping dans un objet, sachant que Python n'a pas d'enums
class KeyMapping(object):
PitchForward
= QtCore.Qt.Key.Key_E
PitchBackward
= QtCore.Qt.Key.Key_D
RollLeft
= QtCore.Qt.Key.Key_S
RollRight
= QtCore.Qt.Key.Key_F
YawLeft
= QtCore.Qt.Key.Key_Z
YawRight
= QtCore.Qt.Key.Key_R
IncreaseAltitude = QtCore.Qt.Key.Key_A
DecreaseAltitude = QtCore.Qt.Key.Key_Q
Flip
= QtCore.Qt.Key.Key_M
Takeoff
= QtCore.Qt.Key.Key_Y
Land
= QtCore.Qt.Key.Key_H
Emergency
= QtCore.Qt.Key.Key_Space
# Le KeyboardController hérite de la classe DroneVideoDisplay, qui nous
servira pour le prochain cour
class KeyboardController(DroneVideoDisplay):
def __init__(self):
super(KeyboardController,self).__init__()
self.pitch = 0
self.roll = 0
self.yaw_velocity = 0
self.z_velocity = 0
# On gère ici les pressions du clavier
def keyPressEvent(self, event):
key = event.key()
# If we have constructed the drone controller and the key is not
generated from an auto-repeating key
if controller is not None and not event.isAutoRepeat():
# Handle the important cases first!
if key == KeyMapping.Emergency:
controller.SendEmergency()
elif key == KeyMapping.Takeoff:
controller.SendTakeoff()
elif key == KeyMapping.Land:
controller.SendLand()
elif key == KeyMapping.Flip:
controller.SendFlip()
else:
# Now we handle moving, notice that this section is the
opposite (+=) of the keyrelease section
if key == KeyMapping.YawLeft:
self.yaw_velocity += 1
elif key == KeyMapping.YawRight:
self.yaw_velocity += -1elif key == KeyMapping.PitchForward:
self.pitch += 1
elif key == KeyMapping.PitchBackward:
self.pitch += -1
elif key == KeyMapping.RollLeft:
self.roll += 1
elif key == KeyMapping.RollRight:
self.roll += -1
elif key == KeyMapping.IncreaseAltitude:
self.z_velocity += 1
elif key == KeyMapping.DecreaseAltitude:
self.z_velocity += -1
# Au final on envoie la commande. Le contrôleur s'occupe
d'envoyer la commande à intervale régulier
controller.SetCommand(self.roll, self.pitch, self.yaw_velocity,
self.z_velocity)
def keyReleaseEvent(self,event):
key = event.key()
# Si nous avons construit le contrôleur du drône et la touche n'est
pas généré par une touche auto-répétante
if controller is not None and not event.isAutoRepeat():
# Ici on gère juste l'annulation des instructions de
yaw/pitch/roll, pas besoin de gérer les commandes sans paramètres
if key == KeyMapping.YawLeft:
self.yaw_velocity -= 1
elif key == KeyMapping.YawRight:
self.yaw_velocity -= -1
elif key == KeyMapping.PitchForward:
self.pitch -= 1
elif key == KeyMapping.PitchBackward:
self.pitch -= -1
elif key == KeyMapping.RollLeft:
self.roll -= 1
elif key == KeyMapping.RollRight:
self.roll -= -1
elif key == KeyMapping.IncreaseAltitude:
self.z_velocity -= 1
elif key == KeyMapping.DecreaseAltitude:
self.z_velocity -= -1
# Au final on envoie la commande. Le contrôleur s'occupe
d'envoyer la commande à intervale régulier
controller.SetCommand(self.roll, self.pitch, self.yaw_velocity,
self.z_velocity)
# Définit l'application
if __name__=='__main__':
import sys
# On définit un noeud ros pour communiquer avec les autres packages
rospy.init_node('ardrone_keyboard_controller')
# On construit l'application Qt et on associe le contrôleur et la fenêtre
app = QtGui.QApplication(sys.argv)
controller = BasicDroneController()
display = KeyboardController()display.show()
# On exécute l'application
status = app.exec_()
# Et on arrive ici que si l'application à été shutdown
rospy.signal_shutdown('Bon vol, commandant!')
sys.exit(status)
