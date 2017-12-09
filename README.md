# SportsSeat
flask and flask restful practice

One things needs to mention: on the OrderList.html, which is the first page after running the server, only the link "Atlanta Hawks" works. I tried to crawl the data from the website, but I failed. So to meet the requirments of the assignment, I just use one basketball team to realize my server example. 

<class>
team
	Indicates the table including all the sports teams.
orderList
	Contains all the orders customer placed before.
gameInfo
	Indicates the information including Date, Teams, Locations of a certain team.
seat
	Indicates a table of seat information. It contains the section, row, price, quantity. 
order-creator
	Indicates a form aiming for creating a order.
name
	Indicates the first name and the last name of a customer.
address
	Indicates the shipping address of an order.
contact
	Indicates the contact including phone number and email of a customer.
payment
	Indicates the payment information of an order
create
	Indicates an order creation
orderInfo
	Indicates the detailed information of a list of orders 
order-updater
	Indicates a form used to update some information of an order

<Rel>
contents
	Appears the games of a certain team. Refers to a table of contents.
about
	Appears the details of a certain order. Refers to a resource that is the subject of the 	
	link's context.
next
	Choosing seats, filling out order form are parts of placing an order. Indicates that the 
	link's context is a part of a series, and that the next in the series is the link target.
collection
	Indicates a list of orders customer placed before. The target IRI points to a resource 
	which represents the collection resource for the context IRI.
  
 <data types>
 1. data: the data of the order
    properties:
      "orderNumber" 
      "firstName"
      "lastName" 
      "shippingAddress" 
      "phoneNumber"
      "zipcode"
      "paymentMethod"
      "cardNumber"
      "cvv"
      "expDate"
      "billingAddress"
      "quantity"
      "date" 
      "teams" 
      "location" 
      "section" 
      "row" 
      "price" 
      "totalPrice"
      "email"
 2. gameData: the data of the NBA games
    properties:
      "date" 
      "teams" 
      "location" 
3.  seatData: the data of the seats
    properties:
      "section" 
      "row" 
      "price" 
