class RawQueries:
    """
    A collection of raw SQL queries used in the application.
    """
    popular_select = """
        SELECT      rec.*, AVG(rev.rating) AS avg_rating, COUNT(rev.id) AS review_count 
        FROM        core_recipe AS rec
        JOIN        core_review AS rev ON rev.recipe_id = rec.id
        GROUP BY    rec.id
        HAVING      avg_rating >= %s
        AND         review_count >= %s
        ORDER BY    review_count DESC, avg_rating DESC;
        """

    trending_select = """
        SELECT      rec.*, COUNT(rev.id) AS review_count 
        FROM        core_recipe AS rec
        JOIN        core_review AS rev 
        ON          rev.recipe_id = rec.id
        AND         (julianday(CURRENT_TIMESTAMP) - julianday(rev.created_at)) * 86400.0 <= %s
        GROUP BY    rec.id
        HAVING      review_count >= %s
        ORDER BY    review_count DESC;
        """
