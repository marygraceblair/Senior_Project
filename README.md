Food Waste WebApp
An app designed to help you prevent food waste. This app will help you monitor and manage your pantry more 
efficiently, which will enable you to make smarter and more environmentally friendly choices at the Grocery Store.


Features:
    - Scan receipts after grocery store trips to update your pantry
    - Edit prices and quantity of scanned-in items
    - Delete items from your pantry/scanned receipts
    - Take weekly consumption surveys
    - Display results from weekly consumption surveys in graphs 

Graphs:
    The app currently can produce graphs that show total money wasted (percent) per scanned receipt. I am hoping to 
    add more usage graphs in the future. 

Note: The app currently only works with Dillons receipts. The project is also still in the early development phases. 
It is still very buggy and could use a lot more work. 

Requirements:
For this webapp, you will need Pytesseract installed on your local machine.
If you are using a mac, I highly suggest that you download it with homebrew. 

You will also need python3 and django for python3. 

Running the Program:
To run the server, run "python3 manage.py runserver"

To show the Graphs:
    Note: This will only work if you have scanned receipts with at least one usage survey completed
    - redirect to the url 'http://127.0.0.1:8000/charts/simple.png'
    
