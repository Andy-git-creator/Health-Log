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
    print("您每周的运动情况为：\n1.完全没有 2.1-3次 3.3-5次\n4.每天运动 5.每天重度运动")
    a = int(input())

    m = A - B
    if m > 0.8:
        print("代谢良好")
    elif m > 0.4:
        print("代谢正常")
    elif m >= 0.0:
        print("代谢差")

    if gender == 1:
        bmr = 10 * B + 6.25 * height - 5 * age + 5
    elif gender == 2:
        bmr = 10 * B + 5.25 * height - 5 * age - 161

    if a == 1:
        C = 1.2
    elif a == 2:
        C = 1.3
    elif a == 3:
        C = 1.5
    elif a == 4:
        C = 1.7
    elif a == 5:
        C = 1.9
    else:
        print("\033[31m输入错误！\033[0m")


    K = bmr * C
    print(f"您今日需摄入\033[32m{K:.2f}\033[0m大卡！")
