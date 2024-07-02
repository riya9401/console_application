CREATE PROCEDURE CalculateAverages(item_id INT)
BEGIN
    DECLARE average_rating DECIMAL(5,2);
    DECLARE average_sentiment DECIMAL(5,2);

    SELECT AVG(rating) INTO average_rating
    FROM feedback
    WHERE item_id = item_id;

    SELECT AVG(sentiment) INTO average_sentiment
    FROM feedback
    WHERE item_id = item_id;

     UPDATE item_score
    SET average_rating = average_rating, average_sentiment
 =average_sentiment
    WHERE item_id = item_id;
END