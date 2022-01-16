using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace pingcha
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        
        private void button1_Click(object sender, EventArgs e)
        {
            int n = int.Parse(textBox_n.Text);
            int t = int.Parse(textBox_t.Text);
            int s = int.Parse(textBox1.Text);
            for (int i = 0; i < t; i++)
            {
                data_income.Columns.Add("参数", "第" + (i + 1) + "个参数点点");
            }
            for(int i = 0; i < s;i++)
            {
                data_income.Columns.Add("已知点", "第" + (i + 1) + "个已知点");
            }
            for(int i = t+s;i<t+s+2;i++)
            {
                if (i == t+s)
                    data_income.Columns.Add("起点观测值", "高程观测值的负数");
                //if (i == t+s+1)
                //    data_income.Columns.Add("终点观测值", "终点观测值");
                if (i == t+s+1)
                    data_income.Columns.Add("观测路线长", "路程的观测距离");
            }
            data_income.Rows.Add(n);
            for(int i = 0;i<t;i++)
            {
                data_B.Columns.Add("第" + (i + 1) + "个参数的系数", "第" + (i + 1) + "个参数的系数");
            }
            for(int i=0;i<n;i++)
            {
                data_quanchang.Columns.Add("高程", "第" + (i+1) + "个高差观测值");
            }
            data_quanchang.Rows.Add(n);
        }
        
        private void button2_Click(object sender, EventArgs e)
        {
            int n = int.Parse(textBox_n.Text);
            int t = int.Parse(textBox_t.Text);
            int s = int.Parse(textBox1.Text);
            var b = new double[n, t+s+2];
            var B = new double[n, t];
            var S = new double[n, 1];
            var l = new double[n, 1];
            
            var x0 = new double[t, 1];
            for(int i=0;i<n;i++)
            {
                for(int j=0;j<t+s+2;j++)
                {
                    b[i, j] = double.Parse(data_income.Rows[i].Cells[j].Value.ToString());
                }
            }
            //预处理 获得B,S,L
            for(int i=0;i<n;i++)
            {
                for(int j=0;j<t;j++)
                {
                    if (b[i, j] != 0)
                        x0[j,0] = Math.Abs(b[i, j]);
                    if (b[i, j] > 0)
                        B[i, j] = 1;
                    else if (b[i, j] < 0)
                        B[i, j] = -1;
                    else
                        B[i, j] = 0;
                }
                S[i, 0] = b[i, t + s + 1]; 
                l[i, 0] = 0;
                for(int j=0; j<t+s+1; j++)
                {
                    l[i, 0] += b[i, j];
                }
               
            }
            
            for(int i=0;i<n;i++)
            {
                data_S.Rows.Add();
                data_l.Rows.Add();
                data_S.Rows[i].Cells[0].Value = S[i, 0];
                data_l.Rows[i].Cells[0].Value = l[i, 0];
                
            }
            for(int i=0;i<n;i++)
            {
                data_B.Rows.Add();
                for(int j=0;j<t;j++)
                {
                    data_B.Rows[i].Cells[j].Value = B[i, j];
                }
            }
            for(int i=0;i<t;i++)
            {
                data_X0.Rows.Add();
                data_X0.Rows[i].Cells[0].Value = x0[i, 0];
            }
        }

        private void Button3_Click(object sender, EventArgs e)
        {
            int n = int.Parse(textBox_n.Text);
            int t = int.Parse(textBox_t.Text);
            int d = int.Parse(textBox4.Text);
            var B = new double[n, t];
            var S = new double[n, 1];
            var L = new double[n, 1];
            var h = new double[n, 1];
            int s = int.Parse(textBox1.Text);
            var C = int.Parse(textBox3.Text);
            var D = new double[d, n];
            double SumS = 0;
            point[] points = new point[t];
            for(int i=0;i<n;i++)
            {
                L[i, 0] = double.Parse(data_l.Rows[i].Cells[0].Value.ToString());
                S[i, 0] = double.Parse(data_S.Rows[i].Cells[0].Value.ToString());
                h[i, 0] = double.Parse(data_income.Rows[i].Cells[t + s].Value.ToString());
                SumS += S[i, 0];
                for(int j=0;j<t;j++)
                { 
                    B[i, j] = int.Parse(data_B.Rows[i].Cells[j].Value.ToString());
                }
            }
            for(int i=0;i<t;i++)
            {
                points[i].X0 = double.Parse(data_X0.Rows[i].Cells[0].Value.ToString());
            }
            var P = new double[n, n];
            for(int i=0;i<n;i++)
            {
                for(int j=0;j<n;j++)
                {
                    P[i, j] = 0;
                    if (i == j)
                        P[i, j] = 1 / S[i, 0];
                }
            }
            for(int i=0;i<d;i++)
            {
                for(int j=0;j<n;j++)
                {
                    D[i, j] = int.Parse(data_quanchang.Rows[i].Cells[j].Value.ToString());
                }
            }
            Matrix _P = new Matrix(n,n,P);
            Matrix _B = new Matrix(n,t,B);
            Matrix _L = new Matrix(n,1,L);
            Matrix V = new Matrix(n, 1);
            Matrix Nbb;double etea;
            double QAB, QA, QB;
            int A_ = int.Parse(textBox_A.Text);
            int B_ = int.Parse(textBox_b.Text);
            gaochenp.pingc(ref points, _P, _B, _L,out V,out Nbb);
            gaochenp.jianyan(_P, V, t, SumS,Nbb,out etea);
            gaochenp.liangdian(_B,Nbb, t, A_, B_,C, out QAB, out QA, out QB);
            double quanwucha;
            gaochenp.quanchang(d, n, S, h, D,out quanwucha);
            data_result.Columns.Add("X", "参数的改正值"); 
            //data_result.Columns.Add("H", "高差的校正值");
            data_result.Rows.Add(n);
            for(int i =0;i<t;i++)
            {
                
                data_result.Rows[i].Cells[0].Value = points[i]._X;   
            }
            if (quanwucha > 10)
                MessageBox.Show("全长中误差超限");
            else
                MessageBox.Show("全长中误差未超限");
            //var _V = V.Detail;
            //for(int i = 0;i<n;i++)
            //{
            //    data_result.Rows[i].Cells[1].Value =double.Parse(data_income.Rows[i].Cells[n + s].Value.ToString())+_V[i,0];
            //}
            textBox2.Text = A_.ToString() + "点的高程中误差为" + (Math.Sqrt(etea * QA).ToString()) + "\n  " + B_.ToString() + "点的高程中误差为" + (Math.Sqrt(etea * QB)).ToString() + "\n   " + A_ + "与" + B_ + "之间的高程中误差为" + (Math.Sqrt(etea * QAB)).ToString();
        }

        private void label11_Click(object sender, EventArgs e)
        {

        }
    }
}
