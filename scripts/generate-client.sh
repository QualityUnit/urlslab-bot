#!/bin/bash

# Check if an argument was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <generator_name>"
    exit 1
fi

# Define constants
API_URL_DOC="http://localhost:9010/openapi.json"
CLIENTS_DIR="client"
DEFAULT_CLIENT_VERSION="0.0.0"
GENERATOR_NAME="$1"
OPENAPI_CLI="openapi-generator-cli.jar"
GENERATOR_VERSION="6.3.0"

# Function to install OpenAPI Generator CLI
install_openapi_cli() {
    echo "Installing OpenAPI Generator CLI..."

    if [ -f "${OPENAPI_CLI}" ]; then
        echo "OpenAPI Generator CLI is already installed."
        return 0
    fi

    echo "Downloading OpenAPI Generator CLI version ${GENERATOR_VERSION}..."
    wget "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${GENERATOR_VERSION}/openapi-generator-cli-${GENERATOR_VERSION}.jar" -O "${OPENAPI_CLI}"
    if [ ! -f "${OPENAPI_CLI}" ]; then
        echo "Failed to download OpenAPI Generator CLI JAR. Please check the provided version."
        exit 1
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
            mkdir -p "${GENERATOR_NAME}"
            java -jar "${OPENAPI_CLI}" generate \
                -i "${API_URL_DOC}" \
                --artifact-id urlslab-bot-scala \
                --api-package bot.urlslab \
                --git-repo-id urlslab-bot \
                --artifact-version "${CLIENT_VERSION}" \
                --group-id bot.urlslab \
                --additional-properties=modelPropertyNaming=original \
                -g scala-akka \
                -o "${GENERATOR_NAME}"
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

# Create clients directory and clean previous clients
rm -rf "${CLIENTS_DIR}"
mkdir -p "${CLIENTS_DIR}"
cd "${CLIENTS_DIR}"

# If necessary install the OpenAPI Generator CLI tool
install_openapi_cli

# Wait for server to be up (optional)
sleep_for_server

# Generate the clients based on the specified generator
generate_clients