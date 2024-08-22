##################################################################################################
##                                                                                              ##
##  This Auxilary python code does search cross-origin resource sharing (CORS) misconfigration  ##
##     Author: Mahmut AY < mahmutayy@yahoo.com >                                                ##
##                                                                                              ##
##              USAGE:  CORS_inspector.py  <url>                                                ##  
##                                                                                              ##
##                This is only educational purpose usage                                        ##
##       !!  Do not attempt to violate the laws with anything contained here. !!!               ##
##                                                                                              ##
##                                                                                              ##
##################################################################################################

import sys
import webbrowser
import os


if len(sys.argv) != 2:
    print("Usage: python script.py <url>")
    sys.exit(1)


url = sys.argv[1]

# HTML template with the URL injected
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XHR Example</title>
</head>
<body>
    <h1>This aux script is only for educational Usage or business needs written by  Mahmut AY</h1>
    <h1> This does a CORS Investigation for  security misconfiguration vulnerability</h1>
    <h1>XHR Request to : " {url}"</h1>
    <button id="sendRequest">Send XHR Request</button>

    <script>
        document.getElementById("sendRequest").addEventListener("click", function() {{
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "{url}", true);

            xhr.onreadystatechange = function() {{
                if (xhr.readyState === XMLHttpRequest.DONE) {{
                    if (xhr.status === 200) {{
                        console.log("Response received: ", xhr.responseText);
                        alert("Response received: " + xhr.responseText);
                    }} else {{
                        console.log("Error: ", xhr.statusText);
                        alert("Error: " + xhr.statusText);
                    }}
                }}
            }};

            xhr.send();
        }});
    </script>
</body>
</html>
"""

# assigning the HTML file name
html_file = "{url}.corsInspect.html"

# Write the HTML content to the file
with open(html_file, "w") as file:
    file.write(html_template)

print(f"HTML file '{html_file}' has been generated.")

# Automatically open the generated HTML file in the default web browser ( it wil  be opened yoru default Browser )
webbrowser.open(f"file://{os.path.abspath(html_file)}")
