from flask import (Flask, render_template, make_response,
                   redirect)
from flask_restful import Api, Resource, reqparse, abort


import json
import random
import string


QUANTITIES = (0, 1, 2, 3, 4, 5)

# Load data from disk.
# This simply loads the data from our "database," which is just 3 JSON files.
with open('data') as data:
    data = json.load(data)

with open('gameData') as gameData:
    gameData = json.load(gameData)

with open('seatData') as seatData:
    seatData = json.load(seatData)


# Generate a unique ID for a new ticket order.
# By default this will consist of six lowercase numbers and letters.
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no ticketorder with the specified ID exists.
def error_if_ticketorder_not_found(ticketorder_id):
    if ticketorder_id not in data['ticketorders']:
        message = "No help ticket with ID: {}".format(ticketorder_id)
        abort(404, message=message)

# Respond with 404 Not Found if no game with the specified ID exists.
def error_if_game_not_found(game_id):
    if game_id not in gameData['games']:
        message = "No game with ID: {}".format(game_id)
        abort(404, message=message)


# Filter and sort a list of ticketorders.
def filter_and_sort_ticketorders(query=''):

    # Returns True if the query string appears in the ticketorders's
    # title or description.
    def matches_query(item):
        (ticketorder_id, ticketorder) = item
        text = ticketorder['firstName'] + ticketorder['lastName']
        return query.lower() in text
    filtered_ticketorders = filter(matches_query, data['ticketorders'].items())
    return sorted(filtered_ticketorders, reverse=True)


# Filter and sort a list of game.
def filter_and_sort_games(query=''):

    # Returns True if the query string appears in the sportsTickets's
    # title or description.
    def matches_query(item):
        (game_id, game) = item
        text = game['date'] + game['teams']
        return query.lower() in text
    filtered_games = filter(matches_query, gameData['games'].items())
    return sorted(filtered_games, reverse=True)


def filter_and_sort_seats(query=''):

    # Returns True if the query string appears in the sportsTickets's
    # title or description.
    def matches_query(item):
        (seat_id, seat) = item
        text = seat['section'] + seat['row']
        return query.lower() in text
    filtered_seats = filter(matches_query, seatData['seats'].items())
    return sorted(filtered_seats, reverse=True)


# Now we define three incoming HTTP request parsers using the Flask-RESTful
# framework <https://flask-restful.readthedocs.io/en/latest/reqparse.html>.
#
# The first (new_sportsTickets_parser) parses incoming POST requests and checks
# that they have the required values.
#
# The second (update_sportsTickets_parser) parses incoming PATCH requests and
# checks that they have the required values.
#
# The third (query_parser) parses incoming GET requests to get the parameters
# for sorting and filtering the list of help tickets.

# Helper function new_sportsTickets_parser. Raises an error if the string x
# is empty (has zero length).
def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


# Specify the data necessary to create a new help ticket.
# "from", "title", and "description" are all required values.
new_ticketorder_parser = reqparse.RequestParser()
for arg in ['firstName', 'lastName', 'shippingAddress', 'phoneNumber', 'zipcode', 'paymentMethod', 'cardNumber',
            'cvv', 'expDate', 'billingAddress', 'date', 'quantity', 'price', 'section', 'row', 'teams',
            'location', 'email']:
    new_ticketorder_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))


# Specify the data necessary to update an existing help ticket.
# Only the priority and comments can be updated.
update_ticketorder_parser = reqparse.RequestParser()
update_ticketorder_parser.add_argument(
    'phoneNumber', type=str, default='')
update_ticketorder_parser.add_argument(
    'email', type=str, default='')
update_ticketorder_parser.add_argument(
    'shippingAddress', type=str, default='')
update_ticketorder_parser.add_argument(
    'zipcode', type=str, default='')


# Specify the parameters for filtering and sorting help tickets.
# See `filter_and_sort_helptickets` above.
query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'query', type=str, default='')

# Then we define a couple of helper functions for inserting data into HTML
# templates (found in the templates/ directory). See
# <http://flask.pocoo.org/docs/latest/quickstart/#rendering-templates>.


