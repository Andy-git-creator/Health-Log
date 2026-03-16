def bmr():
    a = 0.0
    b = 0.0
    c = 0.0

    print("请输入您的年龄：")
    age = int(input())
    print("请选择性别：1.男 2.女")
    gender = int(input())
    print("请输入您的身高：(cm)")
    height = int(input())
    print("请输入您前一天晚上睡前称的体重：")
    A = float(input())
    print("请输入您今天早上空腹（不上厕所也不喝水）称的体重：")
    B = float(input())
    m = A - B

    if m > 0.8:
        print("代谢良好")
    elif m > 0.4:
        print("代谢正常")
    elif m >= 0.0:
        print("代谢差")

    if gender == 1:
        bmr = 10 * B + 6.25 * height - 5 * age + 5
    if gender == 2:
        bmr = 10 * B + 5.25 * height - 5 * age - 161
    print(f"您今日需摄入\033[32m{bmr:.2f}\033[0m大卡！")