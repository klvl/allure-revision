FROM python:3.9-slim-buster

# Install required packages
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the project
RUN git clone https://github.com/klvl/allure-revision.git

# Set the working directory to the project directory
WORKDIR /allure-revision

# Install project dependencies
RUN pip3 install -r requirements.txt

# Run revision
CMD python3 main/make.py \
    --id=$ID \
    --token=$TOKEN \
    --report_path=$REPORT_PATH \
    --sheet_name=$SHEET_NAME \
    --sheet_index=$SHEET_INDEX \
    --config_path=$CONFIG_PATH