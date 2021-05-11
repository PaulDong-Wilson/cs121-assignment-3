from flask import Flask, flash, render_template, request
from stopwatch import Stopwatch

# To hold the file location for document IDs
document_id_file = "document_ids.txt"


def test_response(num_links: int) -> [str]:
    """
    TESTING FUNCTION PLEASE IGNORE

    TODO DELETE AFTER LINK RETRIEVAL IS IMPLEMENTED

    :param num_links: The number of fake links to return.
    :return: A list of fake links for testing purposes.
    """
    for i in range(10000000):
        pass

    if num_links <= 0:
        return []

    return [f"Link {i}" for i in range(1, num_links + 1)]


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

            # Flash the current query to the search_engine.html page
            flash(f"Results for query: {request.form['query']}")

            # Retrieve the links for the given query, while also timing it
            watch.start()
            retrieved_links = test_response(5) # TODO Replace with link retrieval implementation once finished
            watch.stop()

            # Flash each retrieved link to the search_engine.html page
            for next_link in retrieved_links:
                flash(next_link)

            # Flash the time taken for the link retrieval to the search_engine.html page
            flash(f"Time taken for search retrieval: {round(watch.read(), 5)} seconds")

        # When http://127.0.0.1:5000/ is accessed, render the search_engine.html page in the templates directory
        return render_template("search_engine.html")

    # Return the constructed Flask app
    return app


if __name__ == '__main__':
    # Construct and execute the application
    app = create_app()
    app.run()
