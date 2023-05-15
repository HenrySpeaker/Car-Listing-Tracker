"""
Create user table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """CREATE TABLE user_account (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL, 
            email VARCHAR(100) UNIQUE NOT NULL, 
            password_hash VARCHAR(200) NOT NULL, 
            notification_frequency SMALLINT CHECK (notification_frequency > 0 AND notification_frequency < 31), 
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CLOCK_TIMESTAMP(), 
            last_login TIMESTAMP WITH TIME ZONE DEFAULT CLOCK_TIMESTAMP())"""
    )
]
