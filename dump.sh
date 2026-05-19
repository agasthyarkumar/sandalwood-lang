#!/bin/bash

# ============================================

# Sandalwood Project Snapshot Generator

# ============================================

OUTPUT_FILE="project_dump.txt"

# Clear previous output

> "$OUTPUT_FILE"

echo "Generating project dump..."

# Directories to ignore

IGNORE_DIRS=(
".git"
"**pycache**"
".venv"
"venv"
"node_modules"
".idea"
".vscode"
)

# Files to ignore

IGNORE_FILES=(
"$OUTPUT_FILE"
)

# Function to check ignored directories

should_ignore_dir() {
local dir="$1"

```
for ignored in "${IGNORE_DIRS[@]}"; do
    if [[ "$dir" == *"/$ignored"* ]]; then
        return 0
    fi
done

return 1
```

}

# Function to check ignored files

should_ignore_file() {
local file="$1"

```
for ignored in "${IGNORE_FILES[@]}"; do
    if [[ "$(basename "$file")" == "$ignored" ]]; then
        return 0
    fi
done

return 1
```

}

# Recursive traversal

find . -type f | while read -r file; do

```
# Skip ignored directories
if should_ignore_dir "$file"; then
    continue
fi

# Skip ignored files
if should_ignore_file "$file"; then
    continue
fi

echo "==========================================" >> "$OUTPUT_FILE"
echo "PWD: $(dirname "$(realpath "$file")")" >> "$OUTPUT_FILE"
echo "FILE: $(basename "$file")" >> "$OUTPUT_FILE"
echo "PATH: $(realpath "$file")" >> "$OUTPUT_FILE"
echo "==========================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

cat "$file" >> "$OUTPUT_FILE" 2>/dev/null

echo "" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
```

done

echo "Project dump saved to $OUTPUT_FILE"
