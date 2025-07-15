#!/usr/bin/env python
import sys
import warnings
import json
import os

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
    import argparse
    
    parser = argparse.ArgumentParser(description="WSI Cancer Description Analysis")
    parser.add_argument("cancer_type", nargs="?", default="No Tumor (Negative Lymph Nodes)", 
                       help="Cancer type to analyze")
    parser.add_argument("--json-source", type=str, 
                       help="Path to JSON file containing cancer descriptions")
    
    args = parser.parse_args()
    
    cancer_type = args.cancer_type
    use_json_source = args.json_source is not None

    inputs = {
        "cancer_type": cancer_type,
        "current_year": str(datetime.now().year),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    }

    print(f"Starting WSI Cancer Description Analysis for: {cancer_type}")
    print(f"Analysis Date: {inputs['analysis_date']}")
    print(f"Data Source: {'JSON file' if use_json_source else 'PDF files'}")
    if use_json_source:
        print(f"JSON Source: {args.json_source}")
    print("-" * 50)

    try:
        crew_instance = CreateWsiKl(
            use_json_source=use_json_source,
            json_file_path=args.json_source
        )
        result = crew_instance.crew().kickoff(inputs=inputs)
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


def validate():
    """
    Validate and select descriptions from cancer_descriptions.json file.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py validate [cancer_type]")
        print("If no cancer_type is specified, all cancer types in cancer_descriptions.json will be validated")
        sys.exit(1)

    # Path to cancer descriptions file
    cancer_descriptions_path = os.path.join("knowledge", "cancer_descriptions.json")
    
    if not os.path.exists(cancer_descriptions_path):
        print(f"Error: {cancer_descriptions_path} not found")
        sys.exit(1)

    # Load existing cancer descriptions
    try:
        with open(cancer_descriptions_path, 'r') as f:
            existing_descriptions = json.load(f)
    except Exception as e:
        print(f"Error loading {cancer_descriptions_path}: {e}")
        sys.exit(1)

    # Determine which cancer types to validate
    if len(sys.argv) > 2:
        # Validate specific cancer type
        cancer_type = sys.argv[2]
        if cancer_type not in existing_descriptions:
            print(f"Error: Cancer type '{cancer_type}' not found in {cancer_descriptions_path}")
            print(f"Available cancer types: {list(existing_descriptions.keys())}")
            sys.exit(1)
        cancer_types_to_validate = [cancer_type]
    else:
        # Validate all cancer types
        cancer_types_to_validate = list(existing_descriptions.keys())

    print(f"Validating and selecting descriptions for {len(cancer_types_to_validate)} cancer type(s)")
    print("-" * 50)

    validated_results = {}
    
    for cancer_type in cancer_types_to_validate:
        print(f"\nProcessing: {cancer_type}")
        
        # Get existing descriptions for this cancer type
        descriptions = existing_descriptions[cancer_type]
        
        try:
            # Validate and select best descriptions
            selected_descriptions = _validate_and_select_descriptions(cancer_type, descriptions)
            validated_results[cancer_type] = selected_descriptions
            
            print(f"✓ Selected {len(selected_descriptions)} descriptions for {cancer_type}")
            
        except Exception as e:
            print(f"✗ Validation failed for {cancer_type}: {e}")
            validated_results[cancer_type] = descriptions  # Keep original if validation fails

    # Save validated results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"validated_descriptions_{timestamp}.json"
    
    try:
        with open(results_file, 'w') as f:
            json.dump(validated_results, f, indent=2)
        print(f"\nValidated results saved to: {results_file}")
    except Exception as e:
        print(f"Error saving validated results: {e}")

    # Print summary
    total_original = sum(len(existing_descriptions[ct]) for ct in cancer_types_to_validate)
    total_selected = sum(len(validated_results[ct]) for ct in cancer_types_to_validate)
    
    print(f"\nValidation Summary:")
    print(f"  Original descriptions: {total_original}")
    print(f"  Selected descriptions: {total_selected}")
    print(f"  Cancer types processed: {len(cancer_types_to_validate)}")

    return validated_results


def _compare_descriptions(cancer_type, existing_descriptions, new_descriptions):
    """
    Compare existing descriptions with newly generated ones and provide validation analysis.
    """
    return {
        "status": "success",
        "cancer_type": cancer_type,
        "existing_descriptions": existing_descriptions,
        "new_descriptions": new_descriptions,
        "comparison": {
            "existing_count": len(existing_descriptions),
            "new_count": len(new_descriptions),
            "overlapping_content": _find_overlapping_content(existing_descriptions, new_descriptions),
            "unique_to_existing": _find_unique_content(existing_descriptions, new_descriptions),
            "unique_to_new": _find_unique_content(new_descriptions, existing_descriptions),
            "quality_assessment": _assess_quality_differences(existing_descriptions, new_descriptions)
        },
        "validation_notes": _generate_validation_notes(existing_descriptions, new_descriptions)
    }


def _find_overlapping_content(list1, list2):
    """Find content that appears in both description lists."""
    overlaps = []
    for desc1 in list1:
        for desc2 in list2:
            # Simple similarity check - could be enhanced with more sophisticated NLP
            if _descriptions_similar(desc1, desc2):
                overlaps.append({"existing": desc1, "new": desc2})
    return overlaps


def _find_unique_content(source_list, comparison_list):
    """Find content that appears only in the source list."""
    unique = []
    for desc in source_list:
        if not any(_descriptions_similar(desc, comp_desc) for comp_desc in comparison_list):
            unique.append(desc)
    return unique


def _descriptions_similar(desc1, desc2, threshold=0.6):
    """Simple similarity check between two descriptions."""
    # Convert to lowercase and split into words
    words1 = set(desc1.lower().split())
    words2 = set(desc2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return (intersection / union) if union > 0 else 0 >= threshold


def _assess_quality_differences(existing_descriptions, new_descriptions):
    """Assess quality differences between existing and new descriptions."""
    return {
        "avg_length_existing": sum(len(d.split()) for d in existing_descriptions) / len(existing_descriptions) if existing_descriptions else 0,
        "avg_length_new": sum(len(d.split()) for d in new_descriptions) / len(new_descriptions) if new_descriptions else 0,
        "technical_terms_existing": sum(1 for d in existing_descriptions if any(term in d.lower() for term in ["tumor", "carcinoma", "neoplasm", "malignant", "morphology"])),
        "technical_terms_new": sum(1 for d in new_descriptions if any(term in d.lower() for term in ["tumor", "carcinoma", "neoplasm", "malignant", "morphology"]))
    }


def _generate_validation_notes(existing_descriptions, new_descriptions):
    """Generate validation notes comparing the description sets."""
    notes = []
    
    if len(new_descriptions) > len(existing_descriptions):
        notes.append(f"New descriptions are more comprehensive ({len(new_descriptions)} vs {len(existing_descriptions)} descriptions)")
    elif len(new_descriptions) < len(existing_descriptions):
        notes.append(f"Existing descriptions are more comprehensive ({len(existing_descriptions)} vs {len(new_descriptions)} descriptions)")
    else:
        notes.append(f"Both sets have equal number of descriptions ({len(existing_descriptions)})")
    
    # Check for medical terminology usage
    existing_medical_terms = sum(1 for d in existing_descriptions if any(term in d.lower() for term in ["histologic", "pathologic", "microscopic", "immunohistochemical"]))
    new_medical_terms = sum(1 for d in new_descriptions if any(term in d.lower() for term in ["histologic", "pathologic", "microscopic", "immunohistochemical"]))
    
    if new_medical_terms > existing_medical_terms:
        notes.append("New descriptions use more advanced medical terminology")
    elif existing_medical_terms > new_medical_terms:
        notes.append("Existing descriptions use more advanced medical terminology")
    
    return notes


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
