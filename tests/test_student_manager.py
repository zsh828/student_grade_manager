import pytest
from src.student_manager import StudentManager


class TestAddStudent:
    """测试添加学生功能"""

    def setup_method(self):
        self.manager = StudentManager()

    def test_add_valid_student_success(self):
        """测试添加有效学生返回True"""
        result = self.manager.add_student("S001", "Alice", "Class A")
        assert result is True
        assert "S001" in self.manager.students
        assert self.manager.students["S001"]["name"] == "Alice"
        assert self.manager.students["S001"]["class_name"] == "Class A"

    def test_add_duplicate_student_returns_false(self):
        """测试添加重复学号的学生返回False"""
        self.manager.add_student("S001", "Alice", "Class A")
        result = self.manager.add_student("S001", "Bob", "Class B")
        assert result is False
        # 确保原有数据未被覆盖
        assert self.manager.students["S001"]["name"] == "Alice"

    def test_add_student_with_empty_id_raises_error(self):
        """测试使用空学号添加学生抛出ValueError"""
        with pytest.raises(ValueError, match="学号、姓名和班级不能为空"):
            self.manager.add_student("", "Alice", "Class A")

    def test_add_student_with_empty_name_raises_error(self):
        """测试使用空姓名添加学生抛出ValueError"""
        with pytest.raises(ValueError, match="学号、姓名和班级不能为空"):
            self.manager.add_student("S002", "", "Class A")

    def test_add_student_with_empty_class_raises_error(self):
        """测试使用空班级添加学生抛出ValueError"""
        with pytest.raises(ValueError, match="学号、姓名和班级不能为空"):
            self.manager.add_student("S003", "Charlie", "")


class TestRecordGrade:
    """测试录入成绩功能"""

    def setup_method(self):
        self.manager = StudentManager()
        self.manager.add_student("S001", "Alice", "Class A")

    def test_record_valid_grade_success(self):
        """测试录入有效成绩返回True"""
        result = self.manager.record_grade("S001", "Math", 95.5)
        assert result is True
        assert self.manager.grades["S001"]["Math"] == 95.5

    def test_record_grade_updates_existing_subject(self):
        """测试更新已有科目的成绩"""
        self.manager.record_grade("S001", "Math", 80)
        self.manager.record_grade("S001", "Math", 90)
        assert self.manager.grades["S001"]["Math"] == 90.0

    def test_record_grade_for_non_existent_student_raises_error(self):
        """测试为不存在的学生录入成绩抛出ValueError"""
        with pytest.raises(ValueError, match="学生不存在"):
            self.manager.record_grade("S999", "Math", 80)

    def test_record_grade_above_100_raises_error(self):
        """测试录入超过100分的成績抛出ValueError"""
        with pytest.raises(ValueError, match="分数必须在 0 到 100 之间"):
            self.manager.record_grade("S001", "Math", 101)

    def test_record_grade_below_0_raises_error(self):
        """测试录入负分的成绩抛出ValueError"""
        with pytest.raises(ValueError, match="分数必须在 0 到 100 之间"):
            self.manager.record_grade("S001", "Math", -5)

    def test_record_grade_with_empty_subject_raises_error(self):
        """测试使用空科目名称录入成绩抛出ValueError"""
        with pytest.raises(ValueError, match="科目名称不能为空"):
            self.manager.record_grade("S001", "", 80)


class TestGetStudentGrades:
    """测试查询学生成绩功能"""

    def setup_method(self):
        self.manager = StudentManager()
        self.manager.add_student("S001", "Alice", "Class A")
        self.manager.record_grade("S001", "Math", 90)
        self.manager.record_grade("S001", "English", 85)

    def test_get_grades_returns_correct_dict(self):
        """测试获取学生成绩返回正确的字典"""
        grades = self.manager.get_student_grades("S001")
        assert grades == {"Math": 90.0, "English": 85.0}

    def test_get_grades_for_non_existent_student_returns_none(self):
        """测试查询不存在学生的成绩返回None"""
        result = self.manager.get_student_grades("S999")
        assert result is None

    def test_get_grades_for_student_with_no_grades_returns_empty_dict(self):
        """测试查询未录入成绩的学生返回空字典"""
        self.manager.add_student("S002", "Bob", "Class A")
        result = self.manager.get_student_grades("S002")
        assert result == {}


class TestCalculateClassAverage:
    """测试计算班级平均分功能"""

    def setup_method(self):
        self.manager = StudentManager()
        self.manager.add_student("S001", "Alice", "Class A")
        self.manager.add_student("S002", "Bob", "Class A")
        self.manager.record_grade("S001", "Math", 90)
        self.manager.record_grade("S001", "English", 80)
        self.manager.record_grade("S002", "Math", 70)
        self.manager.record_grade("S002", "English", 60)

    def test_calculate_average_for_known_class(self):
        """测试计算已知班级的平均分"""
        # 总分: 90+80+70+60 = 300
        # 总科目次数: 4
        # 平均: 300 / 4 = 75.0
        avg = self.manager.calculate_class_average("Class A")
        assert avg == 75.0

    def test_calculate_average_for_non_existent_class_returns_none(self):
        """测试计算不存在的班级平均分返回None"""
        result = self.manager.calculate_class_average("Class Z")
        assert result is None

    def test_calculate_average_for_class_with_no_grades_returns_none(self):
        """测试计算没有成绩记录的班级平均分返回None"""
        self.manager.add_student("S003", "Charlie", "Class B")
        result = self.manager.calculate_class_average("Class B")
        assert result is None


class TestGetRanking:
    """测试排名功能"""

    def setup_method(self):
        self.manager = StudentManager()
        # Setup Class A
        self.manager.add_student("S001", "Alice", "Class A")
        self.manager.add_student("S002", "Bob", "Class A")
        self.manager.add_student("S003", "Charlie", "Class A")
        
        # Alice: Math=90, English=90 -> Total 180
        self.manager.record_grade("S001", "Math", 90)
        self.manager.record_grade("S001", "English", 90)
        
        # Bob: Math=100, English=80 -> Total 180
        self.manager.record_grade("S002", "Math", 100)
        self.manager.record_grade("S002", "English", 80)
        
        # Charlie: Math=80 -> Total 80
        self.manager.record_grade("S003", "Math", 80)

    def test_ranking_sort_by_total_score_descending(self):
        """测试排名按总分降序排列"""
        ranking = self.manager.get_ranking("Class A")
        # Alice and Bob are tied at 180, Charlie is 80
        assert ranking[2][0] == "S003"
        assert ranking[2][1] == 80.0

    def test_ranking_tie_breaker_by_student_id_ascending(self):
        """测试总分相同时按学号升序排列"""
        ranking = self.manager.get_ranking("Class A")
        # Alice (S001) and Bob (S002) both have 180. S001 < S002
        assert ranking[0][0] == "S001"
        assert ranking[1][0] == "S002"
        
        # Verify names as well
        assert ranking[0][2] == "Alice"
        assert ranking[1][2] == "Bob"

    def test_ranking_for_non_existent_class_returns_empty_list(self):
        """测试查询不存在班级的排名返回空列表"""
        ranking = self.manager.get_ranking("Class Z")
        assert ranking == []

    def test_ranking_order_is_correct(self):
        """测试完整排名顺序正确"""
        ranking = self.manager.get_ranking("Class A")
        expected_ids = ["S001", "S002", "S003"]
        actual_ids = [item[0] for item in ranking]
        assert actual_ids == expected_ids