import os
from datetime import datetime
from utils.Validators import is_valid_domain

def generate_html_report(entity: str, results: dict, output_dir: str = "reports") -> str:
    # Create the reports directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate a timestamped filename based on the entity
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{entity.replace('.', '_')}_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)

    # Start building the HTML content with basic styles
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

    # Iterate through each intelligence section (e.g., WHOIS, Geolocation, etc.)
    for section, data in results.items():
        html_content += f'<div class="section"><h3>{section}</h3>'

        if isinstance(data, dict):
            # For nested data, display each key-value pair
            for sub_key, sub_value in data.items():
                html_content += f'<h4>{sub_key}</h4>'
                if isinstance(sub_value, list):
                    # Display list values (e.g. subdomains) in <pre> block
                    html_content += "<pre>" + "\n".join(sub_value) + "</pre>"
                else:
                    html_content += f"<pre>{sub_value}</pre>"
        else:
            # Display simple values (string, number, etc.)
            html_content += f"<pre>{data}</pre>"

        html_content += '</div>'

    # Embed Wayback Machine iframe only if the entity is a valid domain
    if is_valid_domain(entity):
        clean_entity = entity.strip().lower()
        html_content += f"""
        <div class="section">
            <h3>Wayback Machine Snapshot</h3>
            <iframe 
                src="https://web.archive.org/web/*/{clean_entity}"
                width="100%" height="500px" 
                style="border:1px solid #ccc">
            </iframe>
            <p><small>View historical versions of this site using the Wayback Machine.</small></p>
        </div>
        """

    # Finalize the HTML
    html_content += "</body></html>"

    # Write the report to a file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Return the full path to the generated report
    return filepath