from src.scrape import fetch_questions


def update_question_database(event, context):
    try:
        fetch_questions()
    except Exception as e:
        print(f"Test - {str(e)}")
