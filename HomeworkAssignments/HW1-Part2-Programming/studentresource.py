from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from resources import BaseResource
from db import DB
from models import Student

KV = Dict[str, Any]

class StudentResource(BaseResource):
    TABLE_NAME = "student"
    def __init__(self, db: DB):
        self.db = db

    @staticmethod
    def parse_student(raw_dict: KV) -> Optional[Student]:
        """Attempts to fit key-value pairs into a Student model.

        :param raw_dict: The key-value pairs
        :returns: A Student model if raw_dict represents a valid one;
                  otherwise, None
        """
        try:
            return Student(**raw_dict)
        except ValidationError:
            return None

    def get_all(self, filters: KV) -> List[Student]:
        """Gets all students that satisfy the specified filters.

        :param filters: Key-value pairs that the returned rows must satisfy.
                        An empty dict and None are treated the same.
        :returns: A list of students that satisfy filters
        """
        rows = self.db.select(self.TABLE_NAME, filters)
        res = [self.parse_student(row) for row in rows]
        return res

    # TODO: all methods below

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Gets a student by their ID.

        :param student_id: The ID to be matched
        :returns: The student with ID student_id, or None if none exists
        """
        row = self.db.select(self.TABLE_NAME, {'ID':student_id})
        if row:
            return self.parse_student(row[0])
        else:
            return None

    def create(self, student: Student) -> int:
        """Creates a student.

        :param student: The student to be created
        :returns: The number of students created
        """
        student_dict = {'ID': student.ID, 'name': student.name}

        if student.dept_name:
            student_dict['dept_name'] = student.dept_name
        if student.tot_cred:
            student_dict['tot_cred'] = student.tot_cred
        row = self.db.insert(self.TABLE_NAME,student_dict)
        return row

    def update(self, student_id: int, values: KV) -> int:
        """Updates a student.

        :param student_id: The ID of the student to be updated
        :param values: The new values for the student
        :returns: The number of rows affected. If student_id != student.ID,
                  then immediately return 0 without any updating.
        """
        if 'ID' in values and student_id != values['ID']:
            return 0
        return self.db.update(self.TABLE_NAME, values, {'ID':student_id})
        pass

    def delete(self, student_id: int) -> int:
        """Deletes a student.

        :param student_id: The ID of the student to be deleted
        :returns: The number of rows affected
        """
        return self.db.delete(self.TABLE_NAME,{'ID':student_id})
        pass
