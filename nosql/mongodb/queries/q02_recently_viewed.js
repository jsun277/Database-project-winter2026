// Q2: Retrieve the last 5 products viewed by Sarah (user_id: 1)
// within the past 6 months, ordered by most recent activity.

db.user_events.find({
  user_id: 1,
  event_type: "product_view",
  timestamp: { $gte: new Date(Date.now() - 6 * 30 * 24 * 60 * 60 * 1000) }
})
.sort({ timestamp: -1 })
.limit(5);
