#include <iostream>
#include <string>

using namespace std;
int main() 
{
	string str = "" ;
	double x = 0.33964525769858457853248023817 ;
	while(x!=0)
	{
		x *= 2 ;
		if( (int)x == 1 )
			str += "1" ;
		else
			str += "0" ;
			
				
		x = x - (int)x ;
		
		
	}
	cout << str ;
	
}

