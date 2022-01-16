using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
namespace pingcha
{
    struct point
    {
        public string _ID;
        public string ID
        {
            get { return _ID; }
            set { _ID = value; }
        }
        public double _X { get; set; }//间接平差的参数设置
        
        public double X0 { get; set; }
        
        //public double x;//参数的改正值
        //public double h;//点的高程观测值
        //public double h_cored;//改正值
        //public double X;//点的XY的坐标
        //public double Y;

        
    }
    class gaochenp
    {
        public static void pingc(ref point[] points,Matrix P,Matrix B,Matrix L,out Matrix v,out Matrix Nbb)//X0为已知，h为已知，H为已知。（待输入值）
            //P为n*n的对角阵，B为n*t
        {
            int n = B.getM;
            int t = B.getN;
            //BtPB
            var Bt = MatrixOperator.MatrixTrans(B); //nt
            Nbb = MatrixOperator.MatrixMulti(MatrixOperator.MatrixMulti(Bt, P), B); //tt
            var W = MatrixOperator.MatrixMulti(MatrixOperator.MatrixMulti(Bt, P), L); //n1
            var _x = MatrixOperator.MatrixMulti(MatrixOperator.MatrixInvByCom(Nbb), W); //t1
            v = MatrixOperator.MatrixSub(MatrixOperator.MatrixMulti(B, _x),L); //n1
            //var _L = MatrixOperator.MatrixAdd(L, _x);
            var __x = new double[t,1];
            var __v = v.Detail;

            __x = _x.Detail;
            for(int i=0;i<t;i++)
            {
                points[i]._X = points[i].X0 + __x[i, 0];
               
            }
           
        }
        public static void jianyan(Matrix P,Matrix v,int t,double sumS,Matrix Nbb,out double etea)
        {
            int n = P.getM;
            var Q = MatrixOperator.MatrixInvByCom(P);
            var vt = MatrixOperator.MatrixTrans(v);
            var etea1 = MatrixOperator.MatrixMulti(MatrixOperator.MatrixMulti(vt, P), v);
            var _etea = MatrixOperator.MatrixSimpleMulti(1000 / t, etea1);//单位权中误差
            var InNbb = MatrixOperator.MatrixInvByCom(Nbb);
            var _InNbb = InNbb.Detail;
            var _Q = Q.Detail;
            var etea_ = _etea.Detail; 
            double sumQ = 0;
            etea = etea_[0, 0];
            
            for (int i = 0;i < n;i++)
            {
                sumQ += _Q[i, i];
            }
            var km_etea = MatrixOperator.MatrixSimpleMulti(sumQ,_etea);
            double[,] km_etea1 = km_etea.Detail;
            //检验是否超限
            //if(Math.Sqrt(km_etea1[0,0]) > 10*Math.Sqrt(sumQ))
            //{
            //    MessageBox.Show("超限，超过四等规定每公里水准路线要求");   
            //}
            //else if(Math.Sqrt(km_etea1[0, 0]) > 3 * Math.Sqrt(sumQ))
            //{
            //    MessageBox.Show("超过三等规定每公里路线要求");
            //}
        }
        public static void liangdian( Matrix B,Matrix Nbb,int t,int _A,int _B,int C,out double QABJ,out double QA,out double QB)//
        {
            var InNbb = MatrixOperator.MatrixInvByCom(Nbb);
            var _InNbb = InNbb.Detail;
            
            Matrix hab = new Matrix(t, 1);
            Matrix Qhh = MatrixOperator.MatrixMulti(MatrixOperator.MatrixMulti(B,InNbb),MatrixOperator.MatrixTrans(B));
            double[,] _hab = new double[t, 1];
            for(int i=0;i<t;i++)
            {
                _hab[i,0] = 0;
            }
            if (_A < t)
                _hab[_A, 0] = 1;
            if (_B < t)
                _hab[_B, 0] = 1;
            hab.Detail = _hab;
            //Qab = MatrixOperator.MatrixMulti(MatrixOperator.MatrixTrans(hab), InNbb);
            //Qab = MatrixOperator.MatrixMulti(Qab, hab);
            //var _Qab = Qab.Detail;
            //QABJ = _Qab[0, 0];
            var _Qab = Qhh.Detail;
            QABJ = _Qab[C-1, C-1];
            QA = _InNbb[_A-1, _A-1];
            QB = _InNbb[_B-1, _B-1];
        }
        public static void quanchang(int d,int n,double[,] S,double[,] h,double[,] D,out double wucha)
        {
            var _D = new Matrix(d, n, D);
            var _h = new Matrix(n, 1, h);
            var Sumh = MatrixOperator.MatrixMulti(_D, _h);//d1矩阵
            var subD = new double[d, n];
            for(int i=0;i<d;i++)
            {
                for(int j=0;j<n;j++)
                {
                    subD[i, j] = Math.Abs(D[i, j]);
                }
            }
            var _subD = new Matrix(d, n, subD);
            var _S = new Matrix(n, 1, S);
            var SumS = MatrixOperator.MatrixMulti(_subD, _S);//d1矩阵
            var _SumS = SumS.Detail;
            var _SumH = Sumh.Detail;
            double detadeta = 0;
            for(int i=0;i<d;i++)
            {
                detadeta += _SumH[i,0] * _SumH[i,0] * 1000 / ( _SumS[i,0] * d) ;
            }
            wucha = Math.Sqrt(detadeta);
        }
    }
}
