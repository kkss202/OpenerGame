using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace OpenerGame
{
    public partial class page_1 : Form
    {
        public page_1()
        {
            InitializeComponent();
            MessageBox.Show("本关可在10s内通过（只要你手速够快）", "温馨提示", MessageBoxButtons.OK);
            Thread thread = new(() => Clipboard.SetText("齾（hi！你在找它吗？）"));
            thread.SetApartmentState(ApartmentState.STA); //Set the thread to STA
            thread.Start();
            thread.Join(); //Wait for the thread to end
        }

        private void Page_1_textbox_answer_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                Page_1_button_chick_Click(sender, e);
                // 回车键被按下，执行相应操作
            }
        }

        private void Page_1_button_chick_Click(object sender, EventArgs e)
        {
            if (Page_1_textbox_answer.Text == "'齾'")
            {
                MessageBox.Show("我很好奇你是怎么输入的？进入下一关！", "开了", MessageBoxButtons.OK);
                Thread turnto = new Thread(delegate () { new page_2().ShowDialog(); });
                turnto.Start();
                Close();
            }
            else
            {
                if (Page_1_textbox_answer.Text == "齾" || Page_1_textbox_answer.Text == "'齾" || Page_1_textbox_answer.Text == "齾'")
                {
                    MessageBox.Show("你好像少点什么", "开了", MessageBoxButtons.OK);
                }
                else
                {
                    if (Page_1_textbox_answer.Text == "")
                    {
                        MessageBox.Show("大哥，你输点东西再点吧", "开了", MessageBoxButtons.OK);
                    }
                    else
                    {
                        MessageBox.Show("真开了", "开了", MessageBoxButtons.OK);
                    }
                }
            }
        }
    }
}
