using System;
using System.Drawing;
using System.Windows.Forms;

namespace Lab5_TuringMachineGUI_v1
{
    partial class Form1
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;
        private TextBox inputTextBox; // Добавлено поле для ввода входного слова
        private System.Windows.Forms.Label resultLabel;


        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        //private void InitializeComponent()
        //{
        //    this.components = new System.ComponentModel.Container();
        //    this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
        //    this.ClientSize = new System.Drawing.Size(800, 450);
        //    this.Text = "Form1";
        //}

        private void InitializeComponent()
        {
            this.tapePictureBox = new System.Windows.Forms.PictureBox();
            this.runButton = new System.Windows.Forms.Button();
            this.stateLabel = new System.Windows.Forms.Label();
            this.headLabel = new System.Windows.Forms.Label();
            this.autoMoveButton = new System.Windows.Forms.Button();
            this.inputTextBox = new System.Windows.Forms.TextBox();
            this.buttonInput = new System.Windows.Forms.Button();
            this.resultLabel = new System.Windows.Forms.Label();
            this.pictureBox2 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.tapePictureBox)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            this.SuspendLayout();
            // 
            // tapePictureBox
            // 
            this.tapePictureBox.Location = new System.Drawing.Point(12, 12);
            this.tapePictureBox.Name = "tapePictureBox";
            this.tapePictureBox.Size = new System.Drawing.Size(1116, 129);
            this.tapePictureBox.TabIndex = 0;
            this.tapePictureBox.TabStop = false;
            // 
            // runButton
            // 
            this.runButton.BackColor = System.Drawing.Color.Teal;
            this.runButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.runButton.Font = new System.Drawing.Font("GOST type A", 21.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.runButton.ForeColor = System.Drawing.Color.White;
            this.runButton.Location = new System.Drawing.Point(1008, 308);
            this.runButton.Name = "runButton";
            this.runButton.Size = new System.Drawing.Size(120, 35);
            this.runButton.TabIndex = 1;
            this.runButton.Text = "1 шаг";
            this.runButton.UseVisualStyleBackColor = false;
            this.runButton.Click += new System.EventHandler(this.RunButton_Click);
            // 
            // stateLabel
            // 
            this.stateLabel.AutoSize = true;
            this.stateLabel.Font = new System.Drawing.Font("GOST type A", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.stateLabel.Location = new System.Drawing.Point(7, 170);
            this.stateLabel.Name = "stateLabel";
            this.stateLabel.Size = new System.Drawing.Size(100, 25);
            this.stateLabel.TabIndex = 2;
            this.stateLabel.Text = "Состояние:";
            // 
            // headLabel
            // 
            this.headLabel.AutoSize = true;
            this.headLabel.Font = new System.Drawing.Font("GOST type A", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.headLabel.Location = new System.Drawing.Point(12, -3);
            this.headLabel.Name = "headLabel";
            this.headLabel.Size = new System.Drawing.Size(238, 25);
            this.headLabel.TabIndex = 3;
            this.headLabel.Text = "Позиция головки автомата";
            // 
            // autoMoveButton
            // 
            this.autoMoveButton.BackColor = System.Drawing.Color.Teal;
            this.autoMoveButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.autoMoveButton.Font = new System.Drawing.Font("GOST type A", 72F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.autoMoveButton.ForeColor = System.Drawing.Color.White;
            this.autoMoveButton.Location = new System.Drawing.Point(674, 359);
            this.autoMoveButton.Name = "autoMoveButton";
            this.autoMoveButton.Size = new System.Drawing.Size(465, 299);
            this.autoMoveButton.TabIndex = 4;
            this.autoMoveButton.Text = "Старт";
            this.autoMoveButton.UseVisualStyleBackColor = false;
            this.autoMoveButton.Click += new System.EventHandler(this.autoMoveButton_Click);
            // 
            // inputTextBox
            // 
            this.inputTextBox.Font = new System.Drawing.Font("Segoe UI", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.inputTextBox.Location = new System.Drawing.Point(131, 170);
            this.inputTextBox.Name = "inputTextBox";
            this.inputTextBox.Size = new System.Drawing.Size(689, 25);
            this.inputTextBox.TabIndex = 5;
            this.inputTextBox.TextChanged += new System.EventHandler(this.inputTextBox_TextChanged);
            // 
            // buttonInput
            // 
            this.buttonInput.BackColor = System.Drawing.Color.Teal;
            this.buttonInput.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonInput.Font = new System.Drawing.Font("GOST type A", 18F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.buttonInput.ForeColor = System.Drawing.Color.White;
            this.buttonInput.Location = new System.Drawing.Point(826, 170);
            this.buttonInput.Name = "buttonInput";
            this.buttonInput.Size = new System.Drawing.Size(111, 39);
            this.buttonInput.TabIndex = 6;
            this.buttonInput.Text = "Ввод";
            this.buttonInput.UseVisualStyleBackColor = false;
            this.buttonInput.Click += new System.EventHandler(this.buttonInput_Click);
            // 
            // resultLabel
            // 
            this.resultLabel.AutoSize = true;
            this.resultLabel.Font = new System.Drawing.Font("GOST type A", 18F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.resultLabel.Location = new System.Drawing.Point(16, 331);
            this.resultLabel.Name = "resultLabel";
            this.resultLabel.Size = new System.Drawing.Size(106, 25);
            this.resultLabel.TabIndex = 7;
            this.resultLabel.Text = "Результат:";
            this.resultLabel.Click += new System.EventHandler(this.resultLabel_Click);
            // 
            // pictureBox2
            // 
            this.pictureBox2.Location = new System.Drawing.Point(17, 359);
            this.pictureBox2.Name = "pictureBox2";
            this.pictureBox2.Size = new System.Drawing.Size(633, 489);
            this.pictureBox2.TabIndex = 8;
            this.pictureBox2.TabStop = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 17F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.DarkSalmon;
            this.ClientSize = new System.Drawing.Size(1140, 884);
            this.Controls.Add(this.pictureBox2);
            this.Controls.Add(this.buttonInput);
            this.Controls.Add(this.inputTextBox);
            this.Controls.Add(this.autoMoveButton);
            this.Controls.Add(this.headLabel);
            this.Controls.Add(this.stateLabel);
            this.Controls.Add(this.runButton);
            this.Controls.Add(this.tapePictureBox);
            this.Controls.Add(this.resultLabel);
            this.Font = new System.Drawing.Font("Segoe UI", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.ForeColor = System.Drawing.Color.Black;
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Машина Тьюринга";
            ((System.ComponentModel.ISupportInitialize)(this.tapePictureBox)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private Button autoMoveButton;
        private Button buttonInput;
        private PictureBox pictureBox2;
    }
}

