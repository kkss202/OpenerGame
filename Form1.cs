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
    public partial class page_begin : Form
    {
        public page_begin()
        {
            InitializeComponent();
        }

        private void Page_begin_button_false_Click(object sender, EventArgs e)
        {
            MessageBox.Show("哎呦，你干嘛~~", "你点啥", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
        }

        private void Page_begin_button_true_Click(object sender, EventArgs e)
        {
            MessageBox.Show("不错，眼睛挺尖，进入游戏", "开了", MessageBoxButtons.OK);
            Thread turnto = new(delegate () { new page_1().ShowDialog(); });
            turnto.Start();
            Close();
        }
    }
}
