#include
#include
#include
#include
<ros/ros.h>
"std_msgs/Int32.h"
"std_msgs/Float32.h"
"ardrone_autonomy/Navdata.h"
using namespace std;
ardrone_autonomy::Navdata msg_in;
//variable qui récupère l’état d’AR-drone
int drone_state=0;
void heightControl(const ardrone_autonomy::Navdata& msg_in)
{
//récupérer l’état d’AR-drone à partir de la fonction msg_in.state
drone_state=msg_in.state;
cout << drone_altd << endl;
}
int main(int argc, char **argv)
{
//envoyer les information sur l’état d’AR-drone à ROS et l’affichage
ros::init(argc,argv,"state_Control");
ros::NodeHandle n;
ros::Subscriber sub = n.subscribe("/ardrone/navdata", 1, heightCont
rol);
ros::spin();
return 0;
}
Puis complet avec la co
