#!/bin/bash
echo "🔍 Checking your project..."
echo "Files with @app.callback:"
find . -name "*.py" -exec grep -l "@app.callback" {} \;
echo ""
echo "Checking main files:"
ls -la app.py ui/pages/main_page.py ui/components/ 2>/dev/null
