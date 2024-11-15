#!/bin/bash
set -e  # Exit on any error

# Define constants
SPEC_URL="http://app:8877/api/openapi.json"
OUTPUT_DIR="core/corpora_client"
TEMP_DIR="gen/corpora_client"

echo "Step 1: Fetching OpenAPI spec from $SPEC_URL..."
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"
curl -o "$TEMP_DIR/openapi.json" "$SPEC_URL"

echo "Step 2: Generating Rust client library..."
npx @openapitools/openapi-generator-cli generate \
    -i "$TEMP_DIR/openapi.json" \
    -g rust \
    -o "$TEMP_DIR" \
    --additional-properties=packageName=corpora_client,library=hyper

echo "Step 3: Moving generated code to $OUTPUT_DIR..."
rm -rf "$OUTPUT_DIR/src" "$OUTPUT_DIR/Cargo.toml"
mkdir -p "$OUTPUT_DIR"
cp -r "$TEMP_DIR/src" "$OUTPUT_DIR"
cp "$TEMP_DIR/Cargo.toml" "$OUTPUT_DIR"

echo "Step 4: Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

echo "Step 5: Formatting the codebase..."
cargo fmt

echo "Step 6: Verifying the workspace..."
cargo build
cargo test

echo "Rust client generation complete!"
