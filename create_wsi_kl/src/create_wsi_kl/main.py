#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from create_wsi_kl.crew import CreateWsiKl

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the WSI Cancer Description Multi-Agent System.
    """
    # Require cancer_type and pdf_file arguments
    if len(sys.argv) < 3:
        print("Usage: python main.py <cancer_type> <pdf_file>")
        sys.exit(1)

    cancer_type = sys.argv[1]
    pdf_file = sys.argv[2]

    inputs = {
        "cancer_type": cancer_type,
        "pdf_file": pdf_file,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    print(f"Starting WSI Cancer Description Analysis for: {cancer_type}")
    print(f"Using PDF file: {pdf_file}")
    print(f"Analysis Date: {inputs['analysis_date']}")
    print("-" * 50)

    try:
        result = CreateWsiKl(pdf_file=pdf_file).crew().kickoff(inputs=inputs)
        print(f"\nWSI Cancer Description completed successfully!")
        print(f"Output saved to: wsi_cancer_description.md")
        return result
    except Exception as e:
        raise Exception(
            f"An error occurred while running the WSI cancer description system: {e}"
        )


def train():
    """
    Train the WSI Cancer Description crew for a given number of iterations.
    """
    if len(sys.argv) < 5:
        print(
            "Usage: python main.py train <n_iterations> <training_file> <cancer_type> <pdf_file>"
        )
        sys.exit(1)

    cancer_type = sys.argv[3]
    pdf_file = sys.argv[4]

    inputs = {
        "cancer_type": cancer_type,
        "pdf_file": pdf_file,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    try:
        CreateWsiKl(pdf_file=pdf_file).crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
        print(f"Training completed for {cancer_type} cancer descriptions")
    except Exception as e:
        raise Exception(
            f"An error occurred while training the WSI cancer description crew: {e}"
        )


def replay():
    """
    Replay the WSI Cancer Description crew execution from a specific task.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py replay <task_id>")
        sys.exit(1)

    try:
        CreateWsiKl().crew().replay(task_id=sys.argv[1])
        print("Replay completed successfully")
    except Exception as e:
        raise Exception(
            f"An error occurred while replaying the WSI cancer description crew: {e}"
        )


def test():
    """
    Test the WSI Cancer Description crew execution and returns the results.
    """
    if len(sys.argv) < 5:
        print("Usage: python main.py test <n_iterations> <eval_llm> <cancer_type> <pdf_file>")
        sys.exit(1)

    cancer_type = sys.argv[3]
    pdf_file = sys.argv[4]

    inputs = {
        "cancer_type": cancer_type,
        "pdf_file": pdf_file,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    try:
        result = (
            CreateWsiKl(pdf_file=pdf_file)
            .crew()
            .test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        )
        print(f"Testing completed for {cancer_type} cancer descriptions")
        return result
    except Exception as e:
        raise Exception(
            f"An error occurred while testing the WSI cancer description crew: {e}"
        )


if __name__ == "__main__":
    # Check for minimum required arguments
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python main.py <cancer_type> <pdf_file>")
        print("  python main.py train <n_iterations> <training_file> <cancer_type> <pdf_file>")
        print("  python main.py test <n_iterations> <eval_llm> <cancer_type> <pdf_file>")
        print("  python main.py replay <task_id>")
        sys.exit(1)
    
    # Allow direct execution with different modes
    mode = sys.argv[1].lower()
    if mode == "train":
        train()
    elif mode == "replay":
        replay()
    elif mode == "test":
        test()
    else:
        # Treat the first two arguments as cancer_type and pdf_file
        run()
