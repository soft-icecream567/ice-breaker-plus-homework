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
        self.load_students() #ai编写 解释：将文件信息加载到内存中

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
    
    def read_list(self):
        #使用try-except检查文件是否异常
        
        try:#路径存在
            with open('人工智能编程语言学生名单.txt','r') as file:
                #全部读取，储存在列表中
                context=file.readlines()[1:]
                #[1:]跳过表头的信息栏
                for line in context:
                    #ai编写 分割信息，strip() 去除首尾空白，split('\t') 按制表符分割
                    parts = line.strip().split('\t')
                    
                    if len(parts) >= 5:# 确保每行都有学号、姓名、性别、班级、学院
                        # 人工注释：创建 Student 对象并添加到列表
                        student = Student(
                            student_id=parts[0],    # 学号
                            name=parts[1],          # 姓名
                            gender=parts[2],        # 性别
                            class_name=parts[3],    # 班级
                            college=parts[4]        # 学院
                        )
                        self.students.append(student)
                    
                        
        #文件不存在报错
        except FileNotFoundError:#ai 编写，找不到文件时的报错
            print(f"错误：找不到文件 '{self.file_path}'")
            
            exit(1)#ai编写 退出程序
        
    #实现学号查功能
    def index_student(self,student_id):
        #从保存学生信息的students里面
        for student in self.students:
            if student.student_id==student_id:
                return student
        print("无法找到该学生，请重新输入学号")#排除可能该出现的查找不到的情况
        return  

    def call_student(self,count):
        if isinstance(count,int)==False :
            print("人数输入格式错误")
            return
        if count >len(self.stdents):
            print("点名人数超过总人数")
            return 
        
        #ai编写 实现随机抽取样本
        selected=random.sample(self.students,count)#利用random内置函数实现随意抽取样本功能
        return selected
    
    #生成考场座位安排表
    def generate_exam_seats(self):
        #ai 编写
        # 复制学生列表，避免影响原始数据
        # copy() 创建列表的浅拷贝，不影响内部 Student 对象
        shuffled_students = self.students.copy()
        
        random.shuffle(shuffled_students)# 随机打乱顺序（原地修改）
        
        #引入time 内置模块，获取当前时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")#输出格式化时间
        
        output_lines = []#储存文件内容的列表
        
        #输出文件的生成时间
        output_lines.append(f"生成时间：{current_time}")

        output_lines.append("座位号\t姓名\t学号")#第二行是表例
        
        #遍历打乱后的学生列表，分配座位号
        #使用 enumerate 返回 (索引, 元素)，start=1 让索引从1开始
        for index, student in enumerate(shuffled_students, start=1):
            output_lines.append(f"{index}\t{student.name}\t{student.student_id}")#将打乱后的学生信息依次添入表中
        
        #文件写入
        try:
            with open("考场座位安排表.txt",'w') as file:
                file.wirte('\n'.join(output_lines))#挨个写入学生名单
            print("成功生成考场安排表:考场安排表.txt")
            return shuffled_students #返回打乱后的学生名单，用于后续生成准考证
        
        except Exception as e:#另外设置错误提示
            print(f"生成考场安排表错误{e}")
            return []

    #生成准考证
    def generate_admission_files(self,list_students):
        #首先检查是否存在同名文件夹，便于后续代码debug
        folder_name='准考证'

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"已生成文件夹{folder_name}")
        else:
            print(f"已存在{folder_name}文件夹")

        #ai生成部分——单个学生准考证内容写入，人工更改变量名

        for index, student in enumerate(list_students, start=1):#批量生成准考证
            #使得所生成的文件名格式为 01.txt、02.txt...
            
            file_name = f"{folder_name}/{index:02d}.txt" #{:02d} 表示格式化为两位数字，不足两位补零
            
            #content 中保存每个学生的独立信息——座位号、姓名、学号
            content = f"座位号：{index}\n姓名：{student.name}\n学号：{student.student_id}"

            with open(file_name,'w') as file:
                file.wirte(content)
            
        print('完成准考证的生成')
    

        
