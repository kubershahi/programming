#include <iostream>
#include <algorithm>

using namespace std;

int main()
{
    int n;
    int a, b, c;
    cin >> n;

    for (int i = 0; i < n; i++)
    {
        cin >> a >> b >> c;
        if (a >= b && a >= c)
        {
            if (b >= c)
            {
                cout << b << "\n";
            }
            else
            {
                cout << c << "\n";
            }
        }
        if (b >= a && b >= c)
        {
            if (a >= c)
            {
                cout << a << "\n";
            }
            else
            {
                cout << c << "\n";
            }
        }
        if (c >= a && c >= b)
        {
            if (a >= b)
            {
                cout << a << "\n";
            }
            else
            {
                cout << b << "\n";
            }
        }
    }
    return 0;
}