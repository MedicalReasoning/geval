prompts=("consistency.txt" "explainability.txt" "grounding.txt" "strategic.txt")

# 각 프롬프트에 대해 반복문 실행
for prompt in "${prompts[@]}"
do
    prompt_name="${prompt%.*}"
    for i in {1..3}
    do
        python ./geval.py \
            --input_path './results/0102/multicritic-ddxplus-qwen-2-1.5b-qwen-2-1.5b-qwen-2-1.5b.json' \
            --prompt "./prompts/with_label/cds/$prompt" \
            --use_label \
            --save_dir "./results/ddxplus-$prompt_name/qwen215b/run_$i"
    done
done
