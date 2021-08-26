#include <iostream>
#include <string>

using namespace std;

void print_binary(uint64_t num) 
{
  string res = "\n";
  for (int i = 0; i <64; i++)
  {
    if ((num>>i) & 1)
    {
      string temp = "1";
      res = temp.append(res);
      // cout<<"1";
    }
    else
    { 
      string temp = "0";
      res = temp.append(res);
      // cout<<"0";
    }
  }
  cout << endl << res << endl;

}

int main()
{
  uint64_t s = 16ull;
  print_binary(s);
  return 0;
}