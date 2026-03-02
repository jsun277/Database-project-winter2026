// Q5: Display the number of times each product page has been viewed,
// ordered by popularity (number of views).

db.user_events.aggregate([
  { $match: { event_type: "product_view" } },
  { $group: { _id: "$product_id", view_count: { $sum: 1 } } },
  { $sort: { view_count: -1 } },
  { $limit: 20 }
]);
