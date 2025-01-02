export OPENAI_API_KEY="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"

for i in {1..10}
do
    python ./geval.py \
        --input_path './results/0102/claude/multicritic-ddxplus-claude-3.5-sonnet-claude-3.5-sonnet-claude-3.5-sonnet.json' \
        --prompt './prompts/kqa/consistency.txt' \
        --save_dir "./outputs/medqa-consistency/run_$i"
done