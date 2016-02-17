#!/usr/bin/env python
# La classe de contrôle du drône
# Importe les librairies ROS, et charge le manifest qui premet d'accéder aux
dépendances
import roslib; roslib.load_manifest('ardrone_flip')
import rospy
# Importez les messages qui nous intéresse a envoyer ou à recevoir :
from geometry_msgs.msg import Twist
#pour envoyer des commandes au drone
from std_msgs.msg import Empty
#pour attérir / décoller /
l'atterissage d'urgence / les flip
from ardrone_autonomy.msg import Navdata #pour recevoir les retour NavData
# Un objet qui contiens tous les status du drône
from drone_status import DroneStatus
# La constance d'émission des infos
COMMAND_PERIOD = 100 #ms
class BasicDroneController(object):
def __init__(self):
# Détient le statut actuel du drone
self.status = -1
# On s'abonne au topic /ardrone/navdata, avec un message de type
navdata, et on appelle la méthode ReceiveNavdata une fois le message reçu
self.subNavdata =
rospy.Subscriber('/ardrone/navdata',Navdata,self.ReceiveNavdata)
# Permet au contrôleur de publier sur les différents topic pour le
flip
self.pubLand
= rospy.Publisher('/ardrone/land',Empty)
self.pubTakeoff = rospy.Publisher('/ardrone/takeoff',Empty)
self.pubReset
= rospy.Publisher('/ardrone/reset',Empty)
self.pubFlip
= rospy.Publisher('/ardrone/setflightanimation',"")
# Permet au contrôleur de publier sur le sujet /cmd_vel et donc de
contrôler le drône
self.pubCommand = rospy.Publisher('/cmd_vel',Twist)
# Met en place le timer pour envoyer les commandes en continu
self.command = Twist()
self.commandTimer =
rospy.Timer(rospy.Duration(COMMAND_PERIOD/1000.0),self.SendCommand)
# Attéris le drône quand on arrête le programme
rospy.on_shutdown(self.SendLand)
def ReceiveNavdata(self,navdata):
# Pour l'instant on récupère que le statut du drône
self.status = navdata.state
def SendTakeoff(self):
# Envoie un message de décollage que si le drône à attéris
if(self.status == DroneStatus.Landed):
self.pubTakeoff.publish(Empty())
def SendLand(self):
# Envoie une commande d'atterissage peu importe le statut
self.pubLand.publish(Empty())
def SendFlip(self):# Envoie un message au topic flightanimation pour faire un flip
(Animation 16, durée par défaut 0 donc "16 0")
self.pubLand.publish("16 0")
def SendEmergency(self):
# Envoie un message d'atterissage d'urgence
self.pubReset.publish(Empty())
def SetCommand(self,roll=0,pitch=0,yaw_velocity=0,z_velocity=0):
# Permet de définir les paramètres de la commande à envoyer
self.command.linear.x = pitch
self.command.linear.y = roll
self.command.linear.z = z_velocity
self.command.angular.z = yaw_velocity
def SendCommand(self,event):
# Envoie la commande enregistrée que si on vole
if self.status == DroneStatus.Flying or self.status ==
DroneStatus.GotoHover or self.status == DroneStatus.Hovering:
self.pubCommand.publish(self.command)
