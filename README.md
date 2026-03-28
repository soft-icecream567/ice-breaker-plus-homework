# 人机写作报告——第二次人工智能编程作业

## 1.任务拆解与AI协作策略

在编写代码，以及让AI编写代码之前，我先将项目拆分成多个步骤
1. 定义 Student 这一数据类型
2. 定义 ExamSystem 这一控制类型
3. 实现文件读取功能
4. 实现学号查找功能
5. 实现随机点名功能
6. 实现考场安排表生成
7. 实现准考证文件夹生成
随后让AI对我的思路进行了检查，随后对项目的步骤进行了重新审视和补充
补充后，形成了较为完成清晰的实践思路：
1. 定义 Student 数据类
2. 定义 ExamSystem 控制类框架
3. 实现文件读取功能————AI提示需要考虑异常学号输入处理
4. 实现学号查找功能
5. 实现随机点名功能————AI提示需要包含输入异常点名人数处理
6. 实现考场安排表生成————AI提示需要包含生成时间
7. 实现准考证文件夹生成
8. 整合主程序交互逻辑————重点：AI提示，需要编写主程序给用户提供交互界面
9. 添加逐行代码注释————检查AI核心代码的注释，更贴合本次作业的要求

初步设想让AI在1、2、3、4、5点进行辅助，主要代码为人工编写，在部分复杂语法不太清晰时才调用AI
6、7点核心代码为AI生成，人工注释代码功能并更改变量名保证代码兼容性
随后发现主程序（提供用户交互界面）未编写，在AI输出main函数的调用模型后，人工填写代码并保证和前面ExamSystem和Student类兼容

## 2 核心Prompt迭代记录

以 **6——生成考场安排表** 为例：

### 第一代prompt：
“生成一个生成考场安排表的函数。考场安排表包括考生的座位、姓名和学号三个参数。座位要求你按照学生名单顺序依次生成。学生的名单包含学生的姓名和学号。学生的姓名和学号来自变量self.class。要求你把生成后的考场安排表保存到一个新的‘考场安排表.txt’中。”

**问题：**
- 没有说明函数定义在class ExamSystem中，因此并未使用self.students作为学生名单，而是使用self_class作为学生名单
- 没有打乱顺序——在prompt中没有说明乱序，直接按照原名单生成
- 没有在第一行生成考场安排表的文件生成时间

### 第二代prompt：
“注意函数定义在类中，因此函数接收变量应该为self，调用时学生名单储存在self.students中。同时注意名单自行乱序排列。考场安排表第一行需要展示文件生成的时间，使用格式化时间”

**问题：** 
- 少了很多，基本仅有————直接更改self.students的名单，使其直接打乱，导致无法兼容整个项目

### 第三代prompt：
“注意这是一整个项目，因此我需要你另外保存乱序的学生名单，保存在另一个列表中”

**问题：无**
- 至此基本生成兼容的、功能完整、贴合要求的代码

## 3. Debug 与异常处理记录

### 报错类型：FileNotFoundError
**现象**：程序启动时找不到学生名单文件，程序崩溃

**解决过程**：
- 我首先检查了文件是否存在于当前目录，发现文件存在但程序仍然报错
- 将错误信息喂给 AI 分析，AI 指出可能是路径问题或编码问题
- 我先使用 `os.path.exists()` 检查文件是否存在，发现文件存在
- 再使用print`os.path.abspath(__file__)`确认文件路径是否正确，发现由于查找使用相对路径，但是文件处在访问的下级
- 使用`current_dir = os.path.dirname(os.path.abspath(__file__))`，现查找路径，再更改访问路径，使不同环境都可以轻松访问文件
- 在 `load_students` 方法中添加 `try-except` 捕获 `FileNotFoundError`，提高文件兼容性


### 报错类型：ValueError
**现象**：在index_student函数中，发现无论如何都无法查询学生，哪怕查询存在的学号

