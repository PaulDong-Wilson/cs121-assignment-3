from flask import Flask, flash, render_template, request
from search_query import find_search_query
from stopwatch import Stopwatch

# To hold the file location for document IDs
document_id_file = "document_ids.txt"


# Web UI setup adapted from:
# https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
# https://www.tutorialspoint.com/flask/flask_quick_guide.htm
def create_app(test_config=None):
    # Create the Flask object for the application
    app = Flask(__name__)

    # Needed for flashing messages to the Flask server, is otherwise unused
    # Given value of "LOCAL KEY" is arbitrary
    app.secret_key = "LOCAL KEY"

    # To hold the document ID lookups for the index
    document_id_lookups = {}

    # Load in the document ID associations for the index
    with open(document_id_file, 'r') as document_id_file_stream:
        for next_line in document_id_file_stream:
            next_id, next_url = next_line.rstrip().split("; ")
            document_id_lookups[next_id] = next_url

    # Define the routine that runs when the webserver is accessed at http://127.0.0.1:5000/
    @app.route('/', methods=['GET', 'POST'])
    def query_screen():
        # If a POST request is sent from the page, the user entered a query
        if request.method == 'POST':
            # Create a watch for timing link retrieval
            watch = Stopwatch()

            # Get and strip the query received
            search_query = request.form['query'].strip()

            # Retrieve the document ids for the given query and lookup their associated urls, while also timing it
            watch.start()
            retrieved_ids = find_search_query(search_query)
            associated_urls = [document_id_lookups[next_id] for next_id in retrieved_ids]
            watch.stop()

            # If no results were obtained, flash as much to the webserver
            if len(associated_urls) == 0:
                flash(f"No results for query: {search_query}")
            # Otherwise, flash the results
            else:
                # Flash the current query to the search_engine.html page
                flash(f"Results for query: {search_query}")

                # Flash each retrieved link to the search_engine.html page
                for next_link in associated_urls:
                    flash(next_link)

            # Flash the time taken for the link retrieval to the search_engine.html page
            flash(f"Time taken for search retrieval: {round(watch.read() * 1000)} ms")

        # When http://127.0.0.1:5000/ is accessed, render the search_engine.html page in the templates directory
        return render_template("search_engine.html")

    # Return the constructed Flask app
    return app


if __name__ == '__main__':
    # Construct and execute the application
    app = create_app()
    app.run()
