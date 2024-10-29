using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace OpenerGame
{
    public partial class page_2 : Form
    {
        public page_2()
        {
            InitializeComponent();
        }

        private void page_2_Load(object sender, EventArgs e)
        {
            _ = this.BeginInvoke(new Action(() =>
            {
                this.Hide();
                this.Opacity = 1;
                MessageBox.Show("在接下来的游戏中去世即可通关", "开了", MessageBoxButtons.OK);
                MessageBox.Show("1~5选择方块；Tab起飞/降落；WASD移动；空格跳；左键挖；右键防", "控制方法", MessageBoxButtons.OK);
                MessageBox.Show("注意：请一定要将输入法调到英文，不然会发生奇怪的事情。。。", "提示", MessageBoxButtons.OK);
                MessageBox.Show("本关可在5s内通过（只要你CPU够快）", "温馨提示", MessageBoxButtons.OK);
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.FileName = Path.Combine(".//library", "minecraft.exe");
                startInfo.WorkingDirectory = ".//library";
                Process process = Process.Start(startInfo);
                process.WaitForExit();
                if (process.ExitCode == 0)
                {
                    MessageBox.Show("很好，你过关了", "开了", MessageBoxButtons.OK);
                    
                }
                else
                {
                    Console.WriteLine("进程异常退出，正在重试");
                    Exe_start();
                }
            }));
        }

        private static void Exe_start()
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = Path.Combine(".//library", "minecraft.exe");
            startInfo.WorkingDirectory = ".//library";
            Process process = Process.Start(startInfo);
            process.WaitForExit();
            if (process.ExitCode == 0)
            {
                MessageBox.Show("很好，你过关了", "开了", MessageBoxButtons.OK);
            }
            else
            {
                Console.WriteLine("进程异常退出，正在重试");
                Exe_start();
            }
        }
    }
}
