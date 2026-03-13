import tkinter as tk
from tkinter import ttk, messagebox
import time
import json
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 配置matplotlib支持中文和负号
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['grid.alpha'] = 0.3

# 数据文件路径（确保在当前程序目录）
DATA_FILE = os.path.join(os.path.dirname(__file__), "body_data.json")
body_data_list = []


class HealthCalculatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("健康计算器 v1.0")
        self.root.geometry("800x600")  # 窗口大小
        self.root.resizable(True, True)  # 允许调整大小

        # 加载历史数据
        self.load_data_from_file()

        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 1. BMI/CMI计算标签页
        self.create_bmi_cmi_tab()

        # 2. 身体数据记录标签页
        self.create_data_record_tab()

        # 3. 历史记录查看标签页
        self.create_history_tab()

        # 4. 数据可视化标签页
        self.create_visualization_tab()

        # 5. 关于我们标签页
        self.create_about_tab()

    # ========== 通用函数 ==========
    def load_data_from_file(self):
        """加载历史数据"""
        global body_data_list
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                body_data_list = json.load(f)
            messagebox.showinfo("提示", f"成功加载{len(body_data_list)}条历史数据！")
        except FileNotFoundError:
            messagebox.showinfo("提示", "未找到历史数据文件，将新建记录")
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败：{str(e)}，将新建记录")

    def save_data_to_file(self):
        """保存数据到JSON文件"""
        global body_data_list
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(body_data_list, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"保存数据失败：{str(e)}")
            return False

    def get_float_input(self, entry, prompt, min_val=None, max_val=None):
        """验证输入为数字并返回浮点数"""
        try:
            num = float(entry.get().strip())
            if min_val is not None and num < min_val:
                messagebox.showerror("输入错误", f"数值不能小于{min_val}！")
                entry.focus()
                return None
            if max_val is not None and num > max_val:
                messagebox.showerror("输入错误", f"数值不能大于{max_val}！")
                entry.focus()
                return None
            return num
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字（整数/小数均可）！")
            entry.focus()
            return None

    # ========== 1. BMI/CMI计算标签页 ==========
    def create_bmi_cmi_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="BMI/CMI计算")

        # 选择计算类型
        ttk.Label(tab, text="计算类型：", font=("微软雅黑", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.calc_type = tk.StringVar(value="BMI")
        ttk.Radiobutton(tab, text="BMI（身体质量指数）", variable=self.calc_type,
                        value="BMI", command=self.switch_calc_type).grid(row=0, column=1, padx=5, pady=10)
        ttk.Radiobutton(tab, text="CMI（心脏代谢指数）", variable=self.calc_type,
                        value="CMI", command=self.switch_calc_type).grid(row=0, column=2, padx=5, pady=10)

        # 动态生成输入框（初始显示BMI输入项）
        self.calc_frame = ttk.Frame(tab)
        self.calc_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W)
        self.bmi_widgets = self.create_bmi_widgets()
        self.cmi_widgets = self.create_cmi_widgets()
        self.switch_calc_type()  # 初始化显示

        # 计算按钮
        ttk.Button(tab, text="开始计算", command=self.calculate_bmi_cmi,
                   style="Accent.TButton").grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        # 结果显示
        self.result_label = ttk.Label(tab, text="计算结果：", font=("微软雅黑", 12))
        self.result_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W)

    def create_bmi_widgets(self):
        """创建BMI计算的输入控件"""
        widgets = {}
        # 标准选择
        ttk.Label(self.calc_frame, text="参考标准：").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.bmi_standard = tk.StringVar(value="亚洲")
        ttk.Radiobutton(self.calc_frame, text="亚洲标准", variable=self.bmi_standard, value="亚洲").grid(row=0,
                                                                                                         column=1,
                                                                                                         padx=5, pady=5)
        ttk.Radiobutton(self.calc_frame, text="国际标准", variable=self.bmi_standard, value="国际").grid(row=0,
                                                                                                         column=2,
                                                                                                         padx=5, pady=5)

        # 身高
        ttk.Label(self.calc_frame, text="身高（cm）：").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        widgets["height"] = ttk.Entry(self.calc_frame, width=20)
        widgets["height"].grid(row=1, column=1, padx=5, pady=5)

        # 体重
        ttk.Label(self.calc_frame, text="体重（kg）：").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        widgets["weight"] = ttk.Entry(self.calc_frame, width=20)
        widgets["weight"].grid(row=1, column=3, padx=5, pady=5)
        return widgets

    def create_cmi_widgets(self):
        """创建CMI计算的输入控件"""
        widgets = {}
        # 身高
        ttk.Label(self.calc_frame, text="身高（cm）：").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        widgets["height"] = ttk.Entry(self.calc_frame, width=20)
        widgets["height"].grid(row=0, column=1, padx=5, pady=5)

        # 腰围
        ttk.Label(self.calc_frame, text="腰围（cm）：").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        widgets["waist"] = ttk.Entry(self.calc_frame, width=20)
        widgets["waist"].grid(row=0, column=3, padx=5, pady=5)

        # 甘油三酯
        ttk.Label(self.calc_frame, text="甘油三酯（mmol/L）：").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        widgets["tg"] = ttk.Entry(self.calc_frame, width=20)
        widgets["tg"].grid(row=1, column=1, padx=5, pady=5)

        # 高密度脂蛋白胆固醇
        ttk.Label(self.calc_frame, text="高密度脂蛋白胆固醇（mmol/L）：").grid(row=1, column=2, padx=5, pady=5,
                                                                            sticky=tk.W)
        widgets["hdl"] = ttk.Entry(self.calc_frame, width=20)
        widgets["hdl"].grid(row=1, column=3, padx=5, pady=5)
        return widgets

    def switch_calc_type(self):
        """切换BMI/CMI输入框显示"""
        # 隐藏所有控件
        for widget in self.calc_frame.winfo_children():
            widget.grid_forget()
        # 显示对应控件
        if self.calc_type.get() == "BMI":
            for widget in self.bmi_widgets.values():
                widget.grid()
            self.bmi_widgets["height"].focus()
        else:
            for widget in self.cmi_widgets.values():
                widget.grid()
            self.cmi_widgets["height"].focus()

    def calculate_bmi_cmi(self):
        """计算BMI或CMI并显示结果"""
        if self.calc_type.get() == "BMI":
            self.calculate_bmi()
        else:
            self.calculate_cmi()

    def calculate_bmi(self):
        """计算BMI"""
        height = self.get_float_input(self.bmi_widgets["height"], "身高", min_val=50, max_val=250)
        weight = self.get_float_input(self.bmi_widgets["weight"], "体重", min_val=1, max_val=500)
        if height is None or weight is None:
            return

        # 计算BMI
        bmi = weight / ((height / 100) ** 2)
        bmi_str = f"BMI = {bmi:.2f}"

        # 判断范围
        standard = self.bmi_standard.get()
        if standard == "亚洲":
            if bmi < 18.5:
                status = "低体重（营养不足）"
                color = "#e74c3c"  # 红色
            elif 18.5 <= bmi < 23.0:
                status = "正常体重"
                color = "#2ecc71"  # 绿色
            elif 23.0 <= bmi < 25.0:
                status = "肥胖前期（超重）"
                color = "#f39c12"  # 橙色
            elif 25.0 <= bmi < 30.0:
                status = "一级肥胖（中度肥胖）"
                color = "#9b59b6"  # 紫色
            else:
                status = "二级肥胖（严重肥胖）"
                color = "#e74c3c"  # 红色
        else:  # 国际标准
            if bmi < 18.5:
                status = "低体重（营养不足）"
                color = "#e74c3c"
            elif 18.5 <= bmi < 25.0:
                status = "正常体重"
                color = "#2ecc71"
            elif 25.0 <= bmi < 30.0:
                status = "肥胖前状态（超重）"
                color = "#f39c12"
            elif 30.0 <= bmi < 35.0:
                status = "肥胖I级（中度肥胖）"
                color = "#3498db"  # 蓝色
            elif 35.0 <= bmi < 40.0:
                status = "肥胖II类（严重肥胖）"
                color = "#9b59b6"
            else:
                status = "⚠️肥胖III类（极端肥胖）"
                color = "#e74c3c"

        # 显示结果
        self.result_label.config(text=f"计算结果：{bmi_str} - {status}", foreground=color)

    def calculate_cmi(self):
        """计算CMI"""
        height = self.get_float_input(self.cmi_widgets["height"], "身高", min_val=50, max_val=250)
        waist = self.get_float_input(self.cmi_widgets["waist"], "腰围", min_val=30, max_val=200)
        tg = self.get_float_input(self.cmi_widgets["tg"], "甘油三酯", min_val=0.1, max_val=50)
        hdl = self.get_float_input(self.cmi_widgets["hdl"], "高密度脂蛋白胆固醇", min_val=0.1, max_val=20)
        if None in [height, waist, tg, hdl]:
            return

        # 计算CMI
        cmi = (waist / height) * (tg / hdl)
        cmi_str = f"CMI = {cmi:.2f}"

        # 判断范围
        if cmi <= 0.85:
            status = "正常"
            color = "#2ecc71"
        elif cmi > 1.42:
            status = "高风险"
            color = "#e74c3c"
        else:
            status = "有风险"
            color = "#f39c12"

        # 显示结果
        self.result_label.config(text=f"计算结果：{cmi_str} - {status}", foreground=color)

    # ========== 2. 数据记录标签页 ==========
    def create_data_record_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="身体数据记录")

        # 心率
        ttk.Label(tab, text="心率（次/分）：", font=("微软雅黑", 10)).grid(row=0, column=0, padx=10, pady=8, sticky=tk.W)
        self.hr_entry = ttk.Entry(tab, width=20)
        self.hr_entry.grid(row=0, column=1, padx=5, pady=8)

        # 收缩压
        ttk.Label(tab, text="收缩压（mmHg）：", font=("微软雅黑", 10)).grid(row=1, column=0, padx=10, pady=8, sticky=tk.W)
        self.systolic_entry = ttk.Entry(tab, width=20)
        self.systolic_entry.grid(row=1, column=1, padx=5, pady=8)

        # 舒张压
        ttk.Label(tab, text="舒张压（mmHg）：", font=("微软雅黑", 10)).grid(row=1, column=2, padx=10, pady=8, sticky=tk.W)
        self.diastolic_entry = ttk.Entry(tab, width=20)
        self.diastolic_entry.grid(row=1, column=3, padx=5, pady=8)

        # 体重
        ttk.Label(tab, text="体重（kg）：", font=("微软雅黑", 10)).grid(row=2, column=0, padx=10, pady=8, sticky=tk.W)
        self.weight_entry = ttk.Entry(tab, width=20)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=8)

        # 保存按钮
        ttk.Button(tab, text="保存数据", command=self.save_body_data,
                   style="Accent.TButton").grid(row=3, column=0, columnspan=4, padx=10, pady=15)

    def save_body_data(self):
        """保存身体数据"""
        # 验证输入
        hr = self.get_float_input(self.hr_entry, "心率", min_val=30, max_val=250)
        systolic = self.get_float_input(self.systolic_entry, "收缩压", min_val=60, max_val=250)
        diastolic = self.get_float_input(self.diastolic_entry, "舒张压", min_val=40, max_val=150)
        weight = self.get_float_input(self.weight_entry, "体重", min_val=0.1, max_val=500)

        if None in [hr, systolic, diastolic, weight]:
            return

        # 验证收缩压>舒张压
        if systolic <= diastolic:
            messagebox.showerror("输入错误", "收缩压必须大于舒张压！")
            self.systolic_entry.focus()
            return

        # 构造数据
        single_data = {
            "记录时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "心率(次/分)": hr,
            "收缩压(mmHg)": systolic,
            "舒张压(mmHg)": diastolic,
            "体重(kg)": weight
        }

        # 保存数据
        global body_data_list
        body_data_list.append(single_data)
        if self.save_data_to_file():
            messagebox.showinfo("成功", "数据保存成功！")
            # 清空输入框
            self.hr_entry.delete(0, tk.END)
            self.systolic_entry.delete(0, tk.END)
            self.diastolic_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)

    # ========== 3. 历史记录查看标签页 ==========
    def create_history_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="历史记录")

        # 滚动条 + 文本框显示历史记录
        scrollbar = ttk.Scrollbar(tab)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_text = tk.Text(tab, yscrollcommand=scrollbar.set, font=("微软雅黑", 9))
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.history_text.yview)

        # 刷新按钮
        ttk.Button(tab, text="刷新记录", command=self.show_history_data).pack(padx=10, pady=5)
        self.show_history_data()  # 初始化显示

    def show_history_data(self):
        """显示历史记录"""
        self.history_text.delete(1.0, tk.END)  # 清空文本框
        global body_data_list
        if not body_data_list:
            self.history_text.insert(tk.END, "暂无历史数据，请先录入！", "red")
            return

        # 拼接历史数据
        history_str = "===== 身体数据历史记录 =====\n\n"
        for idx, data in enumerate(body_data_list, 1):
            history_str += f"【第{idx}条】\n"
            for key, val in data.items():
                if isinstance(val, (int, float)):
                    history_str += f"  {key}：{val:.1f}\n"
                else:
                    history_str += f"  {key}：{val}\n"
            history_str += "\n"
        history_str += f"总计：{len(body_data_list)}条记录"

        self.history_text.insert(tk.END, history_str)
        # 设置文本不可编辑
        self.history_text.config(state=tk.DISABLED)

    # ========== 4. 数据可视化标签页 ==========
    def create_visualization_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="数据可视化")

        # 绘图按钮
        ttk.Button(tab, text="绘制趋势图", command=self.plot_data_trend,
                   style="Accent.TButton").pack(padx=10, pady=20)

        # 绘图区域
        self.fig = plt.Figure(figsize=(10, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def plot_data_trend(self):
        """绘制数据趋势图"""
        global body_data_list
        if len(body_data_list) < 1:
            messagebox.showwarning("提示", "暂无足够数据绘制图表！")
            return

        # 清空画布
        self.fig.clear()

        # 提取数据
        x = list(range(1, len(body_data_list) + 1))
        heart_rates = [d["心率(次/分)"] for d in body_data_list]
        systolic_list = [d["收缩压(mmHg)"] for d in body_data_list]
        diastolic_list = [d["舒张压(mmHg)"] for d in body_data_list]
        weights = [d["体重(kg)"] for d in body_data_list]

        # 创建2x2子图
        ax1 = self.fig.add_subplot(221)
        ax2 = self.fig.add_subplot(222)
        ax3 = self.fig.add_subplot(223)
        ax4 = self.fig.add_subplot(224)

        # 绘制子图
        def plot_subplot(ax, y_data, title, y_label, color):
            ax.plot(x, y_data, marker='o', linewidth=2, markersize=6, color=color)
            ax.set_title(title, fontweight='bold')
            ax.set_xlabel('记录序号')
            ax.set_ylabel(y_label)
            ax.grid(True, linestyle='-', alpha=0.3)
            ax.set_xticks(x)
            # 标注数值
            for xi, yi in zip(x, y_data):
                ax.text(xi, yi, f"{yi:.1f}", ha='center', va='bottom', fontsize=8)

        plot_subplot(ax1, heart_rates, '心率变化', '心率(次/分)', '#e74c3c')
        plot_subplot(ax2, systolic_list, '收缩压变化', '收缩压(mmHg)', '#3498db')
        plot_subplot(ax3, diastolic_list, '舒张压变化', '舒张压(mmHg)', '#2ecc71')
        plot_subplot(ax4, weights, '体重变化', '体重(kg)', '#f39c12')

        # 总标题
        self.fig.suptitle('身体数据变化趋势图', fontsize=14, fontweight='bold')
        self.fig.tight_layout()

        # 更新画布
        self.canvas.draw()

    # ========== 5. 关于我们标签页 ==========
    def create_about_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="关于我们")

        info_text = """
        健康计算器 v1.0
        开发者：Chen Zeyue
        邮箱：czyandy@tmu.edu.cn
        GitHub：Andy-git-creator

        功能说明：
        1. BMI/CMI计算：支持亚洲/国际标准的BMI计算、CMI心脏代谢指数计算
        2. 数据记录：记录心率、血压、体重等身体数据
        3. 历史查看：查看所有已记录的身体数据
        4. 数据可视化：绘制数据趋势折线图，直观查看变化
        """
        ttk.Label(tab, text=info_text, font=("微软雅黑", 11), justify=tk.LEFT).pack(padx=20, pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    # 设置ttk样式
    style = ttk.Style(root)
    style.configure("Accent.TButton", font=("微软雅黑", 10), padding=5)
    app = HealthCalculatorUI(root)
    root.mainloop()