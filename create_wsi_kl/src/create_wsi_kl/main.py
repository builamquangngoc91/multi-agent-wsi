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
    # Default cancer type for testing - can be overridden via command line
    cancer_type = "Clear Cell Renal Cell Carcinoma (ccRCC)"

    # Check if cancer type is provided via command line
    if len(sys.argv) > 1:
        cancer_type = sys.argv[1]

    inputs = {
        "cancer_type": cancer_type,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    print(f"Starting WSI Cancer Description Analysis for: {cancer_type}")
    print(f"Analysis Date: {inputs['analysis_date']}")
    print("-" * 50)

    try:
        result = CreateWsiKl().crew().kickoff(inputs=inputs)
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
    if len(sys.argv) < 3:
        print(
            "Usage: python main.py train <n_iterations> <training_file> [cancer_type]"
        )
        sys.exit(1)

    cancer_type = "Clear Cell Renal Cell Carcinoma (ccRCC)"
    if len(sys.argv) > 3:
        cancer_type = sys.argv[3]

    inputs = {
        "cancer_type": cancer_type,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    try:
        CreateWsiKl().crew().train(
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
    if len(sys.argv) < 3:
        print("Usage: python main.py test <n_iterations> <eval_llm> [cancer_type]")
        sys.exit(1)

    cancer_type = "Clear Cell Renal Cell Carcinoma (ccRCC)"
    if len(sys.argv) > 3:
        cancer_type = sys.argv[3]

    inputs = {
        "cancer_type": cancer_type,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    try:
        result = (
            CreateWsiKl()
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
    # Allow direct execution with different modes
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "train":
            train()
        elif mode == "replay":
            replay()
        elif mode == "test":
            test()
        else:
            # Treat the first argument as cancer type
            run()
    else:
        run()
