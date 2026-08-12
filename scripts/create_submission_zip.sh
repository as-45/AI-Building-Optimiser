#!/bin/bash
set -e

# Create a submission_package.zip containing the deliverables judges expect.
# Run from repository root:
#   bash scripts/create_submission_zip.sh

OUT=submission_package.zip
rm -f "$OUT"

# Files and dirs to include; adjust if some files are not present.
INCLUDE=(reports docs scripts extract_metrics.py validate_setup.py AI_Building_Optimizer_Report_Part1-merged.pdf "SIH_Idea_Presentation_Building_Energy_AI (2).pptx" README.md .gitignore)

echo "Creating $OUT with: ${INCLUDE[*]}"

# Use zip if available; fall back to tar.gz
if command -v zip >/dev/null 2>&1; then
  zip -r "$OUT" "${INCLUDE[@]}" || true
else
  tar -czf submission_package.tar.gz "${INCLUDE[@]}" || true
  echo "zip not found; created submission_package.tar.gz instead"
fi

echo "Done. Output: $OUT (or submission_package.tar.gz)"
