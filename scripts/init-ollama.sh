#!/bin/sh

set -e

export OLLAMA_HOST=http://ollama:11434

echo "=============================================="
echo "        Ollama Model Initializer"
echo "=============================================="

echo "Waiting for Ollama server..."

until curl -fs http://ollama:11434/api/tags >/dev/null 2>&1
do
    sleep 2
done

echo
echo "✓ Ollama server is online."
echo

MODELS="
nomic-embed-text
gemma3:4b
"

for MODEL in $MODELS
do
    echo "Checking model: $MODEL"

    INSTALLED=$(curl -s http://ollama:11434/api/tags \
        | jq -r '.models[].name' \
        | grep -Fx "$MODEL" || true)

    if [ "$INSTALLED" = "$MODEL" ]; then
        echo "✓ Already installed."
    else
        echo "Downloading $MODEL..."
        ollama pull "$MODEL"
        echo "✓ Download completed."
    fi

    echo
done

echo "=============================================="
echo "✓ All required models are ready."
echo "=============================================="