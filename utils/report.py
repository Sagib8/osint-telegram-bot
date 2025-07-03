import os
from datetime import datetime

def generate_html_report(entity: str, results: dict, output_dir: str = "reports") -> str:
    # Create the reports directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique filename using the entity and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{entity.replace('.', '_')}_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    # Start building the HTML content with basic styling
    html_content = f"""
    <html>
    <head>
        <title>Intelligence Report - {entity}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                color: #003366;
            }}
            h2 {{
                color: #005599;
                border-bottom: 1px solid #ccc;
                padding-bottom: 4px;
            }}
            h3 {{
                color: #333;
                margin-top: 30px;
            }}
            h4 {{
                color: #006699;
                margin-top: 15px;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border: 1px solid #ccc;
                overflow-x: auto;
            }}
            .section {{
                padding: 10px 20px;
                margin-bottom: 30px;
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}
        </style>
    </head>
    <body>
        <h1>OSINT Analysis Report</h1>
        <h2>Target: {entity}</h2>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <hr>
    """

    # Iterate through each section in the results dictionary
    for section, data in results.items():
        html_content += f'<div class="section"><h3>{section}</h3>'

        # If the section is a nested dictionary (e.g. VirusTotal)
        if isinstance(data, dict):
            for sub_key, sub_value in data.items():
                html_content += f'<h4>{sub_key}</h4>'
                
                # Handle list values (e.g. subdomains list)
                if isinstance(sub_value, list):
                    html_content += "<pre>" + "\n".join(sub_value) + "</pre>"
                else:
                    html_content += f"<pre>{sub_value}</pre>"
        else:
            # For simple string/int/float values
            html_content += f"<pre>{data}</pre>"

        html_content += '</div>'

    # Close the HTML document
    html_content += "</body></html>"

    # Write the HTML to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Return the path to the generated report
    return filepath