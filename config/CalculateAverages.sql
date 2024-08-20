CREATE DEFINER="root"@"localhost" PROCEDURE "CalculateAverages"(IN item_id INT)
BEGIN
    DECLARE average_rating DECIMAL(5,1);
    DECLARE average_sentiment DECIMAL(5,2);

    SELECT AVG(rating) INTO average_rating
    FROM feedback
    WHERE feedback.item_id = item_id;

    SELECT AVG(sentiment) INTO average_sentiment
    FROM feedback
    WHERE feedback.item_id = item_id;

    IF EXISTS (SELECT 1 FROM item_score WHERE item_score.item_id = item_id) THEN
        UPDATE item_score
        SET average_rating = average_rating, average_sentiment = average_sentiment
        WHERE item_score.item_id = item_id;
    ELSE
        INSERT INTO item_score (item_id, average_rating, average_sentiment)
        VALUES (item_id, average_rating, average_sentiment);
    END IF;
END