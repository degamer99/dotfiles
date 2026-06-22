# Ensure the submodule is downloaded and updated
git submodule update --init --recursive

# Run the Dotbot Python script
python dotbot\bin\dotbot -d $PSScriptRoot -c install.conf.yaml
