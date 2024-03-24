var express = require("express")
var { createHandler } = require("graphql-http/lib/use/express")
var { buildSchema } = require("graphql")
var mongoose = require("mongoose");
var { ruruHTML } = require("ruru/server")
var cors = require("cors"); // Import cors
var amqp = require('amqplib'); // Import the amqplib library for async messaging


// Add CORS middleware


// var prometheus = require('prom-client');
// // Create a Prometheus counter
// const counter = new prometheus.Counter({
//   name: 'api_requests_total',
//   help: 'Total number of API requests',
//   labelNames: ['method', 'path'],
// });



mongoose.connect("mongodb://mongodb:27017/matches");

var MatchOverviewSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  name: String,
  home_team: String,
  away_team: String,
  home_score: Number,
  away_score: Number,
  date: Date,
  seats: Number,
  categories: [{ category: String, quantity: Number }],

});

var MatchDetailsSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  name: String,
  description: String,
  venue: String,
  home_team: String,
  away_team: String,
  home_score: Number,
  away_score: Number,
  date: Date,
  seats: Number,
});

var TicketSchema = new mongoose.Schema({
  match_id: { type: mongoose.Schema.Types.ObjectId, ref: 'MatchOverview' },
  seat_number: Number,
  user_id: mongoose.Schema.Types.ObjectId, // This can be null initially, to signify that the user has not booked the ticket
  category: String, // Added category field

});

const MatchOverviewModel = mongoose.model("MatchOverview", MatchOverviewSchema, "matches");
const MatchDetailsModel = mongoose.model("MatchDetails", MatchDetailsSchema, "matches");

// Create another connection to tickets collection, to store tickets.
var mongoose_tickets = mongoose.createConnection("mongodb://mongodb:27017/tickets");
const Ticket = mongoose_tickets.model("Ticket", TicketSchema, "tickets");

var schema = buildSchema(`
  type MatchOverview {
    _id: ID
    name: String
    home_team: String
    away_team: String
    home_score: Int
    away_score: Int
    date: String
    seats: Int
    categories: [Category]
  }

  type MatchDetails {
    _id: ID
    name: String
    description: String
    venue: String
    home_team: String
    away_team: String
    home_score: Int
    away_score: Int
    date: String
    seats: Int
    categories: [Category]
  }

  type Category {
    category: String
    quantity: Int
  }

  input CategoryInput {
    category: String!
    quantity: Int!
  }
  
  type Query {
    matches_overview: [MatchOverview]
    match_details(_id: String): MatchDetails
  }
  type Mutation {
    createMatch(name: String!, home_team: String!, away_team: String!, date: String!, seats: Int!, categories: [CategoryInput]!): MatchOverview
  }
  
`)


// Logging midddleware - just to view logs in the console
function logGraphQLRequests(req, res, next) {
  console.log('GraphQL Request:', {
    query: req.body.query,
    variables: req.body.variables,
    operationName: req.body.operationName,
  });
  next();
}

// The root provides a resolver function for each API endpoint
const root = {
  matches_overview: async () => {
    try {
      return await MatchOverviewModel.find();
    } catch (error) {
      throw error;
    }
  },
  match_details: async ({ _id }) => {
    try {
      return await MatchDetailsModel.findById(new mongoose.Types.ObjectId(_id));
    } catch (error) {
      throw error;
    }
  },
  createMatch: async ({ name, home_team, away_team, date, seats, categories }) => {
    try {
      // Create a new match
      const newMatch = new MatchOverviewModel({
        _id: new mongoose.Types.ObjectId(),
        name,
        home_team,
        away_team,
        date,
        seats,
        categories
      });
      await newMatch.save();

      // Log the creation details
      console.log(`Match created: ${name} between ${home_team} and ${away_team} on ${date}. Total seats: ${seats}.`);

      // Optionally, log the categories if needed
      console.log('Categories:', categories);

      // Generate tickets for the match based on categories
      for (let i = 0; i < categories.length; i++) {
        const category = categories[i];
        for (let j = 1; j <= category.quantity; j++) {
          const newTicket = new Ticket({
            match_id: newMatch._id,
            seat_number: j,
            user_id: null, // Initially, tickets are not assigned to any user
            category: category.category, // Assuming you have a category field in your Ticket schema
          });
          await newTicket.save();
        }
      }
      // Return the created match
      return newMatch;
    } catch (error) {
      throw error;
    }
  },
};

// Express server
const app = express();
app.use(cors());
app.use(express.json());

// Create and use the GraphQL handler
app.all(
  "/graphql",
  logGraphQLRequests,
  createHandler({
    schema: schema,
    rootValue: root,
  })
);



// Serve the GraphiQL IDE.
app.get("/", (_req, res) => {
  res.type("html")
  res.end(ruruHTML({ endpoint: "/graphql" }))
})

// app.use((req, res, next) => {
//   counter.inc({ method: req.method, path: req.path });
//   next();
// });
// app.get('/metrics', (req, res) => {
//   res.set('Content-Type', prometheus.register.contentType);
//   res.end(prometheus.register.metrics());
// });

// function to handle incoming json
const handleIncomingMessage = async (data) => {
  const message = JSON.parse(data.content.toString());
  console.log("Received message:", message);

  const match = await MatchOverviewModel.findById(message.match_id);

  if (!match) {
    console.error(`Match with id ${message.match_id} not found`);
    return;
  }

  console.log(`Match ${match._id} at first had ${match.seats} seats available`);
  match.seats -= message.quantity;
  await match.save();
  console.log(`Match ${match._id} now has ${match.seats} seats available`);
};

// function to set up RabbitMQ consumer
const setupRabbitMQConsumer = async () => {
  try {
    const connection = await amqp.connect('amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/');
    const channel = await connection.createChannel();
    const exchange = 'match-booking-exchange';
    await channel.assertExchange(exchange, 'topic', { durable: true });
    const queue = await channel.assertQueue("match", { durable: true });

    await channel.bindQueue(queue.queue, exchange, "match.#");

    console.log("Waiting for messages in %s. To exit press CTRL+C", queue.queue);

    // Use the promise-based consume method
    await channel.consume(queue.queue, handleIncomingMessage, { noAck: false });
  } catch (error) {
    console.error("Error setting up RabbitMQ consumer:", error);
  }
};

app.listen(9001)
setupRabbitMQConsumer();