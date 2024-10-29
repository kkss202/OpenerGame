namespace OpenerGame
{
    partial class page_1
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(page_1));
            Page_1_textbox_question = new TextBox();
            Page_1_textbox_answer = new TextBox();
            Page_1_button_chick = new Button();
            SuspendLayout();
            // 
            // Page_1_textbox_question
            // 
            Page_1_textbox_question.BackColor = SystemColors.Control;
            Page_1_textbox_question.BorderStyle = BorderStyle.None;
            Page_1_textbox_question.Cursor = Cursors.No;
            Page_1_textbox_question.Enabled = false;
            Page_1_textbox_question.Font = new Font("Microsoft YaHei UI", 16.2F, FontStyle.Regular, GraphicsUnit.Point, 134);
            Page_1_textbox_question.Location = new Point(58, 31);
            Page_1_textbox_question.Multiline = true;
            Page_1_textbox_question.Name = "Page_1_textbox_question";
            Page_1_textbox_question.ShortcutsEnabled = false;
            Page_1_textbox_question.Size = new Size(814, 80);
            Page_1_textbox_question.TabIndex = 0;
            Page_1_textbox_question.TabStop = false;
            Page_1_textbox_question.Text = "第一题：（真的一点也不难）在下面输入框中打出“'齾'”，即可通关（别想Ctrl+C）";
            Page_1_textbox_question.TextAlign = HorizontalAlignment.Center;
            // 
            // Page_1_textbox_answer
            // 
            Page_1_textbox_answer.Location = new Point(147, 228);
            Page_1_textbox_answer.Name = "Page_1_textbox_answer";
            Page_1_textbox_answer.Size = new Size(440, 27);
            Page_1_textbox_answer.TabIndex = 1;
            Page_1_textbox_answer.KeyDown += Page_1_textbox_answer_KeyDown;
            // 
            // Page_1_button_chick
            // 
            Page_1_button_chick.Location = new Point(674, 226);
            Page_1_button_chick.Name = "Page_1_button_chick";
            Page_1_button_chick.Size = new Size(94, 29);
            Page_1_button_chick.TabIndex = 2;
            Page_1_button_chick.Text = "确定";
            Page_1_button_chick.UseVisualStyleBackColor = true;
            Page_1_button_chick.Click += Page_1_button_chick_Click;
            // 
            // page_1
            // 
            AutoScaleDimensions = new SizeF(9F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(Page_1_button_chick);
            Controls.Add(Page_1_textbox_answer);
            Controls.Add(Page_1_textbox_question);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "page_1";
            Text = "开了opener-第一关";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox Page_1_textbox_question;
        private TextBox Page_1_textbox_answer;
        private Button Page_1_button_chick;
    }
}