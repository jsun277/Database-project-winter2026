// Q6: Retrieve all recent search terms used by Sarah (user_id: 1)
// and categorize them by frequency and time of day.

db.user_events.aggregate([
  { $match: { user_id: 1, event_type: "search" } },
  {
    $addFields: {
      time_of_day: {
        $switch: {
          branches: [
            { case: { $lt: [{ $hour: "$timestamp" }, 6] },  then: "night" },
            { case: { $lt: [{ $hour: "$timestamp" }, 12] }, then: "morning" },
            { case: { $lt: [{ $hour: "$timestamp" }, 18] }, then: "afternoon" }
          ],
          default: "evening"
        }
      }
    }
  },
  {
    $group: {
      _id: { term: "$search_query", time_of_day: "$time_of_day" },
      count: { $sum: 1 }
    }
  },
  {
    $group: {
      _id: "$_id.term",
      total: { $sum: "$count" },
      by_time: { $push: { time: "$_id.time_of_day", count: "$count" } }
    }
  },
  { $sort: { total: -1 } }
]);
