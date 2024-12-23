import os
import json
import argparse
import copy

def calculate_average_from_folders(base_folder, output_file, prefix):
    base_folder = os.path.join("/home/intern/mjgwak/medical_reasoning/outputs_filter/", base_folder)
    
    # Get all folders starting with the specified prefix
    folders = [f for f in os.listdir(base_folder) if f.startswith(prefix) and os.path.isdir(os.path.join(base_folder, f))]
    
    # Initialize a dictionary to store cumulative predictions and counts for each file
    cumulative_predictions = {}
    
    for folder in folders:
        folder_path = os.path.join(base_folder, folder)
        
        # Use the filename directly as the key
        files = {f: f for f in os.listdir(folder_path) if f.endswith('.json')}
        
        # Debug: Print the number of files found in each folder
        print(f"Processing folder: {folder}, Number of files: {len(files)}")
        
        for key, filename in files.items():
            with open(os.path.join(folder_path, filename), 'r') as file:
                data = json.load(file)
                if data["label"] != data["output"]["iteration"][0]["refiner_prediction"] and data["label"]:
                #!= data["output"]["initial_prediction"]:  # Check if label equals initial_prediction
                    prediction_str = data["prediction"]
                    if "PREDICTION:" in prediction_str:
                        try:
                            prediction_value = float(prediction_str.split()[1].strip())
                            if key not in cumulative_predictions:
                                cumulative_predictions[key] = {'total': 0, 'count': 0, 'data': None}
                                cumulative_predictions[key]['data'] = {'predictions': []}
                            cumulative_predictions[key]['total'] += prediction_value
                            cumulative_predictions[key]['count'] += 1
                            if folder == folders[0]:  # Deepcopy data from the first folder
                                cumulative_predictions[key]['data'] = copy.deepcopy(data)
                                if "predictions" not in cumulative_predictions[key]['data']:
                                    cumulative_predictions[key]['data']["predictions"] = []
                            folder_name_parts = folder.split('_')  # Split the folder name by underscores
                            second_word = folder_name_parts[1] if len(folder_name_parts) > 1 else ''  # Get the second word
                            cumulative_predictions[key]['data']["predictions"].append(f"\n\n<b>Evaluation Criteria: {second_word.upper()}</b>\n\n {data['prediction']}")
                        except ValueError:
                            print(f"Warning: Could not convert prediction to float in file {filename}")
    
    # Debug: Print the number of unique keys in cumulative_predictions
    print(f"Number of unique keys in cumulative_predictions: {len(cumulative_predictions)}")
    
    # Calculate averages and prepare data
    all_averages = []
    for key, values in cumulative_predictions.items():
        if values['count'] > 0:
            average_prediction = values['total'] / values['count']
        else:
            average_prediction = 0
        all_averages.append((average_prediction, values['data']))
        
    # Sort by average prediction and get top-10
    
    top_10_averages = [entry for entry in all_averages if len(entry[1]['predictions']) == 5]
    
    top_10_averages = sorted(top_10_averages, key=lambda x: x[0], reverse=True)[:12]
        
    #Sort by average prediction and get bottom-10
    #bottom_10_averages = sorted(all_averages, key=lambda x: x[0])[:10]
    
    # Prepare output data and save each as a separate JSON file
    for index, (avg, data) in enumerate(top_10_averages):
        output_data = {
            'average': avg,
            'data': data
        }
        output_filename = f"{output_file}_top_{index+1}.json"
        with open(output_filename, 'w') as outfile:
            json.dump(output_data, outfile, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Calculate and save the averages from JSON files")
    parser.add_argument("base_folder", type=str, help="Base folder containing subfolders")
    parser.add_argument("output_file", type=str, help="Name of the output JSON file")
    parser.add_argument("prefix", type=str, help="Prefix to filter folders")
    
    args = parser.parse_args()
    
    calculate_average_from_folders(args.base_folder, args.output_file, args.prefix)

if __name__ == '__main__':
    main()