#include <iostream>
#include <math.h>
using namespace std;

int main()
{
    float x, y;
    cin >> x >> y;
    if (x + 0.50 <= y && fmod(x, 5) == 0)
    {
        y = y - (x + 0.50);
        printf("%.2f", y);
    }
    else
    {
        printf("%.2f", y);
    }
    return 0;
}