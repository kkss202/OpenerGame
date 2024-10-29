namespace OpenerGame
{
    partial class page_begin
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            Page_begin_button_false = new Button();
            Page_begin_button_true = new Button();
            SuspendLayout();
            // 
            // Page_begin_button_false
            // 
            Page_begin_button_false.FlatAppearance.BorderSize = 0;
            Page_begin_button_false.FlatAppearance.MouseDownBackColor = SystemColors.Control;
            Page_begin_button_false.FlatAppearance.MouseOverBackColor = SystemColors.Control;
            Page_begin_button_false.FlatStyle = FlatStyle.Flat;
            Page_begin_button_false.ForeColor = SystemColors.ControlText;
            Page_begin_button_false.Location = new Point(-1, -1);
            Page_begin_button_false.Name = "Page_begin_button_false";
            Page_begin_button_false.Size = new Size(931, 442);
            Page_begin_button_false.TabIndex = 0;
            Page_begin_button_false.Text = "点击开始游戏";
            Page_begin_button_false.UseVisualStyleBackColor = true;
            Page_begin_button_false.Click += Page_begin_button_false_Click;
            // 
            // Page_begin_button_true
            // 
            Page_begin_button_true.FlatAppearance.BorderSize = 0;
            Page_begin_button_true.FlatAppearance.MouseDownBackColor = SystemColors.Control;
            Page_begin_button_true.FlatAppearance.MouseOverBackColor = SystemColors.Control;
            Page_begin_button_true.FlatStyle = FlatStyle.Flat;
            Page_begin_button_true.ForeColor = SystemColors.MenuHighlight;
            Page_begin_button_true.Location = new Point(-1, 438);
            Page_begin_button_true.Name = "Page_begin_button_true";
            Page_begin_button_true.Size = new Size(931, 63);
            Page_begin_button_true.TabIndex = 1;
            Page_begin_button_true.Text = "OpenerGame By kkss202";
            Page_begin_button_true.UseVisualStyleBackColor = true;
            Page_begin_button_true.Click += Page_begin_button_true_Click;
            // 
            // page_begin
            // 
            AutoScaleDimensions = new SizeF(9F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(931, 500);
            Controls.Add(Page_begin_button_true);
            Controls.Add(Page_begin_button_false);
            Name = "page_begin";
            Text = "开了opener-Hi";
            ResumeLayout(false);
        }

        #endregion

        private Button Page_begin_button_false;
        private Button Page_begin_button_true;
    }
}