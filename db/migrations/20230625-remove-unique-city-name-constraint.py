"""
Remove unique city name constraint
"""

from yoyo import step

__depends__ = {'20230625-increase-state-name-size-limit'}

steps = [
    step(apply="""
        ALTER TABLE city
        DROP CONSTRAINT IF EXISTS city_city_name_key;
    """,
         rollback="""
        ALTER TABLE city
        ADD CONSTRAINT city_city_name_key UNIQUE(city_name);
    """)
]
