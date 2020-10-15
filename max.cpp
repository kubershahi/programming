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
            cout << a << "\n";
        }
        else if (b >= a && b >= c)
        {
            cout << b << "\n";
        }
        else if (c >= a && c >= b)
        {
            cout << c << "\n";
        }
    }
    return 0;
}