import time
import json
import matplotlib.pyplot as plt


def body_data_recorder():

    DATA_FILE = "body_data.json"
    body_data_list = []

    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['grid.alpha'] = 0.3

    def get_current_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def input_number(prompt, min_val=None, max_val=None):
        while True:
            try:
                num = float(input(prompt))
                if min_val is not None and num < min_val:
                    print(f"输入错误！数值不能小于{min_val}，请重新输入")
                    continue
                if max_val is not None and num > max_val:
                    print(f"输入错误！数值不能大于{max_val}，请重新输入")
                    continue
                return num
            except ValueError:
                print("输入错误！请输入数字（整数/小数均可），请重新输入")

    def input_blood_pressure():
        while True:
            systolic = input_number("请输入收缩压（mmHg）：", 60, 250)
            diastolic = input_number("请输入舒张压（mmHg）：", 40, 150)
            if systolic > diastolic:
                return systolic, diastolic
            else:
                print("\033[31m输入错误！收缩压必须大于舒张压！请重新输入\033[0m")

    def save_data_to_file():
        #数据保存到json文件
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(body_data_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ \033[31m数据保存失败：{e}\033[0m")

    def load_data_from_file():
        #程序启动时从json加载数据
        nonlocal body_data_list
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                body_data_list = json.load(f)
            print(f"✅ \033[32m成功加载{len(body_data_list)}条历史身体数据！\033[0m")
        except FileNotFoundError:
            print("ℹ️ \033[31m未找到历史数据文件，将新建记录\033[0m")
        except Exception as e:
            print(f"⚠️  \033[31m加载历史数据失败：{e}，将新建记录\033[0m")

    def add_body_data():
        #录入一条新的身体数据
        print("\n===== 开始录入身体数据 =====")
        heart_rate = input_number("请输入心率（次/分）：", 30, 250)
        systolic, diastolic = input_blood_pressure()
        weight = input_number("请输入体重（kg）：", 0.1)

        # 构造单条数据
        single_data = {
            "记录时间": get_current_time(),
            "心率(次/分)": heart_rate,
            "收缩压(mmHg)": systolic,
            "舒张压(mmHg)": diastolic,
            "体重(kg)": weight
        }
        body_data_list.append(single_data)
        save_data_to_file()
        print("✅数据录入成功！已自动保存到本地")

    def show_all_data():
        #内部函数 查看所有已记录的身体数据
        if not body_data_list:
            print("\n⚠️暂无任何身体数据记录，请先录入！")
            return
        print("\n===== 所有身体数据记录 =====")
        for index, data in enumerate(body_data_list, start=1):
            print(f"\n【第{index}条记录】")
            for key, value in data.items():
                # 数字保留1位小数
                print(f"  {key}：{value:.1f}" if isinstance(value, (int, float)) else f"  {key}：{value}")
        print(f"\n📊 共记录了 {len(body_data_list)} 条身体数据")

    def plot_data_trend():
        #绘制身体数据趋势折线图
        if not body_data_list or len(body_data_list) < 1:
            print("\033[31m\n⚠️ 暂无足够数据绘制图表！\033[0m")
            return

        print("\n📈 正在绘制数据趋势折线图，请稍候...")
        x = list(range(1, len(body_data_list) + 1))  # x轴：第1、2、3...条记录
        heart_rates = [d["心率(次/分)"] for d in body_data_list]
        systolic_list = [d["收缩压(mmHg)"] for d in body_data_list]
        diastolic_list = [d["舒张压(mmHg)"] for d in body_data_list]
        weights = [d["体重(kg)"] for d in body_data_list]

        # 创建2行2列的子图，总标题为身体数据趋势
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, tight_layout=True)
        fig.suptitle('身体数据变化趋势图（按记录顺序）', fontsize=16, fontweight='bold')

        # 定义绘图通用函数（减少重复代码）
        def plot_subplot(ax, y_data, title, y_label, color):
            ax.plot(x, y_data, marker='o', linewidth=2, markersize=6, color=color, label=title)
            ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel('记录序号', fontsize=10)
            ax.set_ylabel(y_label, fontsize=10)
            ax.grid(True, linestyle='-')
            ax.set_xticks(x)  # x轴刻度对应记录序号
            # 标注数据点数值（保留1位小数）
            for xi, yi in zip(x, y_data):
                ax.text(xi, yi, f"{yi:.1f}", ha='center', va='bottom', fontsize=8)

        # 绘制4个子图（分别对应心率、收缩压、舒张压、体重）
        plot_subplot(ax1, heart_rates, '心率变化', '心率(次/分)', '#e74c3c')  # 红色
        plot_subplot(ax2, systolic_list, '收缩压变化', '收缩压(mmHg)', '#3498db')  # 蓝色
        plot_subplot(ax3, diastolic_list, '舒张压变化', '舒张压(mmHg)', '#2ecc71')  # 绿色
        plot_subplot(ax4, weights, '体重变化', '体重(kg)', '#f39c12')  # 橙色

        # 显示图表
        plt.show()
        print("✅ 图表绘制完成！关闭图表窗口可返回菜单")

    print("=" * 20 + " 身体数据记录工具 " + "=" * 20)
    load_data_from_file()  #加载历史数据
    while True:
        # 展示交互菜单
        print("\n请选择操作：")
        print("1. 录入新的身体数据")
        print("2. 查看所有已记录数据")
        print("3. 绘制数据趋势折线图")
        print("4. 退出程序")
        choice = input("请输入数字1/2/3/4：")
        if choice == "1":
            add_body_data()
        elif choice == "2":
            show_all_data()
        elif choice == "3":
            plot_data_trend()  # 调用绘图函数
        elif choice == "4":
            print("\n👋 程序已退出，所有数据已自动保存到本地！")
            break
        else:
            print("❌ 输入错误！请输入1、2、3或4，重新选择")
