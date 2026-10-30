#!/bin/bash
# Generate sample system activity for testing

echo "Generating sample system activity..."

logger -t compliance-test "Sample security event: User authentication"
logger -t compliance-test "Sample system event: Service started"
logger -t compliance-test "Sample access event: File accessed"

mkdir -p ../output
cat > ../output/sample_config.txt << EOF
Sample System Configuration
Generated: $(date)
Hostname: $(hostname)
Kernel: $(uname -r)
