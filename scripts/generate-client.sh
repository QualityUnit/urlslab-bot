#!/bin/bash

# Check if an argument was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <generator_name>"
    exit 1
fi

# Define constants
API_URL_DOC="http://localhost:9010/openapi.json"
CLIENTS_DIR="./client"
DEFAULT_CLIENT_VERSION="0.0.0"
GENERATOR_NAME="$1"

# Function to install OpenAPI Generator CLI
install_openapi_cli() {
    echo "Installing OpenAPI Generator CLI..."
    local install_path="$RUNNER_TEMP/openapi-generator-cli"
    mkdir -p "${install_path}"
    curl -sSL https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/bin/utils/openapi-generator-cli.sh > "${install_path}/openapi-generator-cli"
    chmod u+x "${install_path}/openapi-generator-cli"

    # Point to the local installation of openapi-generator
    export PATH="$PATH:${install_path}"
}

# Function to check if OpenAPI Generator is installed
check_openapi_generator() {
    if ! command -v openapi-generator &> /dev/null; then
        echo "openapi-generator could not be found"
        install_openapi_cli
        # Ensure that the newly installed binary can be found
#        if ! command -v openapi-generator &> /dev/null; then
#            echo "Failed to install openapi-generator. Please install it manually."
#            exit 1
#        fi
    else
        echo "openapi-generator is installed"
    fi
}
# Function to wait for the OpenAPI Documentation to be accessible
sleep_for_server() {
    for i in {0..9}; do
        echo "Trying to connect to server..."
        if curl -s "${API_URL_DOC}" &>/dev/null; then
            echo "Server is up!"
            break
        else
            echo "Waiting for server to start..."
            sleep 30
        fi
    done
}

# Generate clients in the specified directory
generate_clients() {
    case "${GENERATOR_NAME}" in
        "scala-akka")
            output_dir="${CLIENTS_DIR}/${GENERATOR_NAME}"
            mkdir -p "${output_dir}"
            openapi-generator generate \
                -i "${API_URL_DOC}" \
                --artifact-id urlslab-bot-scala \
                --api-package bot.urlslab \
                --git-repo-id urlslab-bot \
                --artifact-version "${CLIENT_VERSION}" \
                --group-id bot.urlslab \
                --additional-properties=modelPropertyNaming=original \
                -g scala-akka \
                -o "${output_dir}"
            ;;
        *)
            echo "Generator '${GENERATOR_NAME}' not supported."
            exit 1
            ;;
    esac
}

# Main script execution

# Check for CLIENT_VERSION environment variable, if not present use default
CLIENT_VERSION="${CLIENT_VERSION:-$DEFAULT_CLIENT_VERSION}"

# If necessary install the OpenAPI Generator CLI tool
check_openapi_generator

# Wait for server to be up (optional)
sleep_for_server

# Create clients directory and clean previous clients
rm -rf "${CLIENTS_DIR}"
mkdir -p "${CLIENTS_DIR}"

# Generate the clients based on the specified generator
generate_clients