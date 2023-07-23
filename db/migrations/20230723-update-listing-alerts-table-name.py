"""
Update listing alerts table name
"""

from yoyo import step

__depends__ = {'20230719-add-last-updated-timestamp-column-to-watched-car'}

steps = [
    step(apply="ALTER TABLE listing_alerts RENAME TO listing_alert;",
         rollback="ALTER TABLE listing_alert RENAME TO listing_alerts")
]
