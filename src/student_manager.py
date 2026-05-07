"""
学生成绩管理系统核心逻辑模块。
提供添加学生、录入成绩、查询成绩、计算平均分和排名的功能。
数据存储在内存中（字典结构），适用于演示或小型应用。
"""

from typing import Dict, List, Optional, Tuple


class StudentManager:
    """管理学生信息和成绩的类。"""

    def __init__(self):
        # 存储学生基本信息: {student_id: {"name": str, "class_name": str}}
        self.students: Dict[str, dict] = {}
        # 存储成绩信息: {student_id: {subject: score}}
        self.grades: Dict[str, Dict[str, float]] = {}

    def add_student(self, student_id: str, name: str, class_name: str) -> bool:
        """
        添加一名学生。
        
        Args:
            student_id: 学号，必须唯一且非空。
            name: 姓名，非空。
            class_name: 班级名称，非空。
            
        Returns:
            bool: 如果添加成功返回 True，如果学号已存在则返回 False。
        """
        if not student_id or not name or not class_name:
            raise ValueError("学号、姓名和班级不能为空")
        
        if student_id in self.students:
            return False
        
        self.students[student_id] = {
            "name": name,
            "class_name": class_name
        }
        # 初始化该学生的成绩字典
        self.grades[student_id] = {}
        return True

    def record_grade(self, student_id: str, subject: str, score: float) -> bool:
        """
        录入学生成绩。
        
        Args:
            student_id: 学号。
            subject: 科目名称。
            score: 分数，必须在 0-100 之间。
            
        Returns:
            bool: 如果录入成功返回 True，如果学生不存在或分数无效则抛出异常。
        """
        if student_id not in self.students:
            raise ValueError(f"学生不存在: {student_id}")
        
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValueError("分数必须在 0 到 100 之间")
        
        if not subject:
            raise ValueError("科目名称不能为空")

        self.grades[student_id][subject] = float(score)
        return True

    def get_student_grades(self, student_id: str) -> Optional[Dict[str, float]]:
        """
        查询学生所有科目的成绩。
        
        Args:
            student_id: 学号。
            
        Returns:
            dict: 包含所有科目及分数的字典，如果学生不存在则返回 None。
        """
        if student_id not in self.students:
            return None
        
        return self.grades.get(student_id, {})

    def calculate_class_average(self, class_name: str) -> Optional[float]:
        """
        计算指定班级的平均分。
        平均分定义为：该班级所有学生所有科目分数的总和 / (学生人数 * 科目种类数)。
        注意：这里采用更常见的“全班总均分”定义，即所有分数的算术平均值。
        如果班级没有学生或没有成绩，返回 None。
        
        Args:
            class_name: 班级名称。
            
        Returns:
            float: 平均分，如果班级不存在或无数据则返回 None。
        """
        # 找出属于该班级的所有学生ID
        students_in_class = [
            sid for sid, info in self.students.items()
            if info["class_name"] == class_name
        ]
        
        if not students_in_class:
            return None
        
        total_score = 0.0
        total_subjects_count = 0
        
        for sid in students_in_class:
            grades = self.grades.get(sid, {})
            if grades:
                total_score += sum(grades.values())
                total_subjects_count += len(grades)
        
        if total_subjects_count == 0:
            return None
            
        return total_score / total_subjects_count

    def get_ranking(self, class_name: str) -> List[Tuple[str, float, str]]:
        """
        按总分对指定班级的学生进行排名。
        排序规则：总分降序；总分相同，按学号升序。
        
        Args:
            class_name: 班级名称。
            
        Returns:
            list of tuples: [(student_id, total_score, name), ...]
        """
        # 找出属于该班级的所有学生ID
        students_in_class = [
            sid for sid, info in self.students.items()
            if info["class_name"] == class_name
        ]
        
        if not students_in_class:
            return []
        
        ranking_list = []
        for sid in students_in_class:
            grades = self.grades.get(sid, {})
            total_score = sum(grades.values())
            name = self.students[sid]["name"]
            ranking_list.append((sid, total_score, name))
        
        # 排序：主要按总分降序 (-x[1])，次要按学号升序 (x[0])
        ranking_list.sort(key=lambda x: (-x[1], x[0]))
        
        return ranking_list