#include <iostream>

using namespace std;

int main()
{
    int n;
    int b[7];
    cin >> n;
    int a;
    int j;
    for (int i = 0; i < n; i++)
    {
        cin >> a;
        for (j = 0; a > 0; j++)
        {
            b[j] = a % 2;
            a = a / 2;
        }
        for (j = j - 1; j >= 0; j--)
        {
            cout << b[j];
        }
        cout << "\n";
    }
}