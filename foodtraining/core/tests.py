from django.test import TestCase
from .models import Trainer, Program, Lecture, Workout

# test if trainer saves properly
class TrainerModelTest(TestCase):
    def test_create_trainer(self):
        trainer = Trainer.objects.create(
            name="John Doe",
            specialty_field="Fitness",
            email="john@example.com",
            experience_year=5,
            gender="Male"
        )
        self.assertEqual(trainer.name, "John Doe")

# test if program saves with a trainer
class ProgramModelTest(TestCase):
    def test_create_program(self):
        trainer = Trainer.objects.create(
            name="Alice",
            specialty_field="Cardio",
            email="alice@example.com",
            experience_year=3,
            gender="Female"
        )
        program = Program.objects.create(
            title="Weight Loss",
            description="A full-body fat burning program.",
            duration=6,
            trainer=trainer
        )
        self.assertEqual(program.title, "Weight Loss")

# test lecture works and links to program
class LectureModelTest(TestCase):
    def test_create_lecture(self):
        trainer = Trainer.objects.create(
            name="Mark",
            specialty_field="Nutrition",
            email="mark@example.com",
            experience_year=4,
            gender="Male"
        )
        program = Program.objects.create(
            title="Nutrition 101",
            description="Basics of healthy eating.",
            duration=4,
            trainer=trainer
        )
        lecture = Lecture.objects.create(
            program=program,
            title="Macros Explained",
            description="Proteins, carbs, fats.",
            video_url="http://example.com/video"
        )
        self.assertEqual(lecture.program.title, "Nutrition 101")

# test workout can be created
class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(
            title="HIIT Blast",
            description="High Intensity Interval Training",
            difficulty="Hard",
            duration=30
        )
        self.assertEqual(workout.title, "HIIT Blast")

# test lecture links to correct program
class LectureLinkTest(TestCase):
    def test_lecture_program_link(self):
        trainer = Trainer.objects.create(
            name="Sarah",
            specialty_field="Strength",
            email="sarah@example.com",
            experience_year=6,
            gender="Female"
        )
        program = Program.objects.create(
            title="Strength 101",
            description="Build muscle strength.",
            duration=8,
            trainer=trainer
        )
        lecture = Lecture.objects.create(
            program=program,
            title="Deadlift Basics",
            description="Proper form and technique.",
            video_url="http://example.com/deadlift"
        )
        self.assertEqual(lecture.program.title, "Strength 101")

# test another workout works
class WorkoutCreateTest(TestCase):
    def test_second_workout(self):
        workout = Workout.objects.create(
            title="Yoga Flow",
            description="Relaxing full-body routine",
            difficulty="Easy",
            duration=45
        )
        self.assertEqual(workout.difficulty, "Easy")

# test trainer with basic info works
class MinimalTrainerTest(TestCase):
    def test_trainer_minimum(self):
        trainer = Trainer.objects.create(
            name="Leo",
            specialty_field="Yoga",
            email="leo@example.com",
            experience_year=1,
            gender="Non-binary"
        )
        self.assertTrue(trainer.email.endswith("@example.com"))

# test program duration is more than 0
class ProgramValidationTest(TestCase):
    def test_program_duration_positive(self):
        trainer = Trainer.objects.create(
            name="Lina",
            specialty_field="CrossFit",
            email="lina@example.com",
            experience_year=2,
            gender="Female"
        )
        program = Program.objects.create(
            title="Cross Training",
            description="Endurance and strength blend",
            duration=10,
            trainer=trainer
        )
        self.assertGreater(program.duration, 0)
