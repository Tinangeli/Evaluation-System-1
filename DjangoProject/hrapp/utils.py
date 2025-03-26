import pandas as pd
from transformers import pipeline
from collections import Counter
from .models import Evaluations  # Import the Evaluations model
import json  # For decoding JSON fields


# Load evaluations from the database
def load_evaluations():
    try:
        # Fetch all Evaluations
        evaluations = Evaluations.objects.all()
        if not evaluations.exists():
            raise ValueError("No evaluations found in the database.")

        # Create lists to store student and instructor activities
        student_activities = []
        instructor_activities = []

        # Process each evaluation
        for evaluation in evaluations:
            # Access the JSON data directly since JSONField returns a dict
            student_data = evaluation.student_activities or {}  # Default to an empty dict if None
            instructor_data = evaluation.instructor_activities or {}  # Default to an empty dict if None

            # Extend the activities list with values from each time slot
            for activities in student_data.values():
                student_activities.extend(activities)

            for activities in instructor_data.values():
                instructor_activities.extend(activities)

        # Use Counter to calculate occurrences of each activity
        return {
            "student_activities": dict(Counter(student_activities)),  # Count occurrences of each activity
            "instructor_activities": dict(Counter(instructor_activities)),  # Count occurrences of each activity
        }
    except Exception as e:
        raise Exception(f"Error loading evaluations: {e}")



# Load feedback from CSV file
def load_feedback(csv_path):
    try:
        df = pd.read_csv(csv_path)
        feedback_dict = {}
        for _, row in df.iterrows():
            category = row['Category']
            pos_feedback = row['Positive Feedback']
            neg_feedback = row['Negative Feedback']
            feedback_dict[category] = {
                "positive": pos_feedback,
                "negative": neg_feedback
            }
        return feedback_dict
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{csv_path}' not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty.")
    except Exception as e:
        raise Exception(f"Error reading CSV: {e}")


# Format actions dynamically
def format_actions(actions_dict, feedback_dict, title):
    formatted_text = f"### {title} ###\n"
    for action, count in actions_dict.items():
        feedback = feedback_dict.get(action, {"positive": "N/A", "negative": "N/A"})
        formatted_text += (f"- {action}: {count} times\n"
                           f"  * Positive: {feedback['positive']}\n"
                           f"  * Negative: {feedback['negative']}\n")
    return formatted_text + "\n"


# Generate the AI summary
def generate_prompt_and_summary(evaluations_data, feedback_csv_path):
    # Load feedback data
    feedback_data = load_feedback(feedback_csv_path)

    # Construct prompt efficiently
    prompt = (
            "Classroom Observation Report:\n\n" +
            format_actions(evaluations_data["student_activities"], feedback_data, "Student Actions Summary") +
            format_actions(evaluations_data["instructor_activities"], feedback_data, "Instructor Actions Summary") +
            "### Detailed Analysis Request ###\n"
            "Please analyze the collected classroom data and provide a thorough summary with insights into the following aspects:\n"
            "1. **Engagement Levels:** Identify how actively students participated and which activities dominated their time.\n"
            "2. **Instructor-Student Interaction:** Assess how balanced the instructor's engagement was compared to student participation.\n"
            "3. **Most and Least Frequent Activities:** Highlight the key trends in classroom dynamics by identifying the highest and lowest recorded actions.\n"
            "4. **Passive vs. Active Learning:** Determine whether students were mostly passive (listening, waiting) or active (discussing, presenting).\n"
            "5. **Teaching Methods Effectiveness:** Evaluate how different teaching actions influenced student engagement and participation.\n"
            "6. **Feedback-Based Improvements:** Suggest actionable recommendations based on both statistical insights and qualitative feedback.\n")

    # Load summarization model
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        raise Exception(f"Error loading model: {e}")

    # Generate summary
    summary_result = summarizer(prompt, max_length=250, min_length=100, do_sample=False)[0]['summary_text']
    return summary_result