**解决过程**：
- 使用`print(self.students[i])`,`print(type(student.student_id))`,`print(type(student_id))`，比较加载的数据中学号和输入查找的学号，比较查看bug
- 发现student.student_id是str类型，而在外部输入查找的student_id被转换成了int，因此两者无法比较，永远无法查询到学生
- 将int()强转换删除
- 在 `main()` 函数的随机点名分支中添加 `try-except` 捕获 `ValueError`，使得函数兼容性更好

### 错误类型：变量名不兼容（多次出现）
**现象**：程序报错，发现查找不到对应可调用的函数（e.g can't find 'find_list', did you mean 'index_students'?）

**解决过程**
- 查看traceback定位line
- 回溯之前定义的函数，发现__init__中定义的是index_student，但是后面调用是find_list

**现象**：程序报错，发现查找不到变量（can't find 'institude'）

**解决过程**
- 回溯traceback查找变量名
- 发现'学院'在__init__ 中我设置的时college，但是在后面load_students中使用的是institude

## 4. 人工代码审查

以下是 AI 生成的核心代码，我添加了逐行中文注释：

```python
    #生成考场座位安排表
    def generate_exam_arrangement(self):
        #AI编写核心代码
        # 复制学生列表，避免影响原始数据
        # copy() 创建列表的浅拷贝，不影响内部 Student 对象
        shuffled_students = self.students.copy()
        
        random.shuffle(shuffled_students)# 随机打乱顺序（原地修改）
        
        #引入time 内置模块，获取当前时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")#输出格式化时间
        
        output_lines = []#储存文件内容的列表
        
        #第一行打印输出文件的生成时间
        output_lines.append(f"生成时间：{current_time}")

        output_lines.append("座位号\t姓名\t学号")#第二行是表例
        
        #遍历打乱后的学生列表，分配座位号
        #使用 enumerate 返回 (索引, 元素)，start=1 让索引从1开始
        for index, student in enumerate(shuffled_students, start=1):
            output_lines.append(f"{index}\t{student.name}\t{student.student_id}")#将打乱后的学生信息依次添入表中
        
        #文件写入
        try:
            with open("考场座位安排表.txt",'w') as file:
                file.write('\n'.join(output_lines))#挨个写入学生名单
            print("成功生成考场安排表:考场安排表.txt")
            return shuffled_students #返回打乱后的学生名单，用于后续生成准考证
        
        except Exception as e:#另外设置错误提示
            print(f"生成考场安排表错误{e}")
            return []

    #生成准考证
    def generate_admission_files(self,list_students):
        #首先检查是否存在同名文件夹，便于后续代码debug
        folder_name='准考证'

        if not os.path.exists(folder_name):#检验是否存在文件夹
            os.makedirs(folder_name)#无文件夹则生成文件夹
            print(f"已生成文件夹{folder_name}")
        else:
            print(f"已存在{folder_name}文件夹")

        #AI生成核心代码——单个学生准考证内容写入，人工更改变量名适配前面的变量

        for index, student in enumerate(list_students, start=1):#批量生成准考证，enumerate方便索引时代码更简洁
            #使得所生成的文件名格式为 01.txt、02.txt...

            #/反斜杠分隔符，确保生成的每个准考证都进入准考证文件夹
            file_name = f"{folder_name}/{index:02d}.txt" #{:02d} 表示格式化为两位数字，不足两位补零
            
            #content 中保存每个学生的独立信息——座位号、姓名、学号
            content = f"座位号：{index}\n姓名：{student.name}\n学号：{student.student_id}"

            with open(file_name,'w') as file:
                file.write(content)#写入文件
            
        print('完成准考证的生成')


<details>
<summary>考场管理系统完整代码</summary>

```python
    import random
    import time
    import os 

    class Student:#创建student类
        def __init__(self,name,gender,class_name,institude,student_id):
            #保存学生的各项信息
            self.name=name
            self.gender=gender
            self.class_name=class_name
            self.institude=institude
            self.student_id=student_id
        def __str__(self):
            #打印学生信息
            return f"姓名：{self.name},学号：{self.student_id},性别：{self.gender},班级：{self.class_name},学院：{self.institude}"

    #创建ExamSystem逻辑控制类——负责点名、查找、生成文件
    class ExamSystem:
        #ExamSystem框架
        #导入学生名单,进行信息初始化
        def __init__(self,file_path):
            self.file_path=file_path #保存文件信息
            self.students=[] #储存所有学生
            self.load_students() #AI编写 解释：将文件信息加载到内存中

        @staticmethod #静态方法对学号格式进行校验
        def examine_student_id(student_id):
            #判断学号长度是否为数字
            flag=student_id.isdigit()
            #判断学号长度是否合规
            if len(student_id)!=7:
                flag=False
            #判断学号前四位是否为对应年份
            if int(student_id[0:4])<=2001 or int(student_id[0:4])>=2026:
                flag=False
            
            return flag
        
        def load_students(self):
            #使用try-except检查文件是否异常
            current_dir=os.path.dirname(os.path.abspath(__file__))
            os.chdir(current_dir)
            try:#路径存在
                with open('人工智能编程语言学生名单.txt','r',encoding='utf-8') as file:
                    #全部读取，储存在列表中
                    context=file.readlines()[1:]
                    #[1:]跳过表头的信息栏
                    for line in context:
                        #AI编写 分割信息，strip() 去除首尾空白，split('\t') 按制表符分割
                        parts = line.strip().split('\t')
                        print(parts)
                        if len(parts) >= 6:# 确保每行都有学号、姓名、性别、班级、学院
                            #创建 Student 对象并添加到列表
                            student = Student(
                                student_id=parts[4],    # 学号
                                name=parts[1],          # 姓名
                                gender=parts[2],        # 性别
                                class_name=parts[3],    # 班级
                                institude=parts[5]        # 学院
                            )
                            self.students.append(student)

            #文件不存在报错
            except FileNotFoundError:#AI编写，找不到文件时的报错
                print(f"错误：找不到文件 '{self.file_path}'")
                
                exit(1)#AI编写-退出程序,并设置退出输出为1
            
        #实现学号查功能
        def index_student(self,student_id):
            #从保存学生信息的students里面搜索学号)
            for student in self.students:
                if student.student_id==student_id:
                    print(student.name)
                    return student
                
            print("无法找到该学生，请重新输入学号")#排除可能该出现的查找不到的情况
            return  

        #实现随机点名功能
        def call_student(self,count):
            if isinstance(count,int)==False:#输入非数字——main的主函数调用中也排除了这个问题
                print("人数输入格式错误")
                return
            if count >len(self.students):#人数超过总人数
                print("点名人数超过总人数")
                return 
            
            #ai编写 实现随机抽取样本
            selected=random.sample(self.students,count)#利用random内置函数实现随意抽取样本功能
            return selected
        
        #生成考场座位安排表
        def generate_exam_arrangement(self):
            #AI编写核心代码
            # 复制学生列表，避免影响原始数据
            # copy() 创建列表的浅拷贝，不影响内部 Student 对象
            shuffled_students = self.students.copy()
            
            random.shuffle(shuffled_students)# 随机打乱顺序（原地修改）
            
            #引入time 内置模块，获取当前时间
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")#输出格式化时间
            
            output_lines = []#储存文件内容的列表
            
            #第一行打印输出文件的生成时间
            output_lines.append(f"生成时间：{current_time}")

            output_lines.append("座位号\t姓名\t学号")#第二行是表例
            
            #遍历打乱后的学生列表，分配座位号
            #使用 enumerate 返回 (索引, 元素)，start=1 让索引从1开始
            for index, student in enumerate(shuffled_students, start=1):
                output_lines.append(f"{index}\t{student.name}\t{student.student_id}")#将打乱后的学生信息依次添入表中
            
            #文件写入
            try:
                with open("考场座位安排表.txt",'w') as file:
                    file.write('\n'.join(output_lines))#挨个写入学生名单
                print("成功生成考场安排表:考场安排表.txt")
                return shuffled_students #返回打乱后的学生名单，用于后续生成准考证
            
            except Exception as e:#另外设置错误提示
                print(f"生成考场安排表错误{e}")
                return []

        #生成准考证
        def generate_admission_files(self,list_students):
            #首先检查是否存在同名文件夹，便于后续代码debug
            folder_name='准考证'

            if not os.path.exists(folder_name):#检验是否存在文件夹
                os.makedirs(folder_name)#无文件夹则生成文件夹
                print(f"已生成文件夹{folder_name}")
            else:
                print(f"已存在{folder_name}文件夹")

            #AI生成核心代码——单个学生准考证内容写入，人工更改变量名适配前面的变量

            for index, student in enumerate(list_students, start=1):#批量生成准考证，enumerate方便索引时代码更简洁
                #使得所生成的文件名格式为 01.txt、02.txt...

                #/反斜杠分隔符，确保生成的每个准考证都进入准考证文件夹
                file_name = f"{folder_name}/{index:02d}.txt" #{:02d} 表示格式化为两位数字，不足两位补零
                
                #content 中保存每个学生的独立信息——座位号、姓名、学号
                content = f"座位号：{index}\n姓名：{student.name}\n学号：{student.student_id}"

                with open(file_name,'w') as file:
                    file.write(content)#写入文件
                
            print('完成准考证的生成')
        
        #ai提示需要补充交互界面
        #生成主函数，实现与用户的交互界面
    def main():
        #AI提示——让用户输入需要完成的功能
        #确保路径正确
        current_dir=os.path.dirname(os.path.abspath(__file__))
        os.chdir(current_dir)
        #AI编写核心代码
        #调用ExamSystem，加载学生数据，将ExamSysetm类赋给system，实现后续功能
        system=ExamSystem('人工智能编程语言学生名单.txt')
        #显示总人数方便后用户了解名单基本情况，后续调用减少出错可能
        print(f"名单中共有{len(system.students)}位学生")

        while True:
            #显示功能菜单
            print("\n\n考场管理系统：")
            print("1. 查询学生信息")
            print("2. 随机点名")
            print("3. 生成考场安排表与准考证")#必须同时生成，否则准考证信息与考场安排表无法对应
            print("4. 退出系统")

            #让用户选择实现的功能
        
            choice=input("请输入想实现的功能：")

            #AI生成else-if语句，这里改成match语句更加清晰
            match choice:
                case '1':#学号查询
                    student_id = input("请输入学号：")
                    student = system.index_student(student_id)#调用ExamSystem中的查找学号func
                    if student:#未找到返回None，则找到时，bool值为True
                        print("\n查询结果：")
                        print(student)#打印找到的结果，打印学生的各项信息
                    else:
                        print(f"未找到学号为 {student_id} 的学生")#未找到学生情况
                
                case '2':#随机点名
                    #使用try-except解决出现的ValueError问题
                    try:
                        count_input = input("请输入点名人数：")#用户输入点名人数

                        count = int(count_input)  #转换为整数，若出现ValueError则转换成except的输出
                        
                        #调用ExamSystem中随机点名的方法
                        selected = system.call_student(count)

                        if selected:#如果返回值不是None
                            print(f"\n随机点名结果（共{count}人）：")
                            for i, student in enumerate(selected, 1):#使用enumerate对学生进行索引，依次输出，更加简洁
                                print(f"{i}. {student.name} ({student.student_id})")
                    except ValueError:
                            #异常处理非数字输入
                            print("错误——请输入有效的数字")
                
                case '3':#生成考场安排表，同时生成准考证
                    #必须同时生成，以为每一次安排学生是乱序的，考场安排表必须和准考证同时生成
                    arranged=system.generate_exam_arrangement()#调用生成
                    
                    #打印准考证
                    if arranged:
                        system.generate_admission_files(arranged)
                
                case'4':
                    print("感谢使用，已退出程序")#退出程序
                    break

                case _:
                    print("无效输入，请重新输入")#输入数字无效，不再1-4的范围内
                    
    #ai编写——创建程序入口点
    #当运行此文件时，__name__=__main__,执行main()

    if __name__=='__main__':
        main()
