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

  