# Given the data for a ticketorder, generate an HTML representation
# of that ticketorder.
def render_ticketorder_as_html(ticketorder):
    return render_template(
        'Order.html',
        ticketorder=ticketorder,
        quantities=reversed(list(enumerate(QUANTITIES))))


# Given the data for a list of ticketorders, generate an HTML representation
# of that list.
def render_ticketorder_list_as_html(ticketorders):
    return render_template(
        'OrderList.html',
        ticketorders=ticketorders,
        quantities=QUANTITIES)

# Given the data for a list of games, generate an HTML representation
# of that list.
def render_ticketorder_gameinfo_as_html(games):
    return render_template('GameInfo.html', games=games)

# Given the data for a list of seats and a single game, generate an HTML representation
# of that list.
def render_ticketorder_seatchoose_as_html(game, seats):
    return render_template('Seat.html', game=game, seats=seats, quantities=QUANTITIES)


# Now we can start defining our resource classes. We define four classes:
# TicketOrder, TicketOrderList, GameInfo, and SeatChoose.
# All of them accept GET requests. TicketOrder also accepts PATCH requests,
# and TicketOrderList also accepts POST requests.


# Define our help ticket resource.
class TicketOrder(Resource):

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, ticketorder_id):
        error_if_ticketorder_not_found(ticketorder_id)
        return make_response(
            render_ticketorder_as_html(
                data['ticketorders'][ticketorder_id]), 200)

    # If a help ticket with the specified ID does not exist,
    # respond with a 404, otherwise update the help ticket and respond
    # with the updated HTML representation.
    def patch(self, ticketorder_id):
        error_if_ticketorder_not_found(ticketorder_id)
        ticketorder = data['ticketorders'][ticketorder_id]
        update = update_ticketorder_parser.parse_args()
        ticketorder['phoneNumber'] = update['phoneNumber']
        ticketorder['shippingAddress'] = update['shippingAddress']
        ticketorder['zipcode'] = update['zipcode']
        ticketorder['email'] = update['email']

        return make_response(
            render_ticketorder_as_html(ticketorder), 200)


# Define our help ticket list resource.
class TicketOrderList(Resource):

    # Respond with an HTML representation of the help ticket list, after
    # applying any filtering and sorting parameters.
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_ticketorder_list_as_html(filter_and_sort_ticketorders(**query)), 200)
    # Add a new help ticket to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        ticketorder = new_ticketorder_parser.parse_args()
        ticketorder_id = generate_id()
        data['ticketorders'][ticketorder_id] = ticketorder
        ticketorder['orderNumber'] = ticketorder_id
        return make_response(
            render_ticketorder_list_as_html(
                filter_and_sort_ticketorders()), 201)


# Direct to Game Info
class GameInfo(Resource):

    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_ticketorder_gameinfo_as_html(filter_and_sort_games(**query)), 200)


# Direct to Seat Selection
class SeatChoose(Resource):
    def get(self, game_id):
        error_if_game_not_found(game_id)
        query = query_parser.parse_args()
        return make_response(
            render_ticketorder_seatchoose_as_html(gameData['games'][game_id], filter_and_sort_seats(**query)), 200)


# After defining our resource classes, we define how URLs are assigned to
# resources by mapping resource classes to URL patterns.
app = Flask(__name__)
api = Api(app)
api.add_resource(TicketOrder, '/order/<string:ticketorder_id>')
api.add_resource(TicketOrderList, '/orders')
api.add_resource(GameInfo, '/orders/gameInfo')
api.add_resource(SeatChoose, '/orders/<string:game_id>/seats')


# There is no resource mapped to the root path (/), so if a request comes in
# for that, redirect to the HelpTicketList resource.

@app.route('/')
def index():
    return redirect(api.url_for(TicketOrderList), code=303)


# Finally we add some headers to all of our HTTP responses which will allow
# JavaScript loaded from other domains and running in the browser to load
# representations of our resources (for security reasons, this is disabled
# by default.

@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# Now we can start the server.

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5555,
        debug=True,
        use_debugger=False,
        use_reloader=False)
