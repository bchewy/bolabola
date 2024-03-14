var express = require("express")
var { createHandler } = require("graphql-http/lib/use/express")
var { buildSchema } = require("graphql")
var mongoose = require("mongoose");
var { ruruHTML } = require("ruru/server")
// var prometheus = require('prom-client');
// // Create a Prometheus counter
// const counter = new prometheus.Counter({
//   name: 'api_requests_total',
//   help: 'Total number of API requests',
//   labelNames: ['method', 'path'],
// });



mongoose.connect("mongodb://mongodb:27017/matches");

var MatchSchema = new mongoose.Schema({
  name: String,
  home_team: String,
  away_team: String,
  home_score: Number,
  away_score: Number,
});

const MatchModel = mongoose.model("Match", MatchSchema);

var schema = buildSchema(`
  type Match {
    name: String
    home_team: String
    away_team: String
    home_score: Int
    away_score: Int
  }
  
  type Query {
    matches: [Match]
  }  
`)

// The root provides a resolver function for each API endpoint
const root = {
  matches: async () => {
    try {
      return await MatchModel.find();
    } catch (error) {
      throw error;
    }
  }
};

const app = express();

// Create and use the GraphQL handler
app.all(
  "/graphql",
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

// Middleware to increment the counter for each API request
// app.use((req, res, next) => {
//   counter.inc({ method: req.method, path: req.path });
//   next();
// });

// // Expose Prometheus metrics endpoint
// app.get('/metrics', (req, res) => {
//   res.set('Content-Type', prometheus.register.contentType);
//   res.end(prometheus.register.metrics());
// });

// Start the server at port
app.listen(9001)