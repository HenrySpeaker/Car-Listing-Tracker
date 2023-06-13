"""
Change body styles to reflect capitalized first letters
"""

from yoyo import step

__depends__ = {'20230530-add-state-id-column-to-cities-table'}

steps = [
    step(apply="""
        ALTER TYPE body_style_type RENAME TO old_body_style_type;

        CREATE TYPE body_style_type AS ENUM (
                'Convertible',
                'Coupe',
                'Hatchback',
                'Van/Minivan',
                'Sedan',
                'SUV',
                'Pickup',
                'Wagon'
                );
        
        ALTER TABLE body_style ALTER COLUMN body_style_name TYPE body_style_type USING body_style_name::text::body_style_type;

        DROP TYPE old_body_style_type;
    """,
         rollback="""
        ALTER TYPE body_style_type RENAME TO old_body_style_type;

        CREATE TYPE body_style_type AS ENUM (
                'convertible',
                'coupe',
                'hatchback',
                'minivan',
                'sedan',
                'suv',
                'truck',
                'wagon'
                );
        
        ALTER TABLE body_style ALTER COLUMN body_style_name TYPE body_style_type USING body_style_name::text::body_style_type;

        DROP TYPE old_body_style_type;
    """)
]
