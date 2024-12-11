from helpers.get_time_slots import get_time_slots
from helpers.day_from_abbr import day_from_abbr
from helpers.sql_generator import SQLGenerator
import frozendict
from csv import DictReader
from io import TextIOWrapper

# Wether to clear all data from
# tables before inserting new data
clear_all = True


def sql_append_faculty(migration_file: TextIOWrapper):
    with open("./gen-sql/sample-faculty.csv", mode="r") as faculty_file:
        csv_reader = DictReader(faculty_file)
        faculty = []
        for row in csv_reader:
            faculty.append(
                {
                    "faculty_id": row["faculty_id"],
                    "faculty_name": row["faculty_name"],
                }
            )
        SQLGenerator.sql_append_faculty(faculty, "kiit.ac.in", migration_file)


def generate_sql_migration(file_path):
    with open(file_path, mode="r") as file:
        csv_reader = DictReader(file)
        time_slots = get_time_slots(csv_reader)

        unique_year = set()
        unique_program = set()  # Set of {program_name, year}
        unique_branch = set()  # Set of {branch_name, program_name, year}
        unique_semester = (
            set()
        )  # Set of {semester_name, branch_name, program_name, year}
        unique_sections = (
            set()
        )  # Set of {semester_name, branch_name, program_name, year}
        schedules = []

        for row in csv_reader:
            year = row["Academic Year"]
            program = row["Program"]
            branch = row["Branch"]
            semester = row["Semester"]

            unique_year.add(year)
            unique_program.add(program)
            unique_branch.add(
                frozendict.frozendict(
                    {
                        "branch_name": branch,
                        "program": program,
                        "year": year,
                    }
                )
            )
            unique_semester.add(
                frozendict.frozendict(
                    {
                        "semester_name": semester,
                        "branch_name": branch,
                        "program_name": program,
                        "academic_year": year,
                    }
                )
            )

            unique_sections.add(
                frozendict.frozendict(
                    {
                        "section_name": row["Section"],
                        "semester_name": semester,
                        "branch_name": branch,
                        "program_name": program,
                        "academic_year": year,
                    }
                )
            )

            for slot in time_slots:
                data_arr = row[slot].split("/")
                subject = data_arr[1]

                if subject == "X":
                    continue

                room = data_arr[0]
                faculty = data_arr[2]
                start_time = slot.split("-")[0].strip()
                end_time = slot.split("-")[1].strip()
                schedules.append(
                    {
                        "section": row["Section"],
                        "semester": semester,
                        "day": day_from_abbr(row["DAY"], capitalize=True),
                        "branch": branch,
                        "program": program,
                        "academic_year": year,
                        "subject": subject,
                        "start_time": start_time,
                        "end_time": end_time,
                        "classroom": room,
                        "faculty_id": faculty,
                    }
                )

        # Convert sets of frozendict to list of dict
        programs = unique_program
        branches = [dict(b) for b in unique_branch]
        semesters = [dict(s) for s in unique_semester]
        sections = [dict(s) for s in unique_sections]

        with open("./gen-sql/migration.sql", mode="w") as migration_file:
            SQLGenerator.sql_append_academic_years(
                year=unique_year,
                file_handle=migration_file,
                clear_all=clear_all,
            )
            # sql_append_faculty(migration_file)
            SQLGenerator.sql_append_programs(
                programs=programs,
                authority="kiit.ac.in",
                file_handle=migration_file,
                clear_all=clear_all,
            )
            SQLGenerator.sql_append_branches(
                branches=branches,
                authority="kiit.ac.in",
                file_handle=migration_file,
                clear_all=clear_all,
            )
            SQLGenerator.sql_append_semesters(
                semesters=semesters,
                authority="kiit.ac.in",
                file_handle=migration_file,
                clear_all=clear_all,
            )
            SQLGenerator.sql_append_sections(
                sections=sections,
                authority="kiit.ac.in",
                file_handle=migration_file,
                clear_all=clear_all,
            )
            SQLGenerator.sql_append_student_schedule(
                schedules=schedules,
                authority="kiit.ac.in",
                file_handle=migration_file,
                clear_all=clear_all,
            )
            migration_file.close()

        print("Shit's done!")


csv_file_path = "./gen-sql/sample-schedule-2.csv"
generate_sql_migration(csv_file_path)
