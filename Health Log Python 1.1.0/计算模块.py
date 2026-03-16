def body_data_calculater():
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
    e = 0.0
    CMI = 0.0
    BMI = 0.0

    print("请输入要计算的指数: 1.BMI 2.CMI 请输入1/2:")
    m = (input())

    if m == "2":
        #计算CMI
        print("\033[34m心脏代谢指数（CMI）是一个综合性指标，用于评估个体的心血管代谢健康状况，预测心血管疾病和代谢紊乱（如代谢综合征）的风险。\033[0m")
        print("\033[34mCMI结合了腰围、甘油三酯和高密度脂蛋白胆固醇的数值，反映了内脏脂肪堆积和脂质代谢异常的综合影响。\033[0m")
        print("请输入身高，单位cm:")
        a = float(input())
        print("请输入腰围，单位cm:")
        b = float(input())
        print("请输入甘油三酯(TG)，单位mmol/L:")
        c = float(input())
        print("请输入高密度脂蛋白胆固醇(好胆固醇)，单位mmol/L:")
        d = float(input())
        CMI = (b / a) * (c / d)
        print(f"CMI={CMI:.4f}，约为{CMI:.2f}，", end="")
        if CMI <= 0.85:
            print("\033[32m正常\033[0m")
        elif CMI > 1.42:
            print("\033[31m高风险\033[0m")
        else:
            print("\033[33m有风险\033[0m")

    elif m == "1":
        #计算BMI
        print("\033[34m身体质量指数（Body Mass Index，BMI），简称体质指数，"
              "是国际上常用的衡量人体胖瘦程度以及是否健康的一个标准。\033[0m")
        print("\033[34m其核心逻辑是将身高与体重的关系数字化，通过简单公式判断体重是否处于“健康范围”。"
              "计算公式为： BMI=体重（千克）÷身高的平方（米）\033[0m")
        print("使用亚洲(1)/国际(2)标准？(输入1或2)")
        standard = int(input())
        print("请输入身高，单位cm:")
        a = float(input())
        print("请输入体重，单位kg:")
        e = float(input())
        BMI = e / (a / 100) / (a / 100)
        print(f"BMI={BMI:.4f}，约为{BMI:.2f}，", end="")
        if standard == 1:
            #亚洲标准
            if BMI < 18.5:
                print("\033[31m低体重（营养不足）\033[0m")
            if (BMI >= 18.5) and (BMI < 23.0):
                print("\033[32m正常体重\033[0m")
            if (BMI >= 23.0) and (BMI < 25.0):
                print("\033[33m肥胖前期（超重）\033[0m")
            if (BMI >= 25.0) and (BMI < 30.0):
                print("\033[35m一级肥胖（中度肥胖）\033[0m")
            if BMI >= 30.0:
                print("\033[31m二级肥胖（严重肥胖）\033[0m")
        if standard == 2:
            #国际标准
            if BMI < 18.5:
                print("\033[31m低体重（营养不足）\033[0m")
            if (BMI >= 18.5) and (BMI < 25.0):
                print("\033[32m正常体重\033[0m")
            if (BMI >= 25.0) and (BMI < 30.0):
                print("\033[33m肥胖前状态（超重）\033[0m")
            if (BMI >= 30.0) and (BMI < 35.0):
                print("\033[34m肥胖I级（中度肥胖）\033[0m")
            if (BMI >= 35.0) and (BMI < 40.0):
                print("\033[35m肥胖II类（严重肥胖）\033[0m")
            if BMI >= 40.0:
                print("\033[31m⚠️肥胖III类（极端肥胖）\033[0m")
    else:
        print("\033[31m输入错误！\033[0m")