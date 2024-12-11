from io import TextIOWrapper
from datetime import datetime


class SQLGenerator:
    @staticmethod
    def sql_append_academic_years(
        file_handle: TextIOWrapper,
        year: list[str],
        clear_all: bool = False,
    ) -> None:
        """
        Generates SQL insert statement for academic_years table.

        Args:
            file_handle (TextIOWrapper): File handle to write SQL statements
            year (str): Academic year to insert
        """
        sql = ""
        if clear_all:
            sql += "DELETE FROM public.academic_years;\n"

        for y in year:
            sql += (
                f"INSERT INTO public.academic_years (year)"
                f" VALUES ('{y}')"
                f" ON CONFLICT (year) DO NOTHING;\n"
            )
        file_handle.write(sql + "\n")

    @staticmethod
    def sql_append_programs(
        programs: set,
        authority: str,
        file_handle: TextIOWrapper,
        clear_all: bool = False,
    ) -> None:
        """
        Generates SQL insert statements for programs table.

        Args:
            programs (set): Set of program names to insert
            authority (str): Authority domain name
            file_handle (TextIOWrapper): File handle to write SQL statements
        """
        sql = ""
        if clear_all:
            sql += "DELETE FROM public.programs;\n"

        for program in programs:
            sql += (
                f"INSERT INTO public.programs (name, authority)"
                f" VALUES ('{program}', '{authority}')"
                f" ON CONFLICT (name) DO NOTHING;\n"
            )
        file_handle.write(sql + "\n")

    @staticmethod
    def sql_append_branches(
        branches: list[dict],
        authority: str,
        file_handle: TextIOWrapper,
        clear_all: bool = False,
    ) -> None:
        """
        Generates SQL insert statements for branches table.

        Args:
            branches (list[dict]): List of dictionaries containing branch details
            authority (str): Authority domain name
            file_handle (TextIOWrapper): File handle to write SQL statements
        """
        sql = ""
        if clear_all:
            sql += "DELETE FROM public.branches;\n"

        for branch in branches:
            sql += (
                f"INSERT INTO public.branches (branch_name, program, authority)"
                f" VALUES ('{branch["branch_name"]}', '{branch["program"]}', '{authority}')"
                f" ON CONFLICT (branch_name, program) DO NOTHING;\n"
            )
        file_handle.write(sql + "\n")

    @staticmethod
    def sql_append_semesters(
        semesters: list[dict],
        authority: str,
        file_handle: TextIOWrapper,
        clear_all: bool = False,
    ) -> None:
        """
        Generates SQL insert statements for semesters table.

        Args:
            semesters (list[dict]): List of dictionaries containing semester details
            authority (str): Authority domain name
            file_handle (TextIOWrapper): File handle to write SQL statements
        """
        sql = ""
        if clear_all:
            sql += "DELETE FROM public.semesters;\n"

        for semester in semesters:
            sql += (
                f"INSERT INTO public.semesters (semester_name, branch_name, program_name, academic_year, authority)"
                f" VALUES ('{semester["semester_name"]}', '{semester["branch_name"]}', '{semester["program_name"]}', '{semester["academic_year"]}', '{authority}')"
                f" ON CONFLICT (semester_name, branch_name, program_name, academic_year, authority) DO NOTHING;\n"
            )
        file_handle.write(sql + "\n")

    @staticmethod
    def sql_append_sections(
        sections: list[dict],
        authority: str,
        file_handle: TextIOWrapper,
        clear_all: bool = False,
    ) -> None:
        """
        Generates SQL insert statements for sections table.

        Args:
            sections (list[dict]): List of dictionaries containing section details
            authority (str): Authority domain name
            file_handle (TextIOWrapper): File handle to write SQL statements
        """
        sql = ""
        if clear_all:
            sql += "DELETE FROM public.section;\n"

        for section in sections:
            sql += (
                f"INSERT INTO public.section (section_name, semester_name, branch, program, academic_year, authority)"
                f" VALUES ('{section["section_name"]}', '{section["semester_name"]}', '{section["branch_name"]}', '{section["program_name"]}', '{section["academic_year"]}', '{authority}')"
                f" ON CONFLICT (section_name, branch, semester_name, program, academic_year, authority) DO NOTHING;\n"
            )

        file_handle.write(sql + "\n")

    @staticmethod
    def sql_append_student_schedule(
        schedules: list[dict],
        authority: str,
        file_handle: TextIOWrapper,
        clear_all: bool = False,
    ) -> None:
        """
        Generates SQL insert statements for student_schedule table.

        Args:
            schedules (list[dict]): List of dictionaries containing schedule details
            authority (str): Authority domain name
            file_handle (TextIOWrapper): File handle to write SQL statements
        """
        sql = ""
        if clear_all:
            sql += "DELETE FROM public.student_schedule;\n"
        for schedule in schedules:
            sql += (
                f"INSERT INTO public.student_schedule ("
                f" section, semester, day, branch, program, academic_year,"
                f" subject, start_time, end_time, classroom, faculty_id, authority)"
                f" VALUES ('{schedule["section"]}', '{schedule["semester"]}', '{schedule["day"]}','{schedule["branch"]}', '{schedule["program"]}', '{schedule["academic_year"]}',"
                f" '{schedule["subject"]}', '{schedule["start_time"]}', '{schedule["end_time"]}',"
                f" '{schedule["classroom"]}',"
                f" {f"'{schedule["faculty_id"]}'" if schedule["faculty_id"] != '' else r'null'}"
                f", '{authority}')"
                f" ON CONFLICT DO NOTHING;\n"
            )

        file_handle.write(sql + "\n")
