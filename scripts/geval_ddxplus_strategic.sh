export OPENAI_API_KEY="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"

for i in {1..10}
do
    python ../geval.py \
        --input_path '../results/0102/multicritic-ddxplus-qwen-2-1.5b-qwen-2-1.5b-qwen-2-1.5b.json' \
        --prompt '../prompts/cds/strategic.txt' \
        --save_dir "../outputs/ddxplus-strategic/qwen215b/run_$i"
done