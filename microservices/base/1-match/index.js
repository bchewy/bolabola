var express = require("express")
var { createHandler } = require("graphql-http/lib/use/express")
var { buildSchema } = require("graphql")
var mongoose = require("mongoose");
var { ruruHTML } = require("ruru/server")

mongoose.connect("mongodb://mongodb:27017/matches");


var MatchOverviewSchema = new mongoose.Schema({
  match_id: {
    type: mongoose.Schema.Types.ObjectId,
    auto: true,
  },
  name: String,
  home_team: String,
  away_team: String,
  home_score: Number,
  away_score: Number,
  date: Date,
  thumbnail_url: String
});

var MatchDetailsSchema = new mongoose.Schema({
  match_id: {
    type: mongoose.Schema.Types.ObjectId,
    auto: true,
  },
  name: String,
  description: String,
  venue: String,
  home_team: String,
  away_team: String,
  home_score: Number,
  away_score: Number,
  date: Date,
  thumbnail_url: String
});

const MatchOverviewModel = mongoose.model("MatchOverview", MatchOverviewSchema);
const MatchDetailsModel = mongoose.model("MatchDetails", MatchDetailsSchema);

var schema = buildSchema(`
  type MatchOverview {
    name: String
    home_team: String
    away_team: String
    home_score: Int
    away_score: Int
  }

  type MatchDetails {
    match_id: String
    name: String
    description: String
    venue: String,
    home_team: String
    away_team: String
    home_score: Int
    away_score: Int
    date: String
    thumbnail_url: String
  }
  
  type OverviewQuery {
    matches: [MatchOverview]
  }

  type DetailsQuery {
    match: MatchDetails
  }
`);

// The root provides a resolver function for each API endpoint
const root = {
  matches_overview: async () => {
    try {
      return await MatchOverviewModel.find();
    } catch (error) {
      throw error;
    }
  },

  match_details: async (match_id) => {
    try {
      return await MatchDetailsModel.findById(match_id);
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

// Start the server at port
app.listen(9001)