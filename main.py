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
        
        
