#include<iostream>
#include<stdio.h>
#include<cstdlib>
#define THRESHOLD 2
#define LQIreq 100
#define PACKET_RECEPTION_RATE 10
#define SIGNAL_PROPAGATION_SPEED 300000000
#define PROCESSING_DELAY 0.1
using namespace std;

int path[1000000];
int numberOfRoboticNodes,numberOfMobileNodes,numberOfHops;
int roboticNodes[1000000][2];
int mobileNodes[1000000][2];

double random_ () {
   return (double)rand()/(RAND_MAX+1);
}

double PRR()
{
	return random_()*PACKET_RECEPTION_RATE;
}

double normalied_RSSI_mean()
{
	double RSSI_mean = random_()*60-100;
	return (RSSI_mean+100)/60;
}

double getLQI(int a,int b)
{
	return PRR()*normalied_RSSI_mean();
}

double getDLink(double distance)
{
    double dProp = distance/SIGNAL_PROPAGATION_SPEED;
    double dProc = PROCESSING_DELAY;
    return dProp+dProc;
}

class LQIete{
	int eteValue;
	int REInode;
	int PREnode;

	public:

		LQIete(){
			eteValue =  0;
			REInode  = -1;
			PREnode  = -1;
		}

		int getETEValue(){
			return eteValue;
		}

		int getREInode(){
			return REInode;
		}

		int getPREnode(){
			return PREnode;
		}

		//Estimates the LQIete value for the link and stores the weak links with lower LQI values
		void estimateLQIete(int source, int destination){
			int minLQI = 1000000;// 1  3  4  6
			for(int i=0;i<numberOfHops-1;i++){
				if(getLQI(path[i],path[i+1]) < minLQI){
					REInode = path[i+1];
					PREnode = path[i];
					minLQI = getLQI(path[i],path[i+1]);
				}
				eteValue += getLQI(path[i],path[i+1]);
			}
		}
};

int findNearestRN(int REI,int PRE)
{
	int midx = (mobileNodes[REI][0]+mobileNodes[PRE][0])/2;
	int midy = (mobileNodes[REI][1]+mobileNodes[PRE][1])/2;
	int min=10000000;
	int roboticNodeNumber;
    for(int i=1;i<=numberOfRoboticNodes;i++)
    {
    	int x = roboticNodes[i][0];
    	int y = roboticNodes[i][1];
		int distance = (midx-x)*(midx-x) + (midy-y)*(midy-y) ;
    	if(distance<min)
    	{
		   min=distance;
		   roboticNodeNumber = i;
	    }
	}
	return roboticNodeNumber;
}

int main()
{
	//Robotic Nodes
	FILE * fp1 = fopen("MobileRobot.txt", "r");
	fscanf(fp1,"%d",&numberOfRoboticNodes);
	for(int i=1;i<=numberOfRoboticNodes;i++)
	{
		fscanf(fp1,"%d%d",&roboticNodes[i][0],&roboticNodes[i][1]);

	}

	//Mobile Nodes
	FILE * fp2 = fopen("MobileNode.txt", "r");
	fscanf(fp2,"%d",&numberOfMobileNodes);
	for(int i=1;i<=numberOfMobileNodes;i++)
	{
		fscanf(fp2,"%d%d",&mobileNodes[i][0],&mobileNodes[i][1]);
	}

	//Path from ACO
	FILE * fp5 = fopen("ACOPath.txt", "r");
	fscanf(fp5,"%d",&numberOfHops);
	for(int i=0;i<numberOfHops;i++)
	{
		fscanf(fp5,"%d",&path[i]);
	}
	//0-based Indexing used in Path array only.
	int source=path[0],destination=path[numberOfHops-1];

	LQIete link;
	link.estimateLQIete(source, destination);

	if(link.getETEValue() >= LQIreq){
		cout<<"Link quality is good"<<endl;
		return 0;
	} else{
		cout<<"Link quality is not good"<<endl;
		//Finding nearest Robotic node
		int nearestRN = findNearestRN(link.getREInode(),link.getPREnode());
		FILE * fp3 = fopen("ReinforcementFlag.txt", "w");
		fprintf(fp3,"TRUE");

		FILE * fp4 = fopen("UpdatedPath.txt", "w");
		int i=0;
		while(path[i]!=link.getPREnode())
		{
			fprintf(fp4,"%d ",path[i]);
			i++;
		}

		fprintf(fp4,"%d ",link.getPREnode());
		fprintf(fp4,"%d ",-nearestRN);
		i++;
		while(i<numberOfHops)
		{
			fprintf(fp4,"%d ",path[i]);
			i++;
		}
	}
}
