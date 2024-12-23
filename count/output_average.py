import os
import json
import argparse

def calculate_average_from_folders(folder, output_file):
    folder_path = os.path.join("/home/intern/mjgwak/medical_reasoning/outputs/", folder)

    # Validate folder existence
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

    total_prediction = 0
    count = 0

    # Process files named numerically from 0.json to 299.json
    for i in range(300):  # Range is exclusive, covers 0 to 299
        filename = f"{i}.json"
        file_path = os.path.join(folder_path, filename)
        
        if not os.path.exists(file_path):
            continue  # Skip missing files silently

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                prediction_str = data.get("prediction", "")
                
                if "PREDICTION: " in prediction_str:
                    # Extract and convert the prediction value
                    prediction_value = float(prediction_str.split("PREDICTION: ")[1].strip())
                    total_prediction += prediction_value
                    count += 1
                else:
                    print(f"Warning: 'PREDICTION: ' not found in file {filename}")
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                print(f"Warning: Error processing file {filename}: {e}")

    # Calculate the average prediction
    average_prediction = total_prediction / count if count > 0 else 0

    # Save the average to the output JSON file
    averages = {"average_prediction": average_prediction}
    with open(output_file, 'w') as outfile:
        json.dump(averages, outfile, indent=4)

    print(f"Average prediction calculated: {average_prediction:.4f}")
    print(f"Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Calculate and save the averages from JSON files")
    parser.add_argument("folder", type=str, help="Name of the folder containing JSON files")
    parser.add_argument("output_file", type=str, help="Name of the output JSON file")
    
    args = parser.parse_args()
    
    calculate_average_from_folders(args.folder, args.output_file)

if __name__ == '__main__':
    main()
