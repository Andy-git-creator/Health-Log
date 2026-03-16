# 陈泽悦 czyAndy czyandy@tmu.edu.cn czyandyac@gmail.com
# github: Andy-git-creator

print(" ============ 欢迎使用 ============ ")

while True:
    print("请选择操作：")
    print("1. 计算BMI/CMI")
    print("2. 记录数据")
    print("3. 健康管家")
    print("4. 安全退出")
    print("5. 联系我们")
    choice = input ("请输入数字1/2/3/4/5：\n")

    if choice == "1":
        from 计算模块 import body_data_calculater
        body_data_calculater()
        print("==================")
    elif choice == "2":
        from 记录模块 import body_data_recorder
        body_data_recorder()
        print("==================")
    elif choice == "3":
        print("正在测试，完整功能敬请期待!")
        from 基础代谢测试模块 import bmr
        bmr()
        print("==================")
    elif choice == "4":
        print("感谢使用！👋 ")
        break
    elif choice == "5":
        print("ℹ️\nemail: czyandyac@gmail.com\n"
              "github: Andy-git-creator\n")
        print("==================")
    else:
        print("❌输入错误！输入1/2/3/4/5")