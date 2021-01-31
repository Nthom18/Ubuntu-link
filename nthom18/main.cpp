#include "Driver.h"

using namespace std;

int main() {
    
    // Benchmark great performance from previous submissions
    // From [1,1] -> [999,999]:
    //  Â· Runtime: ~ 18 sec.
    // Â Â· Memory: ~ 190 MB.

    // Positions are indexed starting from 0.
    // So the position [0,0] translates to A1 in chess nomenclature.

    cout << MinimumSteps(1000,1000,1,2,3,4) << endl;
    cout << MinimumSteps(1000,1000,1,2,7,7) << endl;
    cout << MinimumSteps(1000,1000,0,0,6,6) << endl;
    cout << MinimumSteps(1000,1000,6,4,241,230) << endl;
    cout << MinimumSteps(1000,1000,1,2,899,899) << endl;

    return 0;
}