#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <Eigen/Dense>
#include <emp-ot/emp-ot.h>
#include <emp-tool/emp-tool.h>

using namespace std;
using namespace Eigen;
using namespace emp;

typedef Eigen::Matrix<uint64_t, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor > MatrixXi64;
typedef Eigen::Matrix<uint64_t, 1, Eigen::Dynamic, Eigen::RowMajor> RowVectorXi64;

IOFormat CleanFmt(4, 0, ", ", "\n", "[", "]", "[", "]");

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

template<class Derived>
void send(emp::NetIO* io, Eigen::PlainObjectBase<Derived>& X){
  io->send_data(X.data(), X.rows() * X.cols() * sizeof(uint64_t));
  return;
}

template<class Derived>
void recv(emp::NetIO* io, Eigen::PlainObjectBase<Derived>& X){
  io->recv_data(X.data(), X.rows() * X.cols() * sizeof(uint64_t));
  return;
}

int main(int argc, char** argv)
{

  int port = 8000;
  string address = "127.0.0.1";

  // int PARTY = atoi(argv[1]);
  // cout << "Party: " << PARTY << endl;
  
  cout << "Party: 1" << endl;
  NetIO* io = new NetIO(nullptr, port);

  // cout << io << endl;

  MatrixXd t = MatrixXd::Random(10,10);
  // t << 4,1,2,8,1,0,3,2,1,4,6,7;
  // // cout << t.format(CleanFmt) << endl;

  // if (PARTY == ALICE){
    send(io,t);
  // }
  // else {
  //   MatrixXd s(t.rows(),t.cols());
  //   recv(io,s);
  //   cout << "Received matrix is: "<<s.format(CleanFmt) << endl;
  // }
  return 0;
}
